import streamlit as st
import textwrap
from dataclasses import dataclass
from typing import Callable, List, Dict, Tuple
import math, io, wave
from array import array

st.set_page_config(page_title="Python Garden", page_icon="🪴", layout="wide")


st.markdown(
    """
    <style>
      .stApp {background: radial-gradient(1200px 600px at 0% 0%, #f0fdf4 0%, #ffffff 40%), radial-gradient(1200px 600px at 100% 0%, #eff6ff 0%, transparent 40%), radial-gradient(1200px 600px at 100% 100%, #fff7ed 0%, transparent 40%);} 
      @keyframes floaty {0%{transform:translateY(0)} 50%{transform:translateY(-10px)} 100%{transform:translateY(0)}}
      .stMainBlockContainer {max-width:1080px; margin: 12px auto; padding: 10px 14px; border-radius: 18px; background: rgba(255,255,255,0.75); box-shadow: 0 1px 0 rgba(0,0,0,0.02), 0 8px 40px rgba(2,6,23,0.06);} 
      #python-garden {text-align: center;}
      .badge {display:inline-block; padding:4px 10px; border-radius:999px; background:#e8f7ee; color:#065f46; font-weight:700; font-size:12px;}
      .big-emo {font-size: 32px; line-height:1; display:inline-block; padding: 0 6px;}
      .lbl { color:#334155; font-weight:700; }
      .garden { border-collapse: collapse; margin: 0.25rem 0; border: 1px solid #e5e7eb; }
      .garden th, .garden td { border: 1px solid #e5e7eb; width: 48px; height: 48px; text-align: center; }
      .garden th.hdr { background: #f8fafc; font-weight: 800; font-size: 12px; color: #334155; width: 32px; }
      .cell { transition: transform 120ms ease, background 200ms ease; }
      .cell:hover { transform: scale(1.05); }
      .cell.empty  { background: #ffffff; }
      .cell.plant  { background: #f0fdf4; }
      .cell.water  { background: #eff6ff; }
      .cell.fert   { background: #fdf4ff; }
      .cell.rem    { background: #fff1f2; }
      .emo { display:inline-block; font-size: 32px; line-height: 1; transform: translateY(2px); }
      .subtle { color:#64748b; }
      .card { border:1px solid #e5e7eb; border-radius: 14px; padding: 12px 14px; background: #ffffffc0; }
      .card h4{ margin: 0 0 8px 0; color:#0f172a; }
      .chip{ display:inline-block; padding:4px 10px; border-radius:999px; background:#eef2ff; color:#3730a3; font-weight:700; font-size:12px; margin-right:6px; margin-bottom:6px;}
      .callout{ border-left:4px solid #22c55e; background:#ecfdf5; padding:10px 12px; border-radius:12px;}
      .hero{ margin: 4px 0 12px; border-radius: 16px; padding: 14px 16px; color:#0f172a; background: linear-gradient(90deg,#f0fdf4,#ecfeff,#fff7ed); box-shadow: inset 0 0 0 1px #e5e7eb; }
      .hero-title{ font-size: 20px; font-weight: 800;}
      .meta{ font-size:12px; color:#475569;}
      .bg-floaters{ position: fixed; inset: 0; pointer-events:none; z-index:0; }
      .flo{ position:absolute; opacity:.10; animation: floaty 7s ease-in-out infinite; }
      .flo-1{ top:5%; left:5%; font-size:72px; animation-delay: 0s;}
      .flo-2{ top:10%; right:8%; font-size:68px; animation-delay: .6s;}
      .flo-3{ bottom:8%; left:6%; font-size:74px; animation-delay: 1.1s;}
      .flo-4{ bottom:12%; right:12%; font-size:70px; animation-delay: 1.6s;}
      .legend{ margin-bottom:8px;}
    </style>
    """,
    unsafe_allow_html=True,
)
# background floaters
st.markdown(
    f"""
<div class='bg-floaters'>
  <div class='flo flo-1'>🌱</div>
  <div class='flo flo-2'>💧</div>
  <div class='flo flo-3'>🌼</div>
  <div class='flo flo-4'>🧹</div>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================
# Data structures
# ==========================
@dataclass
class Tile:
    plant: bool
    watered: bool
    fertilized: bool
    removed: bool

@dataclass
class Step:
    title: str
    description: List[str]
    starter: str
    hint: str
    setup: Callable[[int], List[Tile]]
    validator: Callable[[List[Tile], int], Tuple[bool, str]]  # may read st.session_state['last_ns']

@dataclass
class Level:
    id: str
    title: str
    size: int
    show_grid: bool
    steps: List[Step]

# ==========================
# Emoji (single skin)
# ==========================
EMPTY = "⬜"
PLANT = "🌱"
WATER = "💧"
FERTILIZED = "🌼"
REMOVED = "🧹"  # broom fits the "remove weed" metaphor
OK = "✅"
NO = "🚫"
SPARKLE = "✨"
WITHER = "🥀"

# ==========================
# Helpers
# ==========================

def make_grid(N:int, *, plant_default=True) -> List[Tile]:
    return [Tile(plant=plant_default, watered=False, fertilized=False, removed=False) for _ in range(N*N)]

def symbol_for_tile(t: Tile) -> Tuple[str,str]:
    # returns (emoji, class)
    if t.removed:
        return REMOVED, "rem"
    if t.fertilized:
        return FERTILIZED, "fert"
    if t.watered:
        return WATER, "water"
    if t.plant:
        return PLANT, "plant"
    return EMPTY, "empty"

# 2D grid renderer with axis labels + tooltips

def draw_grid_html(grid: List[Tile], N:int) -> None:
    header_cells = ''.join([f'<th class="hdr">{c}</th>' for c in range(N)])
    rows_html = []
    for r in range(N):
        cells = []
        for c in range(N):
            idx = r*N + c
            emo, cls = symbol_for_tile(grid[idx])
            tip = f"r{r},c{c} • idx {idx}"
            cells.append(f'<td class="cell {cls}" title="{tip}"><span class="emo">{emo}</span></td>')
        row_html = f'<tr><th class="hdr">{r}</th>' + ''.join(cells) + '</tr>'
        rows_html.append(row_html)

    table_html = f'''
    <table class="garden">
      <thead>
        <tr>
          <th class="hdr"></th>
          {header_cells}
        </tr>
      </thead>
      <tbody>
        {''.join(rows_html)}
      </tbody>
    </table>
    '''
    st.markdown(table_html, unsafe_allow_html=True)

# Level 1 visual panels (no 2D grid table)

def draw_basics_panel(step_title:str, N:int):
    ns = st.session_state.get("last_ns", {})

    if "Booleans" in step_title:
        is_planted   = bool(ns.get("is_planted", False))
        is_watered   = bool(ns.get("is_watered", False))
        is_fertilized= bool(ns.get("is_fertilized", False))
        st.markdown("<h4>Plant states</h4>", unsafe_allow_html=True)
        st.markdown(f"**Plant:**  <span class='big-emo'>{PLANT if is_planted else EMPTY}</span>", unsafe_allow_html=True)
        st.markdown(f"**Water:**  <span class='big-emo'>{WATER if is_watered else NO}</span>",   unsafe_allow_html=True)
        st.markdown(f"**Fertilizer:**  <span class='big-emo'>{FERTILIZED if is_fertilized else NO}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif "Numbers" in step_title:
        pots = ns.get("pots", 0)
        dpp  = ns.get("drops_per_pot", 0)
        total = ns.get("total_drops", 0)
        st.markdown("<h4>Counting water</h4>", unsafe_allow_html=True)
        st.markdown("**Pots:**  " + "".join([f"<span class='big-emo'>{PLANT}</span>" for _ in range(int(pots) if isinstance(pots,int) else 0)]), unsafe_allow_html=True)
        st.markdown("**Drops per pot:**  " + "".join([f"<span class='big-emo'>{WATER}</span>" for _ in range(int(dpp) if isinstance(dpp,int) else 0)]), unsafe_allow_html=True)
        st.markdown(f"**Total drops:** {total}")
        st.markdown("</div>", unsafe_allow_html=True)

    elif "Comparisons" in step_title:
        has_water = bool(ns.get("has_water", False))
        is_weed   = bool(ns.get("is_weed", False))
        is_alive  = bool(ns.get("is_alive", False))
        plant_emo = PLANT if is_alive else WITHER
        water_emo = WATER if has_water else NO
        weed_emo  = REMOVED if is_weed else OK

        st.markdown("<h4>Alive or not?</h4>", unsafe_allow_html=True)
        st.markdown(f"**Status:** <span class='big-emo'>{plant_emo}</span> {SPARKLE if is_alive else ''}", unsafe_allow_html=True)
        st.markdown(f"**Water:** <span class='big-emo'>{water_emo}</span>", unsafe_allow_html=True)
        st.markdown(f"**Weed present:** <span class='big-emo'>{weed_emo}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif "Lists (1D" in step_title:
        row_cells = []
        for c in range(N):
            t = st.session_state.grid[c]
            emo, _ = symbol_for_tile(t)
            row_cells.append(emo)
        st.markdown("<h4>Pot strip</h4>", unsafe_allow_html=True)
        st.markdown("".join([f"<span class='big-emo'>{s}</span>" for s in row_cells]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# Sandbox API (water/fertilize/remove/get)
# ==========================

def grid_api_factory():
    def water(i:int):
        if 0 <= i < len(st.session_state.grid):
            t = st.session_state.grid[i]
            st.session_state.grid[i] = Tile(plant=t.plant, watered=True, fertilized=t.fertilized, removed=t.removed)
    def fertilize(i:int):
        if 0 <= i < len(st.session_state.grid):
            t = st.session_state.grid[i]
            st.session_state.grid[i] = Tile(plant=t.plant, watered=t.watered, fertilized=True, removed=t.removed)
    def remove(i:int):
        if 0 <= i < len(st.session_state.grid):
            t = st.session_state.grid[i]
            st.session_state.grid[i] = Tile(plant=t.plant, watered=t.watered, fertilized=t.fertilized, removed=True)
    def get(i:int):
        if 0 <= i < len(st.session_state.grid):
            t = st.session_state.grid[i]
            return {"plant": t.plant, "watered": t.watered, "fertilized": t.fertilized, "removed": t.removed}
        return {"plant": False, "watered": False, "fertilized": False, "removed": False}
    return water, fertilize, remove, get

# Safe builtins (block imports, I/O, eval, etc.)
import builtins as _bi
_ALLOWED_BUILTINS = (
    "ArithmeticError","AssertionError","AttributeError","BaseException","Exception","False","True","None",
    "abs","all","any","bool","bytes","callable","chr","complex","dict","dir","divmod","enumerate",
    "filter","float","format","frozenset","getattr","hasattr","hash","help","hex","id","int","isinstance",
    "issubclass","iter","len","list","map","max","min","next","object","oct","ord","pow","print","range",
    "repr","reversed","round","set","slice","sorted","str","sum","tuple","type","zip"
)
SAFE_BUILTINS = {k: getattr(_bi, k) for k in _ALLOWED_BUILTINS if hasattr(_bi, k)}

def _blocked(*a, **k):
    raise RuntimeError("Not allowed in this sandbox")
for bad in ("__import__","open","exec","eval","compile","globals","locals","__build_class__","input"):
    SAFE_BUILTINS[bad] = _blocked


def run_user_code(user_code:str, level:Level, step:Step) -> Tuple[bool, str, str]:
    # Reset grid to step setup before execution
    st.session_state.grid = step.setup(level.size)
    water, fertilize, remove, get = grid_api_factory()

    g = {"__builtins__": SAFE_BUILTINS,
         "water": water, "fertilize": fertilize, "remove": remove, "get": get,
         "N": level.size}
    loc: Dict[str, object] = {}

    if "import" in user_code:
        return False, "", "Imports are disabled in this sandbox"

    try:
        exec(user_code, g, loc)
        st.session_state["last_ns"] = {**g, **loc}
        ok, message = step.validator(st.session_state.grid, level.size)
        return ok, "", message
    except Exception as e:
        return False, str(e), "There was an error in your code."

# Success chime (tiny sine tone)

def success_wav(f=880.0, secs=0.25, vol=0.35, rate=16000):
    n = int(secs*rate)
    data = array('h', (int(vol*32767*math.sin(2*math.pi*f*t/rate)) for t in range(n)))
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(data.tobytes())
    return buf.getvalue()

# ==========================
# Levels & Steps
# ==========================
LEVELS: List[Level] = [
    # -------- Level 1: Basics (emoji visuals, no 2D grid table) --------
    Level(
        id="1",
        title="Python Basics",
        size=5,
        show_grid=False,
        steps=[
            Step(
                title="Booleans (plant states)",
                description=["Set plant state booleans.", "Make: is_planted=True, is_watered=False, is_fertilized=False."],
                starter=textwrap.dedent("""
                    is_planted = True
                    is_watered = False
                    is_fertilized = False
                """).strip(),
                hint="Use True/False (capitalized).",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        st.session_state.get("last_ns",{}).get("is_planted") is True and
                        st.session_state.get("last_ns",{}).get("is_watered") is False and
                        st.session_state.get("last_ns",{}).get("is_fertilized") is False
                    ),
                    "Great! Plant booleans look good." if (
                        st.session_state.get("last_ns",{}).get("is_planted") is True and
                        st.session_state.get("last_ns",{}).get("is_watered") is False and
                        st.session_state.get("last_ns",{}).get("is_fertilized") is False
                    ) else "Set is_planted=True, is_watered=False, is_fertilized=False."
                ),
            ),
            Step(
                title="Numbers & operations (watering)",
                description=["Create pots and water drop counts.", "Set: pots=3, drops_per_pot=2, total_drops=pots*drops_per_pot (6)."],
                starter=textwrap.dedent("""
                    pots = 3
                    drops_per_pot = 2
                    total_drops = pots * drops_per_pot
                """).strip(),
                hint="Use integers and * to multiply.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        st.session_state.get("last_ns",{}).get("pots") == 3 and
                        st.session_state.get("last_ns",{}).get("drops_per_pot") == 2 and
                        st.session_state.get("last_ns",{}).get("total_drops") == 6
                    ),
                    "Nice! total_drops = 6." if (
                        st.session_state.get("last_ns",{}).get("pots") == 3 and
                        st.session_state.get("last_ns",{}).get("drops_per_pot") == 2 and
                        st.session_state.get("last_ns",{}).get("total_drops") == 6
                    ) else "Define pots=3, drops_per_pot=2, total_drops=pots*drops_per_pot."
                ),
            ),
            Step(
                title="Comparisons & logic (alive?)",
                description=["Decide if a plant is alive.", "Make: has_water=True, is_weed=False, is_alive = has_water and not is_weed."],
                starter=textwrap.dedent("""
                    has_water = True
                    is_weed = False
                    is_alive = has_water and not is_weed
                """).strip(),
                hint="Combine booleans with and/or/not.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        st.session_state.get("last_ns",{}).get("has_water") is True and
                        st.session_state.get("last_ns",{}).get("is_weed") is False and
                        st.session_state.get("last_ns",{}).get("is_alive") is True
                    ),
                    "Logic looks good!" if (
                        st.session_state.get("last_ns",{}).get("has_water") is True and
                        st.session_state.get("last_ns",{}).get("is_weed") is False and
                        st.session_state.get("last_ns",{}).get("is_alive") is True
                    ) else "Set has_water=True, is_weed=False, then is_alive = has_water and not is_weed."
                ),
            ),
            Step(
                title="Lists (1D plants strip)",
                description=["Create a list for the first row pots and water them using a loop.", "Use indices=[0,1,2,3,4] then for i in indices: water(i)."],
                starter=textwrap.dedent("""
                    indices = [0, 1, 2, 3, 4]
                    for i in indices:
                        water(i)
                """).strip(),
                hint="indices=[0,1,2,3,4]; for i in indices: water(i)",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        all(state[0*N + c].watered for c in range(N)) and
                        all((not t.watered) for i,t in enumerate(state) if i//N!=0)
                    ),
                    "Great! First row watered via list." if (
                        all(state[0*N + c].watered for c in range(N)) and
                        all((not t.watered) for i,t in enumerate(state) if i//N!=0)
                    ) else "Only water the first row using your list."
                ),
            ),
        ],
    ),

    # -------- Level 2: Grid Challenges (shows grid) --------
    Level(
        id="2",
        title="Grid Challenges",
        size=5,
        show_grid=True,
        steps=[
            Step(
                title="Loops 101: water everything",
                description=["Use a for-loop to water every plant (25 tiles)."],
                starter=textwrap.dedent("""
                    for i in range(25):
                        water(i)
                """).strip(),
                hint="for i in range(25): water(i)",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (all((not t.plant) or (t.plant and t.watered) for t in state)),
                    "Nice! Every plant is watered." if (all((not t.plant) or (t.plant and t.watered) for t in state)) else "Some plants aren’t watered yet."
                ),
            ),
            Step(
                title="Selective watering",
                description=["Water only tiles that have a plant. Use get(i)['plant']."],
                starter=textwrap.dedent("""
                    for i in range(25):
                        if get(i)['plant']:
                            water(i)
                """).strip(),
                hint="if get(i)['plant']: water(i)",
                setup=lambda N: [Tile(plant=(i % 2 == 0), watered=False, fertilized=False, removed=False) for i in range(N*N)],
                validator=lambda state,N: (
                    (all((t.watered if t.plant else not t.watered) for t in state)),
                    "Perfect selective watering!" if (all((t.watered if t.plant else not t.watered) for t in state)) else "You watered an empty patch or missed a plant."
                ),
            ),
            Step(
                title="Index math: corners",
                description=["Fertilize only the four corners (0, N-1, N*(N-1), N*N-1)."],
                starter=textwrap.dedent("""
                    for i in (0, N-1, N*(N-1), N*N-1):
                        fertilize(i)
                """).strip(),
                hint="Use the formula for corners.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        all(state[i].fertilized for i in [0, N-1, N*(N-1), N*N-1]) and
                        all((i in [0, N-1, N*(N-1), N*N-1]) or (not t.fertilized) for i,t in enumerate(state))
                    ),
                    "Corner boost achieved!" if (
                        all(state[i].fertilized for i in [0, N-1, N*(N-1), N*N-1]) and
                        all((i in [0, N-1, N*(N-1), N*N-1]) or (not t.fertilized) for i,t in enumerate(state))
                    ) else "Fertilize only the corners."
                ),
            ),
            Step(
                title="While/conditionals: remove weeds",
                description=["Remove non-plant tiles so only plants remain."],
                starter=textwrap.dedent("""
                    for i in range(25):
                        if not get(i)['plant']:
                            remove(i)
                """).strip(),
                hint="if not get(i)['plant']: remove(i)",
                setup=lambda N: [Tile(plant=(i % 5 != 0), watered=False, fertilized=False, removed=False) for i in range(N*N)],
                validator=lambda state,N: (
                    (all((t.removed if not t.plant else True) for t in state)),
                    "Weed-free zone!" if (all((t.removed if not t.plant else True) for t in state)) else "Some weeds remain."
                ),
            ),
            Step(
                title="Functions & reuse: rows 1 and 3",
                description=["Write water_row(r) and water rows 1 and 3 only."],
                starter=textwrap.dedent("""
                    def water_row(r):
                        for c in range(5):
                            idx = r*5 + c
                            water(idx)

                    water_row(1)
                    water_row(3)
                """).strip(),
                hint="Define and call water_row(1) & (3)",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        all(state[1*5 + c].watered for c in range(5)) and
                        all(state[3*5 + c].watered for c in range(5)) and
                        all((t.watered is False) if (i//5 not in (1,3)) else True for i,t in enumerate(state))
                    ),
                    "Reusable functions for the win!" if (
                        all(state[1*5 + c].watered for c in range(5)) and
                        all(state[3*5 + c].watered for c in range(5)) and
                        all((t.watered is False) if (i//5 not in (1,3)) else True for i,t in enumerate(state))
                    ) else "Make sure you watered rows 1 and 3 only."
                ),
            ),
        ],
    ),
]

# ==========================
# Session state init
# ==========================
if "level_idx" not in st.session_state:
    st.session_state.level_idx = 0
if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0
if "grid" not in st.session_state:
    st.session_state.grid = LEVELS[0].steps[0].setup(LEVELS[0].size)
if "starter_cache" not in st.session_state:
    st.session_state.starter_cache: Dict[str, str] = {}

# ==========================
# Instruction renderer
# ==========================

def render_instructions(level: Level, step: Step):
    st.divider()
    st.markdown(f"<h4>📘 Instructions — {step.title}</h4>", unsafe_allow_html=True)
    for d in step.description:
        st.markdown(f"- {d}")
    if level.show_grid:
        st.markdown("<div class='callout'>💡 API: <span class='chip'>water(i)</span> <span class='chip'>fertilize(i)</span> <span class='chip'>remove(i)</span> <span class='chip'>get(i) → dict</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


with st.container():
    st.markdown("<div class='app-wrap'>", unsafe_allow_html=True)
st.markdown("<div class='hero'><div class='hero-title'>Grow Python skills by tending a garden</div><div class='meta'>Basics → 2D puzzles · variables • loops • conditionals • functions</div></div>", unsafe_allow_html=True)

st.markdown("# <span class='title-accent'>🪴 Python Garden</span>", unsafe_allow_html=True)
st.caption("Learn Python with Python Garden!")


# Level picker
level_labels = [f"Level {lv.id} — {lv.title}" for lv in LEVELS]
level_choice = st.selectbox("Choose a level", options=level_labels, index=st.session_state.level_idx)
new_level_idx = level_labels.index(level_choice)


level = LEVELS[new_level_idx]
step_labels = [f"Step {i+1}: {s.title}" for i,s in enumerate(level.steps)]
step_choice = st.selectbox("Step", options=step_labels, index=(0 if st.session_state.level_idx!=new_level_idx else st.session_state.step_idx))
new_step_idx = step_labels.index(step_choice)

# Persist selection
if new_level_idx != st.session_state.level_idx:
    st.session_state.level_idx = new_level_idx
    st.session_state.step_idx = 0
    st.session_state.grid = level.steps[0].setup(level.size)
else:
    st.session_state.level_idx = new_level_idx
    st.session_state.step_idx = new_step_idx

step = level.steps[st.session_state.step_idx]

# Progress within level
done = st.session_state.step_idx
total = len(level.steps)
st.progress((done+1)/total, text=f"Step {done+1}/{total}")
st.markdown(f"<span class='badge'>Level {level.id}</span> <span class='subtle'>— {level.title}</span>", unsafe_allow_html=True)

render_instructions(level, step)

N = level.size
grid = st.session_state.grid

if level.show_grid:
    st.markdown(f"<div class='legend'><span class='chip'>{PLANT} plant</span> <span class='chip'>{WATER} watered</span> <span class='chip'>{FERTILIZED} fertilized</span> <span class='chip'>{REMOVED} removed</span> <span class='chip'>{EMPTY} empty</span></div>", unsafe_allow_html=True)
    draw_grid_html(grid, N)
else:
    draw_basics_panel(step.title, N)
    st.caption("Level 1 uses emoji panels for variables and simple actions; Level 2 shows the full 2D grid.")


cache_key = f"code_L{st.session_state.level_idx}_S{st.session_state.step_idx}"
code_default = st.session_state.starter_cache.get(cache_key, step.starter)
user_code = st.text_area("Your Python code", value=code_default, height=240, key=cache_key)

colA, colB, colC, colD = st.columns(4)
with colA:
    run_clicked = st.button("▶ Run", use_container_width=True)
with colB:
    reset_clicked = st.button("↺ Reset", use_container_width=True)
with colC:
    prev_clicked = st.button("⬅ Prev", use_container_width=True, disabled=(st.session_state.step_idx==0))
with colD:
    next_clicked = st.button("Next ➡", use_container_width=True, disabled=(st.session_state.step_idx==len(level.steps)-1))

if reset_clicked:
    st.session_state.grid = step.setup(level.size)
    st.session_state.starter_cache[cache_key] = step.starter
    st.rerun()

if prev_clicked:
    st.session_state.step_idx = max(0, st.session_state.step_idx-1)
    st.rerun()

if next_clicked:
    st.session_state.step_idx = min(len(level.steps)-1, st.session_state.step_idx+1)
    st.rerun()

if run_clicked:
    st.session_state.starter_cache[cache_key] = user_code
    ok, err, msg = run_user_code(user_code, level, step)
    if err:
        st.error(err)
    if ok:
        st.audio(success_wav(), format="audio/wav")
        st.success(msg)
    else:
        st.info(msg)

with st.expander("Need a hint?", expanded=False):
    st.code(step.hint)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.markdown("baahan gpt dej baisnaa neree bicheed hha")
