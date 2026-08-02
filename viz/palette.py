"""
The Library's visual language. Three inks, three meanings, no exceptions:

    AMBER  evidence -- the confidence ladder, rare-ID chips, link UI. Never
           decoration. One hue that dims as certainty drops, so a hunch can
           never be drawn as loudly as a certainty.
    BLUE   process -- pipeline stages, lineage. Brightens as data becomes
           more useful.
    GRAYS  presence -- brightness = evidence. Full white only for selection
           and bridges; uncharted tables are dim, never invisible.

Everything a figure or panel needs to look like the Library imports from
here; nothing else defines a colour.
"""

# Strongest first. Order is meaning (design brief D2) -- do not shuffle.
LADDER_COLOUR = ["#fbc06a", "#eda748", "#d98d33", "#bd7327", "#9d5c1e", "#7d4818"]

# The five pipeline stages, dim to bright as data becomes more useful, plus
# the siding for tables never wired into the build.
STAGE_COLOUR = {
    "siding": "#31404f",
    "intake": "#256abf",
    "staging": "#3987e5",
    "bridge": "#6da7ec",
    "shelf": "#9ec5f4",
    "desk": "#cde2fb",
}
STAGE_ORDER = ["siding", "intake", "staging", "bridge", "shelf", "desk"]

# Presence, as brightness. lit > dark > keyless > uncharted -- but all four
# are drawn, all four are clickable. Dim always means "quiet", never "bad".
STATE_COLOUR = ["#eef1f5", "#8fa0b5", "#5d6d80", "#41505f"]
STATE_OPACITY = [1.0, 0.95, 0.85, 0.45]

SURFACE = "#0d1117"
PANEL = "#0f1620"
PANEL_2 = "#121a24"
INK = "#e8eaed"
INK_2 = "#9aa4b2"
INK_3 = "#6b7684"
RULE = "rgba(255,255,255,.10)"
MONO = "ui-monospace, SFMono-Regular, Consolas, monospace"
SANS = 'ui-sans-serif, system-ui, "Segoe UI", sans-serif'

VIEW_BLURB = {
    "subject": ("Arranged by subject",
                "Every dataset, in a room with the others about the same "
                "thing. Bigger room, more datasets. Bigger tile, more records "
                "inside it. The quiet band along the bottom is the annex: "
                "collected, not yet wired in."),
    "connection": ("Arranged by what connects to what",
                   "Two datasets can only be linked if they share an ID. Each "
                   "one sits beside the ID it's identified by; the bright "
                   "ones between two wells carry two rare IDs, and those are "
                   "what let a question travel from one world to another."),
    "journey": ("Arranged by the journey data takes",
                "Left to right is the order things actually happen: raw files "
                "land, get tidied up, a few get combined, most become ready "
                "to use, and a handful end up in a queue for a person. The "
                "left-most siding holds what's collected but not yet built on."),
}

STATE_STORY = [
    # Plain words for each presence state, used by the dossier.
    ("Connected", "This one has verified links -- it's part of the mesh."),
    ("Measured, no match yet",
     "It carries a real ID and we ran the search: nothing matched. That's a "
     "measured fact, and it's on the follow-up list."),
    ("Nothing to match on yet",
     "None of its columns work as an ID we could join with. Getting a better "
     "column is the fix."),
    ("Measured and shelved",
     "This one hasn't been through link discovery yet -- that pass is "
     "queued, not missed. Most of these already carry a usable ID."),
]
