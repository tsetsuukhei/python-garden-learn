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
      
      .footer {text-align: center; fcolor:#475569; margin-bottom:6px;}
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
      .callout{ border-left:4px solid #22c55e; background:#ecfdf5; padding:10px 12px; border-radius:12px; margin: 8px 0;}
      .explain-box{ border-left:4px solid #3b82f6; background:#eff6ff; padding:12px 14px; border-radius:12px; margin: 12px 0;}
      .explain-box h5{ margin: 0 0 6px 0; color:#1e40af; font-size: 14px; font-weight: 700;}
      .explain-box p{ margin: 4px 0; color:#1e3a8a; font-size: 13px; line-height: 1.5;}
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
      .example-code{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:8px 10px; font-family:monospace; font-size:13px; margin:6px 0;}

      @media (prefers-color-scheme: dark) {
    .stApp {
        background: rgb(14, 17, 23);
    }

    .stMainBlockContainer {
        background: rgb(14, 17, 23);
        box-shadow: 0;
        color: #e2e8f0;
    }

    /* text */
    .lbl, .card h4, .hero-title { color: #e2e8f0; }
    .subtle, .meta { color: #94a3b8; }

    /* card & chips */
    .card { background:#1e293b; border-color:#334155; }
    .chip { background:#1e40af; color:#c7d2fe; }

    /* table */
    .garden { border-color:#334155; }
    .garden th, .garden td { border-color:#334155; }
    .garden th.hdr { background:#1e293b; color:#f1f5f9; }

    /* cells */
    .cell.empty { background:#1e293b; }
    .cell.plant { background:#064e3b; }
    .cell.water { background:#1e3a8a; }
    .cell.fert  { background:#581c87; }
    .cell.rem   { background:#7f1d1d; }

    /* code blocks */
    .example-code { background:#0b1220; border-color:#334155; color:#e5e7eb; }

    /* callouts */
    .callout { background:#052e16; border-left-color:#22c55e; }
    .explain-box { background:#0c4a6e; border-left-color:#3b82f6; }
    .explain-box h5, .explain-box p { color:#dbeafe; }

    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    explanation: str
    starter: str
    hint: str
    setup: Callable[[int], List[Tile]]
    validator: Callable[[List[Tile], int], Tuple[bool, str]]

@dataclass
class Level:
    id: str
    title: str
    size: int
    show_grid: bool
    steps: List[Step]

# ==========================
# Emoji
# ==========================
EMPTY = "⬜"
PLANT = "🌱"
WATER = "💧"
FERTILIZED = "🌼"
REMOVED = "🧹"
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
    if t.removed:
        return REMOVED, "rem"
    if t.fertilized:
        return FERTILIZED, "fert"
    if t.watered:
        return WATER, "water"
    if t.plant:
        return PLANT, "plant"
    return EMPTY, "empty"

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

def draw_basics_panel(step_title:str, N:int):
    ns = st.session_state.get("last_ns", {})

    if "Variables" in step_title:
        plant_name = ns.get("plant_name", "")
        st.markdown("<h4>Your plant</h4>", unsafe_allow_html=True)
        st.markdown(f"<span class='big-emo'>{PLANT}</span> **Name:** {plant_name if plant_name else '(not set)'}", unsafe_allow_html=True)

    elif "Booleans" in step_title:
        is_planted   = bool(ns.get("is_planted", False))
        is_watered   = bool(ns.get("is_watered", False))
        is_fertilized= bool(ns.get("is_fertilized", False))
        st.markdown("<h4>Plant states</h4>", unsafe_allow_html=True)
        st.markdown(f"**Plant:**  <span class='big-emo'>{PLANT if is_planted else EMPTY}</span>", unsafe_allow_html=True)
        st.markdown(f"**Water:**  <span class='big-emo'>{WATER if is_watered else NO}</span>",   unsafe_allow_html=True)
        st.markdown(f"**Fertilizer:**  <span class='big-emo'>{FERTILIZED if is_fertilized else NO}</span>", unsafe_allow_html=True)

    elif "Numbers" in step_title:
        pots = ns.get("pots", 0)
        dpp  = ns.get("drops_per_pot", 0)
        total = ns.get("total_drops", 0)
        st.markdown("<h4>Counting water</h4>", unsafe_allow_html=True)
        st.markdown("**Pots:**  " + "".join([f"<span class='big-emo'>{PLANT}</span>" for _ in range(int(pots) if isinstance(pots,int) else 0)]), unsafe_allow_html=True)
        st.markdown("**Drops per pot:**  " + "".join([f"<span class='big-emo'>{WATER}</span>" for _ in range(int(dpp) if isinstance(dpp,int) else 0)]), unsafe_allow_html=True)
        st.markdown(f"**Total drops:** {total}")

    elif "Comparisons" in step_title or "Conditionals" in step_title or "Logic" in step_title:
        has_water = bool(ns.get("has_water", False))
        is_weed   = bool(ns.get("is_weed", False))
        is_alive  = bool(ns.get("is_alive", False))
        needs_water = bool(ns.get("needs_water", False))
        is_dry = bool(ns.get("is_dry", False))
        has_enough = bool(ns.get("has_enough", False))
        
        plant_emo = PLANT if is_alive else WITHER
        water_emo = WATER if has_water else NO
        weed_emo  = REMOVED if is_weed else OK

        st.markdown("<h4>Plant status</h4>", unsafe_allow_html=True)
        if "is_alive" in ns:
            st.markdown(f"**Status:** <span class='big-emo'>{plant_emo}</span> {SPARKLE if is_alive else ''}", unsafe_allow_html=True)
        if "has_water" in ns:
            st.markdown(f"**Water:** <span class='big-emo'>{water_emo}</span>", unsafe_allow_html=True)
        if "is_weed" in ns:
            st.markdown(f"**Weed present:** <span class='big-emo'>{weed_emo}</span>", unsafe_allow_html=True)
        if "needs_water" in ns:
            st.markdown(f"**Needs water:** <span class='big-emo'>{WATER if needs_water else NO}</span>", unsafe_allow_html=True)
        if "has_enough" in ns:
            st.markdown(f"**Has enough water:** <span class='big-emo'>{OK if has_enough else NO}</span>", unsafe_allow_html=True)

    elif "Lists" in step_title or "range" in step_title or "loop" in step_title.lower():
        row_cells = []
        for c in range(N):
            t = st.session_state.grid[c]
            emo, _ = symbol_for_tile(t)
            row_cells.append(emo)
        st.markdown("<h4>Pot strip</h4>", unsafe_allow_html=True)
        st.markdown("".join([f"<span class='big-emo'>{s}</span>" for s in row_cells]), unsafe_allow_html=True)

# ==========================
# Sandbox API
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


# ==========================
# Levels & Steps
# ==========================
LEVELS: List[Level] = [
    Level(
        id="1",
        title="Суурь ойлголтууд",
        size=5,
        show_grid=False,
        steps=[
            Step(
                title="Ургамлаа нэрлэх (хувьсагч)",
                description=["Ургамлын нэрийг хувьсагчид хадгалах."],
                explanation="""<div class='explain-box'>
<h5>📚 Хувьсагч гэж юу вэ?</h5>
<p>Хувьсагч нь мэдээллийг хадгалах хайрцагтай адил. Пайтонд хувьсагч зарлахын тулд хувьсагчийнхаа нэрийг бичээд, араас нь <code>=</code> тэмдэгтийг ашиглан утга оноож өгдөг.</p>
<p><strong>Жишээ:</strong></p>
<div class='example-code'>my_age = 25<br>favorite_color = "blue"</div>
<p>Хувьсагчийн нэрэнд латин үсэг, цифр, доогуур зураас орж болно (my_variable_name). Гэвч хувьсагчийн нэр заавал үсгээр эхлэх ёстой.</p>
</div>""",
                starter=textwrap.dedent("""
                    # plant_name гэдэг хувьсагч зарлах
                    # Ургамалдаа Rosie гэж нэр өгөөрэй
                    ### КОДОО ЭНД БИЧНЭ ҮҮ ###
                """).strip(),
                hint='plant_name = "Rosie"',
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    "plant_name" in st.session_state.get("last_ns",{}) and isinstance(st.session_state.get("last_ns",{}).get("plant_name"), str),
                    "Ургамалдаа нэр амжилттай өгчээ!" if ("plant_name" in st.session_state.get("last_ns",{}) and isinstance(st.session_state.get("last_ns",{}).get("plant_name"), str)) else "Create a variable called plant_name with a text value."
                ),
            ),
            Step(
                title="Ургамлын төлөв (boolean)",
                description=["True болон False утгуудыг ашиглан ургамлын төлвийг тодорхойл."],
                explanation="""<div class='explain-box'>
<h5>📚 Boolean гэж юу вэ?</h5>
<p>Boolean нь тийм/үгүй эсвэл on/off гэсэн утгуудыг илэрхийлдэг дата төрөл юм. <code>True</code> утга нь 1-ийн тоо, <code>False</code> утга нь 0-ийн тоог илэрхийлдэг.</p>
<p><strong>Жишээ:</strong></p>
<div class='example-code'>is_sunny = True<br>is_raining = False</div>
<p>Boolean ашиглан ургамлын төлвийг тодорхойлж болно. Жишээлбэл ургамлаа усалсан эсэхээ тэмдэглэхийг хүсвэл <code>is_watered = True</code> гэж бичнэ.</p>
</div>""",
                starter=textwrap.dedent("""
                    # Rosie TO DO листээ тодорхойлж байна. Түүнд ургамлын төлвүүдээ хянахад нь туслаарай.
                    # is_planted нь үнэн, is_watered болон is_fertilized нь худал байх ёстой.
                    is_planted = 
                    is_watered = 
                    is_fertilized = 
                """).strip(),
                hint="True болон False (capitalized) утгуудыг хувьсагч бүрийн ард нь бичээрэй.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        st.session_state.get("last_ns",{}).get("is_planted") is True and
                        st.session_state.get("last_ns",{}).get("is_watered") is False and
                        st.session_state.get("last_ns",{}).get("is_fertilized") is False
                    ),
                    "Сайн байна!" if (
                        st.session_state.get("last_ns",{}).get("is_planted") is True and
                        st.session_state.get("last_ns",{}).get("is_watered") is False and
                        st.session_state.get("last_ns",{}).get("is_fertilized") is False
                    ) else "is_planted=True, is_watered=False, is_fertilized=False."
                ),
            ),
            Step(
                title="Ургамлаа усалъя (тоо болон арифметик үйлдлүүд)",
                description=["Арифметик үйлдлүүдийг ашиглан хэрэгцээтэй нийт усны дуслын тоог тооцоолох."],
                explanation="""<div class='explain-box'>
<h5>📚 Пайтон дээр хийж болох математик үйлдлүүд</h5>
<p>Пайтоныг энгийн тооны машин шиг ашиглаж болно:</p>
<div class='example-code'>
+ (нийлбэр): 5 + 3 → 8<br>
- (ялгавар): 10 - 4 → 6<br>
* (үржвэр): 3 * 4 → 12<br>
/ (хуваах): 15 / 3 → 5
</div>
<p>Тооцоололдоо хувьсагчдыг ашиглаж болно: хэрэв <code>x = 5</code> болон <code>y = 3</code> бол <code>z = x * y</code> нь <code>z = 15</code> болно.</p>
</div>""",
                starter=textwrap.dedent("""
                    # Нийт хэдэн усны дусал хэрэгтэйг тооцоол
                    pots = 3
                    drops_per_pot = 2
                    total_drops = 
                """).strip(),
                hint="Үржүүлэхдээ * тэмдэгтийг ашиглана. pots хувьсагчийг drops_per_pot хувьсагчаар үржүүлээрэй.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        st.session_state.get("last_ns",{}).get("pots") == 3 and
                        st.session_state.get("last_ns",{}).get("drops_per_pot") == 2 and
                        st.session_state.get("last_ns",{}).get("total_drops") == 6
                    ),
                    "Гайхалтай! Нийт = 6 дусал." if (
                        st.session_state.get("last_ns",{}).get("pots") == 3 and
                        st.session_state.get("last_ns",{}).get("drops_per_pot") == 2 and
                        st.session_state.get("last_ns",{}).get("total_drops") == 6
                    ) else "Set pots=3, drops_per_pot=2, and calculate total_drops."
                ),
            ),
            Step(
                title="Нөхцөл шалгах",
                description=["Харьцуулах үйлдлүүдийг ашиглан True эсвэл False эсэхийг шалгаарай."],
                explanation="""<div class='explain-box'>
<h5>📚 Харьцуулах үйлдлүүд</h5>
<p>Пайтон хэлэнд утгуудыг хооронд нь харьцуулж болдог. Эдгээр нь үргэлж <code>True</code> эсвэл <code>False</code> буцаадаг:</p>
<div class='example-code'>
== (тэнцүү эсэх): 5 == 5 → True<br>
!= (тэнцүү биш): 5 != 3 → True<br>
> (их): 7 > 5 → True<br>
< (бага): 3 < 5 → True<br>
>= (их эсвэл тэнцүү): 5 >= 5 → True
</div>
<p><strong>Жишээ:</strong> <code>has_enough_water = water_level >= 50</code></p>
</div>""",
                starter=textwrap.dedent("""
                    # Хангалттай их ус байгаа эсэхийг шалга
                    water_level = 75
                    minimum_needed = 50
                    has_enough = water_level >= minimum_needed
                """).strip(),
                hint=">= ашиглан water_level-ийг minimum_needed-тэй харьцуулна.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    st.session_state.get("last_ns",{}).get("has_enough") is True,
                    "Зөв!" if st.session_state.get("last_ns",{}).get("has_enough") is True else "Check if water_level is >= minimum_needed"
                ),
            ),
            Step(
                title="Логик үйлдлүүд",
                description=["'and', 'or', 'not' операторуудыг ашиглан логик утгуудыг нэгтгэнэ."],
                explanation="""<div class='explain-box'>
<h5>📚 Логик үйлдлүүд</h5>
<p>Олон төлвийг логик үйлдлүүд ашиглан нэгтгэнэ:</p>
<div class='example-code'>
<strong>and</strong>: аль аль нь True байх ёстой<br>
True and True → True<br>
True and False → False<br><br>
<strong>or</strong>: хамгийн багадаа нэг нь True байх ёстой<br>
True or False → True<br>
False or False → False<br><br>
<strong>not</strong>: утгыг эсрэгээр нь хувиргадаг<br>
not True → False<br>
not False → True
</div>
<p><strong>Жишээ:</strong> Ургамал нь устай AND хогийн ургамал биш бол амьд байна.</p>
</div>""",
                starter=textwrap.dedent("""
                    # Ургамал амьд эсэхийг шалга
                    has_water = True
                    is_weed = False
                    is_alive = has_water and not is_weed
                """).strip(),
                hint="Combine conditions: has_water and not is_weed",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        st.session_state.get("last_ns",{}).get("has_water") is True and
                        st.session_state.get("last_ns",{}).get("is_weed") is False and
                        st.session_state.get("last_ns",{}).get("is_alive") is True
                    ),
                    "Зөв!" if (
                        st.session_state.get("last_ns",{}).get("has_water") is True and
                        st.session_state.get("last_ns",{}).get("is_weed") is False and
                        st.session_state.get("last_ns",{}).get("is_alive") is True
                    ) else "'and' болон 'not' операторуудыг ашиглан нөхцлийг нэгтгэнэ."
                ),
            ),
            Step(
                title="Хэрэв...тэгвэл... (if/else нөхцөл)",
                description=["if/else нөхцөл ашиглан кодын гүйцэтгэлийг хянах."],
                explanation="""<div class='explain-box'>
<h5>📚 If нөхцөл</h5>
<p>If нөхцөл нь кодод шийдвэр гаргах боломжийг олгодог. If нөхцөл нь True үед дараах код ажиллана:</p>
<div class='example-code'>
temperature = 30<br>
if temperature > 25:<br>
&nbsp;&nbsp;&nbsp;&nbsp;message = "Халуун байна!"<br>
else:<br>
&nbsp;&nbsp;&nbsp;&nbsp;message = "Хүйтэн байна!"
</div>
<p><strong>Санамж:</strong> <code>if</code> болон <code>else</code> -ын дараах код урдаа инденттэй (хоосон зай) байх ёстой.</p>
</div>""",
                starter=textwrap.dedent("""
                    # Ургамал хуурай эсэхийг шалгаад, хуурай бол услаарай.
                    is_dry = True
                    
                    if is_dry:
                        needs_water = True
                    else:
                        needs_water = False
                """).strip(),
                hint="if-ийн дараа ажиллах ёстой код шинэ мөрнөөс, урдаа инденттэй байх ёстой. is_dry-ийг өөрчлөөд кодыг дахин ажиллуулж үзээрэй.",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    st.session_state.get("last_ns",{}).get("needs_water") is True,
                    "Сайн байна." if st.session_state.get("last_ns",{}).get("needs_water") is True else "is_dry=True болон needs_water-ыг зөв тохируулах."
                ),
            ),
            Step(
                title="Лист",
                description=["Хэд хэдэн утгыг нэг хувьсагчид хадгалах."],
                explanation="""<div class='explain-box'>
<h5>📚 Лист гэж юу вэ?</h5>
<p>Лист нь олон утгыг нэг хувьсагчид хадгалах боломжийг олгодог. Листийг дөрвөлжийн хаалт ашиглан үүсгэнэ:</p>
<div class='example-code'>
fruits = ["apple", "banana", "orange"]<br>
numbers = [1, 2, 3, 4, 5]<br>
mixed = [1, "hello", True]
</div>
<p>Листийн элементэд байршлаар нь хандах (0-ээс эхэлж дугаарлана):</p>
<div class='example-code'>
fruits[0] → "apple"<br>
fruits[1] → "banana"<br>
numbers[2] → 3
</div>
</div>""",
                starter=textwrap.dedent("""
                    # Ургамлуудын байрлалыг листэд хадгалах
                    # Байршлыг нь ашиглан бүх ургамлыг услаарай
                    positions = [0, 1, 2, 3, 4]
                    
                    water(positions[0])
                    water(positions[1])
                    water(positions[2])
                    water(positions[3])
                    water(positions[4])
                """).strip(),
                hint="positions[0], positions[1], гэх мэтчилэн элемент бүрт хандаарай",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    all(state[c].watered for c in range(N)),
                    "Сайн байна! Бүх ургамлыг усаллаа." if all(state[c].watered for c in range(N)) else "Листийг ашиглан бүх ургамлыг услаарай."
                ),
            ),
            Step(
                title="For-давталт",
                description=["Давталтыг автоматжуулахын тулд for-давталт ашигла."],
                explanation="""<div class='explain-box'>
                <h5>📚 For давталт</h5>
                <p>Кодыг гар аргаар давтахын оронд for давталт ашигладаг:</p>
                <div class='example-code'>
                numbers = [1, 2, 3]<br>
                for num in numbers:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;print(num)
                </div>
                <p>Энэ нь дэлгэцэд эхлээд 1, дараа нь 2, дараа нь 3-ыг хэвлэнэ. <code>num</code> хувьсагч нь жагсаалтаас нэг нэгээр утгыг авдаг.</p>
                <p><strong>Санамж:</strong> Давталт доторх код нь урдаа инденттэй (хоосон зай) байх ёстой!</p>
                </div>""",
                starter=textwrap.dedent("""
                    # Давталтыг ашиглан бүх ургамлыг услаарай
                    positions = [0, 1, 2, 3, 4]
                    
                    for pos in positions:
                        water(pos)
                """).strip(),
                hint="for pos in positions: гээд шинэ мөрнөөс зай аваад үйлдлээ бичээрэй",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    all(state[c].watered for c in range(N)),
                    "Сайн байна!" if all(state[c].watered for c in range(N)) else "for-давталт ашиглаарай"
                ),
            ),
            Step(
                title="range() функц",
                description=["range() функцийг тоонуудын дараалал үүсгэхэд ашиглагддаг."],
                explanation="""<div class='explain-box'>
                <h5>📚 range() функц</h5>
                <p><code>[0, 1, 2, 3, 4]</code> гэж бичихийн оронд <code>range()</code> функцийг ашиглан тоонуудыг үүсгэнэ:</p>
                <div class='example-code'>
                range(5) → 0, 1, 2, 3, 4<br>
                range(2, 7) → 2, 3, 4, 5, 6<br>
                range(0, 10, 2) → 0, 2, 4, 6, 8
                </div>
                <p><strong>Түгээмэл жишээ:</strong></p>
                <div class='example-code'>
                for i in range(5):<br>
                &nbsp;&nbsp;&nbsp;&nbsp;print(i)
                </div>
                <p>Энэ нь 0-4 хүртэлх тоонуудыг хэвлэнэ. Давталтуудын хувьд маш ашигтай!</p>
                </div>""",
                starter=textwrap.dedent("""
                    # Лист ашиглахын оронд range() функцийг ашиглаарай
                    # Бүх ургамлыг услаарай
                    for i in range(5):
                        water(i)
                """).strip(),
                hint="range(5) нь 0, 1, 2, 3, 4-ийг үүсгэнэ",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    all(state[c].watered for c in range(N)),
                    "Сайн байна! range() функцийг амжилттай ашиглалаа." if all(state[c].watered for c in range(N)) else "range(5)-ыг ашиглах"
                ),
            ),
        ],
    ),

    Level(
        id="2",
        title="Давталт ба нөхцөл",
        size=5,
        show_grid=True,
        steps=[
            Step(
                title="Бүгдийг усал!",
                description=["Цэцэрлэгийн бүх ургамлыг услаарай."],
                explanation="""<div class='explain-box'>
<h5>📚 Олон ургамлыг услах</h5>
<p>Манай цэцэрлэг нь 5×5 харьцаатай нийт 25 байрлалтай. Бүх байрлал нь 0-24 хүртэлх индексүүдтэй:</p>
<div class='example-code'>
0-р мөр: 0, 1, 2, 3, 4 индекс<br>
1-р мөр: 5, 6, 7, 8, 9 индекс<br>
2-р мөр: 10, 11, 12, 13, 14 индекс<br>
...бусад
</div>
<p>Бүх 25 байрлалыг услахын тулд давталтанд <code>range(25)</code> ашиглаарай!</p>
</div>""",
                starter=textwrap.dedent("""
                    # Бүх ургамлыг услаарай
                    for i ...:
                        water(i)
                """).strip(),
                hint="range(25) функцийг ашиглан 0-24 хүртэлх байршилд хандаарай",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    all(t.watered for t in state),
                    "Сайн байна! Бүх ургамал услагдлаа" if all(t.watered for t in state) else "Бүх ургамлыг услаарай."
                ),
            ),
            Step(
                title="Нөхцөлийн дагуу услах",
                description=["Зөвхөн ургамалтай нүдийг услаарай. Зарим нүднүүд хоосон байна!"],
                explanation="""<div class='explain-box'>
<h5>📚 Долоо хэмжиж нэг огтол</h5>
<p><code>get(i)</code> функцийг ашиглан тухайн нүдний төлвийг шалгана. Энэ нь dict буцаана:</p>
<div class='example-code'>
tile_info = get(0)<br>
# tile_info looks like:<br>
# {"plant": True, "watered": False, ...}
</div>
<p>Утгыг нь дөрвөлжийн хаалт ашиглан авна:</p>
<div class='example-code'>
if get(i)['plant']:<br>
&nbsp;&nbsp;&nbsp;&nbsp;water(i)  # Ургамал байвал усал
</div>
<p>Энэ нь хоосон газар услахаас сэргийлнэ!</p>
</div>""",
                starter=textwrap.dedent("""
                    # Water only tiles with plants
                    for i in range(25):
                        if get(i)['plant']:
                            water(i)
                """).strip(),
                hint="Check get(i)['plant'] before calling water(i)",
                setup=lambda N: [Tile(plant=(i % 2 == 0), watered=False, fertilized=False, removed=False) for i in range(N*N)],
                validator=lambda state,N: (
                    all((t.watered if t.plant else not t.watered) for t in state),
                    "Зөв!" if all((t.watered if t.plant else not t.watered) for t in state) else "Зөвхөн ургамалтай нүдийг услаарай."
                ),
            ),
            Step(
                title="Индексийн тооцоо",
                description=["Зөвхөн булангийн 4 ургамлыг бордоорой."],
                explanation="""<div class='explain-box'>
        <h5>📚 Байршлыг тооцоолох</h5>
        <p>5×5 торон (N=5)-д булангууд дараах байршилд байна:</p>
        <div class='example-code'>
        Зүүн дээд: 0<br>
        Баруун дээд: N-1 = 4<br>
        Зүүн доод: N*(N-1) = 5*4 = 20<br>
        Баруун доод: N*N-1 = 25-1 = 24
        </div>
        <p><code>N</code>-ийг тооцоололдоо ашиглаж болно шүү! <code>N=5</code> гээд аль хэдийн тодорхойлчихсон.</p>
        <p><strong>Зөвлөмж:</strong> tuple эсвэл лист: <code>(0, 4, 20, 24)</code></p>
        </div>""",
                starter=textwrap.dedent("""
                    # Дөрвөн буланг бордоорой
                    corners = (0, N-1, N*(N-1), N*N-1)
                    for i in corners:
                        fertilize(i)
                """).strip(),
                hint="булангууд = (0, N-1, N*(N-1), N*N-1)",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        all(state[i].fertilized for i in [0, N-1, N*(N-1), N*N-1]) and
                        all((i in [0, N-1, N*(N-1), N*N-1]) or (not t.fertilized) for i,t in enumerate(state))
                    ),
                    "Амжилттай!" if (
                        all(state[i].fertilized for i in [0, N-1, N*(N-1), N*N-1]) and
                        all((i in [0, N-1, N*(N-1), N*N-1]) or (not t.fertilized) for i,t in enumerate(state))
                    ) else "Зөвхөн дөрвөн буланг бордоорой."
                ),
            ),
            Step(
                title="Хоосон нүдийг арилгах",
                description=["Ургамалгүй нүднүүдийг арилга."],
                explanation="""<div class='explain-box'>
            <h5>📚 Нөхцөл ашиглан филтер хийх</h5>
            <p>Заримдаа та НӨХЦӨЛД ТААРДАГГҮЙ элементүүд дээр үйлдэл хийх шаардлагатай болдог. <code>not</code> ашигла:</p>
            <div class='example-code'>
            if not get(i)['plant']:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;remove(i)  # Ургамал байхгүй бол арилгах
            </div>
            <p><strong>Бүх байршлаар давталт хийж, нөхцөл нь таарвал үйлдэл хийнэ.</strong></p>
            </div>""",
                starter=textwrap.dedent("""
                    # хоосон нүдийг арилгах
                    for i in range(25):
                        if not get(i)['plant']:
                            remove(i)
                """).strip(),
                hint="'not get(i)['plant']'-ийг хоосон нүдийг олохдоо ашиглаарай",
                setup=lambda N: [Tile(plant=(i % 5 != 0), watered=False, fertilized=False, removed=False) for i in range(N*N)],
                validator=lambda state,N: (
                    all((t.removed if not t.plant else True) for t in state),
                    "Зөв байна!" if all((t.removed if not t.plant else True) for t in state) else "Ургамалгүй нүднүүдийг арилгах."
                ),
            ),
            Step(
                title="Функц тодорхойлох",
                description=["Дахин ашиглагдах боломжтой функц үүсгэж, 1 болон 3-р мөрүүдийг услаарай."],
                explanation="""<div class='explain-box'>
                <h5>📚 Функц тодорхойлох</h5>
                <p>Функц ашигласнаар бичсэн кодоо дахин ашиглах боломжтой. Функцийг<code>def</code> түлхүүр ашиглан тодорхойлно:</p>
                <div class='example-code'>
                def greet(name):<br>
                &nbsp;&nbsp;&nbsp;&nbsp;print("Hello " + name)<br><br>
                greet("Alice")  # Hello Alice гэж хэвлэнэ<br>
                greet("Bob")    # Hello Bob гэж хэвлэнэ
                </div>
                <p><strong>Мөрийн хувьд:</strong> r мөр нь r*N-ээс r*N + (N-1) нүднүүдийг агуулна</p>
                <div class='example-code'>
                Row 0: 0, 1, 2, 3, 4 (0*5 through 0*5+4)<br>
                Row 1: 5, 6, 7, 8, 9 (1*5 through 1*5+4)
                </div>
                </div>""",
                starter=textwrap.dedent("""
                    # Бүтэн мөр услах функц бичих
                    def water_row(r):
                        for c in range(N):
                            idx = r * N + c
                            water(idx)
                    
                    # Water rows 1 and 3
                    water_row(1)
                    water_row(3)
                """).strip(),
                hint="Calculate idx as r*N + c, where r is row and c is column",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    (
                        all(state[1*N + c].watered for c in range(N)) and
                        all(state[3*N + c].watered for c in range(N)) and
                        all((t.watered is False) if (i//N not in (1,3)) else True for i,t in enumerate(state))
                    ),
                    "Reusable functions for the win!" if (
                        all(state[1*N + c].watered for c in range(N)) and
                        all(state[3*N + c].watered for c in range(N)) and
                        all((t.watered is False) if (i//N not in (1,3)) else True for i,t in enumerate(state))
                    ) else "Water only rows 1 and 3 using your function."
                ),
            ),
            Step(
                title="Давхар давталт",
                description=["Ургамлуудыг шатрын хөлөг шиг услаарай."],
                explanation="""<div class='explain-box'>
<h5>📚 Давхар давталтаар 2D дүрс үүсгэх</h5>
<p>Хоёр давхар for-давталт (нэгийг нь мөрөнд, нөгөөг нь баганад) ашиглах:</p>
<div class='example-code'>
for row in range(N):<br>
&nbsp;&nbsp;&nbsp;&nbsp;for col in range(N):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;idx = row * N + col<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# idx-ээр ямар нэгэн юм хийх
</div>
<p><strong>Зөвлөмж:</strong> (row + col) тэгш тоо байх үед нүд нь бараан өнгөтэй байдаг:</p>
<div class='example-code'>
if (row + col) % 2 == 0:<br>
&nbsp;&nbsp;&nbsp;&nbsp;water(idx)
</div>
<p><code>%</code> үйлдэл нь үлдэгдлийг харуулдаг.</p>
</div>""",
                starter=textwrap.dedent("""
                    # Шатрын хөлөг шиг услах
                    for row in range(N):
                        for col in range(N):
                            idx = row * N + col
                            if (row + col) % 2 == 0:
                                water(idx)
                """).strip(),
                hint="(row + col) % 2 == 0 ашиглаарай",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    all(state[r*N + c].watered == ((r+c) % 2 == 0) for r in range(N) for c in range(N)),
                    "Маш сайн!" if all(state[r*N + c].watered == ((r+c) % 2 == 0) for r in range(N) for c in range(N)) else "(row+col) % 2 == 0 ашиглан шатрын хөлөг шиг услах."
                ),
            ),
            Step(
                title="Хүрээг услах",
                description=["Талбайн захын ургамлууд буюу хүрээг услаарай."],
                explanation="""<div class='explain-box'>
<h5>📚 Ирмэг илрүүлэх</h5>
<p>Хэрэв нүд нь анхны/сүүлийн мөрөнд эсвэл анхны/сүүлийн баганад байвал тэр нь захынх гэж үзнэ:</p>
<div class='example-code'>
is_edge = (row == 0 or row == N-1 or col == 0 or col == N-1)
</div>
<p>Энэ нь дараах байдлаар задрах болно:</p>
<div class='example-code'>
row == 0        # Дээд зах<br>
row == N-1      # Доод зах<br>
col == 0        # Зүүн зах<br>
col == N-1      # Баруун зах
</div>
<p><code>or</code> ашиглан нэгтгээрэй. Зөвхөн нэг нь үнэн байх ёстой!</p>
</div>""",
                starter=textwrap.dedent("""
                    # Хүрээний ургамлуудыг услаарай
                    for row in range(N):
                        for col in range(N):
                            idx = row * N + col
                            is_edge = (row == 0 or row == N-1 or 
                                       col == 0 or col == N-1)
                            if is_edge:
                                water(idx)
                """).strip(),
                hint="row эсвэл col 0 эсвэл N-1-тэй тэнцүү байна",
                setup=lambda N: make_grid(N, plant_default=True),
                validator=lambda state,N: (
                    all(state[r*N + c].watered == (r == 0 or r == N-1 or c == 0 or c == N-1) for r in range(N) for c in range(N)),
                    "Гайхалтай!" if all(state[r*N + c].watered == (r == 0 or r == N-1 or c == 0 or c == N-1) for r in range(N) for c in range(N)) else "Талбайн захын ургамлуудыг услаарай."
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
    st.markdown(f"<h4>📘 Заавар — {step.title}</h4>", unsafe_allow_html=True)
    for d in step.description:
        st.markdown(f"- {d}")
    
    # Show explanation box
    st.markdown(step.explanation, unsafe_allow_html=True)
    
    if level.show_grid:
        st.markdown("<div class='callout'>💡 <strong>Ашиглах бэлэн функцууд:</strong> <span class='chip'>water(i)</span> <span class='chip'>fertilize(i)</span> <span class='chip'>remove(i)</span> <span class='chip'>get(i) → dict</span></div>", unsafe_allow_html=True)


with st.container():
    st.markdown("<div class='app-wrap'>", unsafe_allow_html=True)

st.markdown("# 🪴 Python Garden", unsafe_allow_html=True)
st.caption("Python ашиглаж цэцэрлэгээ тохижуулцгаая! 🌱")

# ===== 0) NAV QUEUE: apply button-driven changes BEFORE widgets render =====
# (Buttons set 'pending_step' then st.rerun(); we consume it here.)
if "pending_step" in st.session_state:
    tgt = int(st.session_state.pending_step)
    st.session_state.step_idx = tgt
    st.session_state.sb_step_idx = tgt  # safe here (before widget)
    del st.session_state["pending_step"]

if "pending_level" in st.session_state:
    L = int(st.session_state.pending_level)
    st.session_state.level_idx = L
    st.session_state.sb_level_idx = L
    # when level changes, reset step
    st.session_state.step_idx = 0
    st.session_state.sb_step_idx = 0
    del st.session_state["pending_level"]

# ===== 1) INIT sensible defaults =====
if "level_idx" not in st.session_state:
    st.session_state.level_idx = 0
if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0
if "sb_level_idx" not in st.session_state:
    st.session_state.sb_level_idx = st.session_state.level_idx
if "sb_step_idx" not in st.session_state:
    st.session_state.sb_step_idx = st.session_state.step_idx

# ===== 2) CALLBACKS for sidebar widgets =====
def _on_level_change():
    # keep indices mirrored, reset step to 0 on level change
    st.session_state.level_idx = st.session_state.sb_level_idx
    st.session_state.step_idx = 0
    st.session_state.sb_step_idx = 0

def _on_step_change():
    st.session_state.step_idx = st.session_state.sb_step_idx

# ===== 3) SIDEBAR (indices under the hood, label-only UI) =====
with st.sidebar:
    level_options = list(range(len(LEVELS)))
    sb_level_idx = st.selectbox(
        "Түвшин",
        options=level_options,
        index=st.session_state.sb_level_idx,
        format_func=lambda i: LEVELS[i].title,
        key="sb_level_idx",
        on_change=_on_level_change,
    )

    level_for_steps = LEVELS[st.session_state.level_idx]  # after _on_level_change
    step_options = list(range(len(level_for_steps.steps)))
    sb_step_idx = st.selectbox(
        "Алхам",
        options=step_options,
        index=st.session_state.sb_step_idx,
        format_func=lambda i: level_for_steps.steps[i].title,
        key="sb_step_idx",
        on_change=_on_step_change,
    )

# ===== 4) USE current level/step =====
level = LEVELS[st.session_state.level_idx]
step  = level.steps[st.session_state.step_idx]

# (re)build grid if needed (optional guard)
cur_key = f"L{st.session_state.level_idx}-S{st.session_state.step_idx}"
if st.session_state.get("loaded_key") != cur_key:
    st.session_state.grid = step.setup(level.size)
    st.session_state["loaded_key"] = cur_key
    st.session_state.pop("last_ns", None)



_cur_key = f"L{st.session_state.level_idx}-S{st.session_state.step_idx}"
if st.session_state.get("loaded_key") != _cur_key:
    st.session_state.grid = level.steps[st.session_state.step_idx].setup(level.size)
    st.session_state["loaded_key"] = _cur_key
    # Clear previous variables panel state so basics visuals don't leak across steps
    st.session_state.pop("last_ns", None)


done = st.session_state.step_idx
total = len(level.steps)
st.markdown(f"<span class='badge'>Түвшин {level.id}</span> <span class='subtle'>— {level.title}</span>", unsafe_allow_html=True)
st.progress((done+1)/total, text=f"Алхам {done+1}/{total}")


render_instructions(level, step)

N = level.size
grid = st.session_state.grid

if level.show_grid:
    st.markdown(f"<div class='legend'><span class='chip'>{PLANT} plant</span> <span class='chip'>{WATER} watered</span> <span class='chip'>{FERTILIZED} fertilized</span> <span class='chip'>{REMOVED} removed</span> <span class='chip'>{EMPTY} empty</span></div>", unsafe_allow_html=True)
    draw_grid_html(grid, N)
else:
    draw_basics_panel(step.title, N)


cache_key = f"code_L{st.session_state.level_idx}_S{st.session_state.step_idx}"
code_default = st.session_state.starter_cache.get(cache_key, step.starter)
user_code = st.text_area("✍️ Кодоо энд бичээрэй", value=code_default, height=240, key=cache_key)

colA, colB, colC, colD = st.columns(4)
with colA:
    run_clicked = st.button("▶ Код ажиллуулах", use_container_width=True, type="primary")
with colB:
    reset_clicked = st.button("↺ Буцаах", use_container_width=True)
with colC:
    prev_clicked = st.button("⬅ Өмнөх", use_container_width=True, disabled=(st.session_state.step_idx==0))
with colD:
    next_clicked = st.button("Дараах ➡", use_container_width=True, disabled=(st.session_state.step_idx==len(level.steps)-1))

if reset_clicked:
    st.session_state.grid = step.setup(level.size)
    st.session_state.starter_cache[cache_key] = step.starter
    st.rerun()

if prev_clicked:
    st.session_state.pending_step = max(0, st.session_state.step_idx - 1)
    st.rerun()

if next_clicked:
    st.session_state.pending_step = min(len(level.steps) - 1, st.session_state.step_idx + 1)
    st.rerun()


DISPLAY = {'success': st.success, 'warning': st.warning, 'error': st.error, 'info': st.info}

if 'flash' in st.session_state:
    kind, text = st.session_state.pop('flash')
    DISPLAY.get(kind, st.info)(text)

if 'flash_hint' in st.session_state:
    st.info(st.session_state.pop('flash_hint'))


if run_clicked:
    st.session_state.starter_cache[cache_key] = user_code
    ok, err, msg = run_user_code(user_code, level, step)

    if err:
        st.session_state['flash'] = ('error', f"❌ Error: {err}")
    elif ok:
        st.session_state['flash'] = ('success', f"✅ {msg}")
        if st.session_state.step_idx < len(level.steps) - 1:
            st.session_state['flash_hint'] = "'Дараах ➡' дээр дарна уу!"
    else:
        st.session_state['flash'] = ('warning', f"💭 {msg}")

    st.rerun()


with st.expander("💡 Тусламж", expanded=False):
    st.code(step.hint, language="python")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>🌟 @cecuhe</div>", unsafe_allow_html=True)
