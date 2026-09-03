from playwright.sync_api import sync_playwright
import pathlib
p_html = pathlib.Path(r'C:\Users\wroge\AppData\Local\Temp\claude\c--Code-Ripple-v6\6ee210e7-d88d-4de6-85b1-9c5796ff377f\scratchpad\warehouse-map.html')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1600, 'height': 900})
    pg.goto(p_html.as_uri())
    pg.wait_for_timeout(1200)
    pg.screenshot(path=str(p_html.parent / 'map_shot.png'))
    pg.evaluate("""() => {
      const s = 0.18, w = document.getElementById('world');
      const tx = innerWidth/2 - 2420*s, ty = innerHeight/2 - 911*s;
      w.style.transform = `translate(${tx}px,${ty}px) scale(${s})`;
    }""")
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(p_html.parent / 'map_far.png'))
    b.close()
print('ok')
