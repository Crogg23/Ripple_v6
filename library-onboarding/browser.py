"""Headless-browser rendering (C1b) -- Playwright.

The static scrape path (C1 Phase 1: requests + BeautifulSoup) reaches any page
whose data lives in the initial HTML. It does NOT reach two whole classes of page:

  - **JS-rendered** pages (SPAs) where the data is injected client-side after load,
    so the raw HTML `requests` gets back is an empty shell.
  - **Bot-protected** pages that serve a JavaScript challenge ("Just a moment...",
    Cloudflare interstitials) to non-browser clients -- a 200 with no real content.

`render(url)` drives a real headless Chromium via Playwright: it loads the page,
runs its JavaScript, waits for the content to settle (and optionally for a CSS
selector), optionally scrolls to trigger lazy content, then returns the
fully-rendered HTML. The Claude-generated `fetch_data()` then parses that HTML with
BeautifulSoup / pandas.read_html exactly like a static page -- the only thing that
changed is HOW the bytes were fetched.

Playwright is an **optional, heavy** dependency: the pip package is small but it
drives a ~170 MB browser binary installed separately (`playwright install
chromium`). It is imported lazily so the rest of the agent runs without it, and
`render()` raises a clear, actionable error if either the package or the browser
binary is missing -- the agent only pays the cost for sources that actually need it.
"""

from __future__ import annotations

from config import settings

# A real desktop-Chrome UA. Many bot walls 403 (or challenge) obvious automation
# UAs; the headless browser already looks like Chrome, this just removes the
# "HeadlessChrome" tell from the default string.
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Telltales of a page that did NOT give us real content: a JS bot-challenge, or a
# notice that JS is required. Used to decide when static fetch should escalate to
# the browser (recon) and surfaced for callers that want to detect a wall.
CHALLENGE_MARKERS = (
    "just a moment",
    "checking your browser",
    "cf-browser-verification",
    "challenge-platform",
    "cf_chl",
    "enable javascript",
    "please enable javascript",
    "ddos protection by",
)


def playwright_available() -> bool:
    """True if the Playwright package can be imported (browser may still be absent)."""
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False


def looks_blocked(html: str, min_chars: int = 600) -> bool:
    """Heuristic: does this HTML look like a bot-challenge / empty-SPA shell?

    True when the page carries a known challenge marker, or is suspiciously short
    (a challenge interstitial / SPA skeleton is tiny compared to a real listing).
    Lets recon and generated fetches notice "we got a wall, not data" and escalate
    to the browser.
    """
    if not html:
        return True
    low = html.lower()
    if any(marker in low for marker in CHALLENGE_MARKERS):
        return True
    # An SPA shell with a mount point and almost no text is also "blocked" for our
    # purposes (the data isn't in the static HTML).
    if len(html) < min_chars:
        return True
    return False


def render(
    url: str,
    *,
    wait_until: str | None = None,
    wait_selector: str | None = None,
    timeout_ms: int | None = None,
    user_agent: str | None = None,
    scroll: bool = False,
    ignore_https_errors: bool | None = None,
) -> str:
    """Load ``url`` in headless Chromium and return the fully-rendered HTML.

    Args:
        wait_until: navigation milestone for ``page.goto`` (``domcontentloaded`` by
            default -- reliable; a bounded ``networkidle`` wait happens afterwards).
        wait_selector: if given, wait until this CSS selector appears (the most
            robust signal that the data has rendered -- prefer it over timing).
        timeout_ms: per-step timeout (navigation / selector wait).
        user_agent: override the default desktop-Chrome UA.
        scroll: nudge the page down a few times to trigger lazy / infinite-scroll
            content before reading.
        ignore_https_errors: accept untrusted certs (needed behind TLS-intercepting
            proxies). Defaults to the ``ONBOARD_BROWSER_IGNORE_HTTPS_ERRORS`` setting.

    Raises:
        RuntimeError: with install instructions if Playwright or the browser binary
            is missing, or if navigation fails.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "This source needs a headless browser (access_pattern=scrape_js) but "
            "Playwright is not installed. Install it with:\n"
            "    pip install playwright && playwright install chromium"
        ) from exc

    wait_until = wait_until or settings.browser_wait_until
    timeout_ms = timeout_ms or settings.browser_timeout_ms
    ua = user_agent or DEFAULT_UA
    ignore_https = (
        settings.browser_ignore_https_errors
        if ignore_https_errors is None
        else ignore_https_errors
    )

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
                headless=settings.browser_headless,
                # --no-sandbox: required to run Chromium as root in a container.
                # --disable-dev-shm-usage: avoid crashes on small /dev/shm.
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
        except Exception as exc:  # browser binary missing / failed to launch
            raise RuntimeError(
                "Playwright is installed but Chromium could not launch -- the browser "
                "binary is likely missing. Install it with:\n"
                "    playwright install chromium\n"
                f"(underlying error: {exc})"
            ) from exc
        try:
            ctx = browser.new_context(user_agent=ua, ignore_https_errors=ignore_https)
            page = ctx.new_page()
            page.goto(url, wait_until=wait_until, timeout=timeout_ms)

            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=timeout_ms)
            else:
                # Best-effort settle: let in-flight XHR/fetch (and JS challenges that
                # reload into real content) finish. Bounded so a chatty page can't hang.
                try:
                    page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 20_000))
                except Exception:
                    pass

            if scroll:
                for _ in range(8):
                    page.mouse.wheel(0, 20_000)
                    page.wait_for_timeout(500)

            return page.content()
        finally:
            browser.close()
