"""Generate a 10-slide presentation matching the exact template, font, layout, and color scheme
of the demo presentation (StockWise), tailored for:
Task 35: Employee Ranking System
Student: Mani Chetan | PRN: 25070725016
Professor / Project Guide: Dr. Kranthi
Symbiosis Institute of Technology, Hyderabad
"""
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette precisely extracted from Demo PDF:
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BG_WHITE = RGBColor(255, 255, 255)
COLOR_DARK_BLOCK = RGBColor(24, 36, 43)        # Slate Navy from Slide 1 right block
COLOR_TEAL_PRIMARY = RGBColor(19, 122, 109)    # Deep Teal for titles, accents, borders (#137A6D)
COLOR_TEAL_LIGHT = RGBColor(235, 246, 244)      # Very pale teal tint for subtle card fills
COLOR_TEXT_MAIN = RGBColor(26, 32, 44)         # Deep black-charcoal for crisp readability (#1A202C)
COLOR_TEXT_MUTED = RGBColor(113, 128, 150)     # Gray for subtitles and descriptions (#718096)
COLOR_CARD_BORDER = RGBColor(226, 232, 240)    # Soft slate border for cards (#E2E8F0)
COLOR_CARD_BG = RGBColor(255, 255, 255)        # Pure white card background
COLOR_NUMBERING = RGBColor(160, 174, 192)      # Gray for "X / 10" slide numbers

FONT_FAMILY = "Segoe UI"


def create_base_slide(prs, slide_num=1):
    """Creates a slide with the signature left teal vertical bar and slide number."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_WHITE

    # Left vertical teal bar running down the entire slide
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.16), SLIDE_HEIGHT)
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_TEAL_PRIMARY
    bar.line.fill.background()

    # Slide numbering at bottom right: "X / 10"
    num_box = slide.shapes.add_textbox(Inches(12.0), Inches(7.05), Inches(1.1), Inches(0.35))
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.text = f"{slide_num} / 10"
    p_num.font.size = Pt(9.5)
    p_num.font.color.rgb = COLOR_NUMBERING
    p_num.font.name = FONT_FAMILY
    p_num.alignment = PP_ALIGN.RIGHT

    return slide


def add_slide_header(slide, title_text, subtitle_text):
    """Adds the clean title and gray subtitle matching the demo slides."""
    tb = slide.shapes.add_textbox(Inches(0.65), Inches(0.55), Inches(12.0), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True

    # Main Title
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_MAIN
    p_title.font.name = FONT_FAMILY

    # Subtitle
    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.font.name = FONT_FAMILY
    p_sub.space_before = Pt(6)


def add_demo_card(slide, left, top, width, height, title, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Adds a rounded card matching the demo's 3-card and 4-card layouts."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    # Title inside card
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL_PRIMARY
    p.font.name = FONT_FAMILY

    return card


# ==============================================================================
# SLIDE 1: COVER SLIDE (Identical to Demo Slide 1)
# ==============================================================================
def build_slide_1(prs):
    slide = create_base_slide(prs, 1)

    # Right-side dark navy-slate block (Width ~3.8 inches)
    dark_block = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(9.5), Inches(0), Inches(3.833), SLIDE_HEIGHT
    )
    dark_block.fill.solid()
    dark_block.fill.fore_color.rgb = COLOR_DARK_BLOCK
    dark_block.line.fill.background()

    # Inside dark block: Tagline and decorative wireframe icon
    tb_dark = slide.shapes.add_textbox(Inches(9.8), Inches(4.3), Inches(3.2), Inches(1.8))
    tf_d = tb_dark.text_frame
    tf_d.word_wrap = True

    p_d = tf_d.paragraphs[0]
    p_d.text = "RANKING,\nWITH PRECISION"
    p_d.font.size = Pt(16)
    p_d.font.bold = True
    p_d.font.color.rgb = COLOR_WHITE
    p_d.font.name = FONT_FAMILY
    p_d.alignment = PP_ALIGN.CENTER

    p_d2 = tf_d.add_paragraph()
    p_d2.text = "STABLE • DETERMINISTIC • O(N log N)"
    p_d2.font.size = Pt(8.5)
    p_d2.font.color.rgb = COLOR_TEAL_PRIMARY
    p_d2.font.name = FONT_FAMILY
    p_d2.alignment = PP_ALIGN.CENTER
    p_d2.space_before = Pt(8)

    # Decorative cube / rank icon in dark panel
    cube_box = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(10.6), Inches(2.6), Inches(1.6), Inches(1.6))
    cube_box.fill.solid()
    cube_box.fill.fore_color.rgb = COLOR_DARK_BLOCK
    cube_box.line.color.rgb = COLOR_TEAL_PRIMARY
    cube_box.line.width = Pt(2.5)

    # Left main content area
    tb_main = slide.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(8.4), Inches(4.8))
    tf_m = tb_main.text_frame
    tf_m.word_wrap = True

    # Big Brand / Project Name
    p_brand = tf_m.paragraphs[0]
    p_brand.text = "RANKWISE"
    p_brand.font.size = Pt(44)
    p_brand.font.bold = True
    p_brand.font.color.rgb = COLOR_TEXT_MAIN
    p_brand.font.name = FONT_FAMILY

    # Subtitle in Teal (like StockWise demo)
    p_title = tf_m.add_paragraph()
    p_title.text = "Employee Ranking System"
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEAL_PRIMARY
    p_title.font.name = FONT_FAMILY
    p_title.space_before = Pt(6)

    # Course tag
    p_course = tf_m.add_paragraph()
    p_course.text = "Data Structures & Algorithms – Lab Project (CA-2)"
    p_course.font.size = Pt(13)
    p_course.font.color.rgb = COLOR_TEXT_MUTED
    p_course.font.name = FONT_FAMILY
    p_course.space_before = Pt(28)

    # Student submission
    p_sub = tf_m.add_paragraph()
    p_sub.text = "Submitted by: Mani Chetan (PRN: 25070725016)"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = COLOR_TEXT_MAIN
    p_sub.font.name = FONT_FAMILY
    p_sub.space_before = Pt(36)

    # Project Guide & Department (Professor Name: Dr. Kranthi)
    p_dept = tf_m.add_paragraph()
    p_dept.text = "Project Guide: Dr. Kranthi\nCSE • Symbiosis Institute of Technology, Hyderabad"
    p_dept.font.size = Pt(10.5)
    p_dept.font.color.rgb = COLOR_TEXT_MUTED
    p_dept.font.name = FONT_FAMILY
    p_dept.space_before = Pt(4)


# ==============================================================================
# SLIDE 2: PROJECT OVERVIEW (3-Card Layout matching Demo Slide 2)
# ==============================================================================
def build_slide_2(prs):
    slide = create_base_slide(prs, 2)
    add_slide_header(
        slide,
        "Project Overview",
        "An algorithmic employee evaluation system for tracking, ranking, and merit appraisals"
    )

    card_w = Inches(3.7)
    card_h = Inches(4.2)
    top_pos = Inches(1.85)

    # Card 1: Purpose
    add_demo_card(slide, Inches(0.65), top_pos, card_w, card_h, "Purpose")
    tb1 = slide.shapes.add_textbox(Inches(0.85), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    bullets1 = [
        "Replace manual spreadsheets and biased evaluations with a rigorous algorithmic system.",
        "Rank personnel fairly based on performance, salary, and industry experience.",
        "Preserve preexisting order for employees sharing equal appraisal ratings (stability)."
    ]
    for idx, b in enumerate(bullets1):
        p = tf1.paragraphs[0] if idx == 0 else tf1.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(10)

    # Card 2: Core features
    add_demo_card(slide, Inches(4.6), top_pos, card_w, card_h, "Core features")
    tb2 = slide.shapes.add_textbox(Inches(4.8), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    bullets2 = [
        "Sort employees by Rating, Salary, Experience, or 100-point Composite Score.",
        "Real-time telemetry measuring execution time (µs), key comparisons, and data moves.",
        "Interactive Desktop GUI (Tkinter + Matplotlib) and ANSI Terminal CLI with CSV export."
    ]
    for idx, b in enumerate(bullets2):
        p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(10)

    # Card 3: Technology
    add_demo_card(slide, Inches(8.55), top_pos, card_w, card_h, "Technology")
    tb3 = slide.shapes.add_textbox(Inches(8.75), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    bullets3 = [
        "Python 3.13 & ANSI C99 implementation.",
        "Merge Sort (Best Engine), Quick Sort, Heap Sort, Insertion, Selection, Bubble Sort.",
        "Matplotlib visualizer for empirical O(N log N) vs O(N²) complexity curves."
    ]
    for idx, b in enumerate(bullets3):
        p = tf3.paragraphs[0] if idx == 0 else tf3.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(10)

    # Bottom summary text (matching Demo Slide 2)
    tb_bot = slide.shapes.add_textbox(Inches(0.65), Inches(6.25), Inches(11.6), Inches(0.65))
    tf_b = tb_bot.text_frame
    tf_b.word_wrap = True
    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "Dashboard shows ranked employees, appraisal ratings, salary distribution and runtime telemetry."
    p_b1.font.size = Pt(10)
    p_b1.font.color.rgb = COLOR_TEXT_MAIN
    p_b1.font.name = FONT_FAMILY

    p_b2 = tf_b.add_paragraph()
    p_b2.text = "Demonstrates real-world use of Data Structures and Algorithms."
    p_b2.font.size = Pt(10)
    p_b2.font.color.rgb = COLOR_TEXT_MUTED
    p_b2.font.name = FONT_FAMILY
    p_b2.space_before = Pt(2)


# ==============================================================================
# SLIDE 3: SYSTEM WORKFLOW (5-Step Pipeline with Arrows matching Demo Slide 3)
# ==============================================================================
def build_slide_3(prs):
    slide = create_base_slide(prs, 3)
    add_slide_header(
        slide,
        "System Workflow",
        "From loading employee data to multi-criteria sorting, telemetry analysis and reporting"
    )

    steps = [
        ("1. Input Data", "Load CSV roster or generate synthetic cohort (N = 25 to 2,000)"),
        ("2. Choose Metric", "Select criterion: Performance, Salary, Experience, or Composite"),
        ("3. Run Sorting", "Execute Merge Sort or comparative sorting algorithms"),
        ("4. Log Telemetry", "_SortTracker logs comparisons, moves, and microsecond runtime"),
        ("5. Output & Export", "Display ranked table with medal tags (#1, #2, #3) and export CSV"),
    ]

    card_w = Inches(2.15)
    card_h = Inches(4.0)
    top_pos = Inches(1.85)
    start_left = Inches(0.65)
    gap = Inches(0.3)

    for i, (title, desc) in enumerate(steps):
        left = start_left + i * (card_w + gap)
        add_demo_card(slide, left, top_pos, card_w, card_h, title)

        tb = slide.shapes.add_textbox(left + Inches(0.15), top_pos + Inches(0.7), card_w - Inches(0.3), card_h - Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(4)

        # Arrow indicator between cards
        if i < 4:
            arrow_left = left + card_w + Inches(0.06)
            tb_arr = slide.shapes.add_textbox(arrow_left, top_pos + Inches(1.7), Inches(0.2), Inches(0.4))
            tf_a = tb_arr.text_frame
            p_a = tf_a.paragraphs[0]
            p_a.text = "➔"
            p_a.font.size = Pt(14)
            p_a.font.color.rgb = COLOR_TEAL_PRIMARY

    # Bottom footer notes
    tb_bot = slide.shapes.add_textbox(Inches(0.65), Inches(6.25), Inches(11.6), Inches(0.65))
    tf_b = tb_bot.text_frame
    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "Stored records remain available for persistent querying across sorting criteria."
    p_b1.font.size = Pt(10)
    p_b1.font.color.rgb = COLOR_TEXT_MAIN
    p_b1.font.name = FONT_FAMILY

    p_b2 = tf_b.add_paragraph()
    p_b2.text = "Ranked employee records can be exported directly as a CSV file."
    p_b2.font.size = Pt(10)
    p_b2.font.color.rgb = COLOR_TEXT_MUTED
    p_b2.font.name = FONT_FAMILY
    p_b2.space_before = Pt(2)


# ==============================================================================
# SLIDE 4: SYSTEM MODULES (3-Card Layout matching Demo Slide 4)
# ==============================================================================
def build_slide_4(prs):
    slide = create_base_slide(prs, 4)
    add_slide_header(
        slide,
        "System Modules",
        "Each module handles a different part of the ranking and benchmarking architecture"
    )

    card_w = Inches(3.7)
    card_h = Inches(4.3)
    top_pos = Inches(1.85)

    # Module 1
    add_demo_card(slide, Inches(0.65), top_pos, card_w, card_h, "Core Sorting Module")
    tb1 = slide.shapes.add_textbox(Inches(0.85), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    bullets1 = [
        "Implements pure DSA sorting algorithms from scratch (core/sorting.py).",
        "Features Merge Sort, Quick Sort (Median-3), Heap Sort, Insertion, Selection, Bubble Sort.",
        "Integrates _SortTracker to count exact comparison operations and memory moves.",
        "Calculates execution runtime in microseconds and milliseconds."
    ]
    for idx, b in enumerate(bullets1):
        p = tf1.paragraphs[0] if idx == 0 else tf1.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(8)

    # Module 2
    add_demo_card(slide, Inches(4.6), top_pos, card_w, card_h, "Employee Data Model")
    tb2 = slide.shapes.add_textbox(Inches(4.8), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    bullets2 = [
        "Structured Employee entity (id, name, department, salary, experience, rating).",
        "Calculates 100-point Composite Score:",
        "  Score = (Norm_Perf * 0.50) + (Norm_Exp * 0.30) + (Norm_Salary * 0.20) * 100",
        "CSV persistence loader and synthetic cohort generator for up to 20,000 records."
    ]
    for idx, b in enumerate(bullets2):
        p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(8)

    # Module 3
    add_demo_card(slide, Inches(8.55), top_pos, card_w, card_h, "User Interface Modules")
    tb3 = slide.shapes.add_textbox(Inches(8.75), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    bullets3 = [
        "Tkinter Desktop GUI with directory tables and medal badges (#1 Gold, #2 Silver, #3 Bronze).",
        "Embedded Matplotlib visualizer showing live empirical complexity curves.",
        "Interactive ANSI terminal CLI menu for rapid viva demonstration.",
        "C99 Google Colab runnable engine for web-based live execution."
    ]
    for idx, b in enumerate(bullets3):
        p = tf3.paragraphs[0] if idx == 0 else tf3.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.space_before = Pt(8)


# ==============================================================================
# SLIDE 5: DATA STRUCTURES & ALGORITHMS USED (4-Card Layout matching Demo Slide 5)
# ==============================================================================
def build_slide_5(prs):
    slide = create_base_slide(prs, 5)
    add_slide_header(
        slide,
        "Data Structures & Algorithms Used",
        "Contiguous array buffers, binary heaps, and divide-and-conquer sorting algorithms"
    )

    card_w = Inches(2.75)
    card_h = Inches(4.6)
    top_pos = Inches(1.85)

    cards_info = [
        ("Dynamic Arrays", "Contiguous buffer", "Time: O(1) access", [
            "Contiguous memory list holding employee objects.",
            "Enables O(1) random-access indexing for pointer comparisons.",
            "Dynamically resizes during dataset generation.",
            "Efficient CPU cache line locality."
        ]),
        ("Binary Max-Heap", "Complete binary tree", "Time: O(N log N)", [
            "Mapped onto array: parent[i] >= child[2i+1], child[2i+2].",
            "Repeatedly extracts root to achieve in-place sorting.",
            "Zero auxiliary space overhead (Space: O(1)).",
            "Inherently unstable due to tree swaps."
        ]),
        ("Quick Sort", "Median-3 Partition", "Time: O(N log N) avg", [
            "In-place divide-and-conquer partition.",
            "Uses Median-of-Three pivot to avoid O(N²) degradation on sorted data.",
            "Performs minimal data copies.",
            "Unstable: scrambles equal appraisal keys."
        ]),
        ("Merge Sort", "Chosen Best Algorithm", "Time: O(N log N)", [
            "Divide-and-conquer binary halving.",
            "Guaranteed O(N log N) worst-case time bound in all scenarios.",
            "100% Stable: preserves order of equal rating scores (e.g. 4.8).",
            "Deterministic audit reproducibility."
        ]),
    ]

    for i, (title, sub, badge, bullets) in enumerate(cards_info):
        left = Inches(0.65) + i * (card_w + Inches(0.24))
        is_best = (i == 3)
        bg = COLOR_TEAL_LIGHT if is_best else COLOR_CARD_BG
        border = COLOR_TEAL_PRIMARY if is_best else COLOR_CARD_BORDER

        add_demo_card(slide, left, top_pos, card_w, card_h, title, bg_color=bg, border_color=border)

        tb = slide.shapes.add_textbox(left + Inches(0.15), top_pos + Inches(0.65), card_w - Inches(0.3), card_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        # Subtitle
        p_sub = tf.paragraphs[0]
        p_sub.text = sub
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.font.name = FONT_FAMILY

        # Complexity Badge
        p_badge = tf.add_paragraph()
        p_badge.text = badge
        p_badge.font.size = Pt(9.5)
        p_badge.font.bold = True
        p_badge.font.color.rgb = COLOR_TEAL_PRIMARY
        p_badge.font.name = FONT_FAMILY
        p_badge.space_before = Pt(4)

        # Bullets
        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.size = Pt(9)
            pb.font.color.rgb = COLOR_TEXT_MAIN
            pb.font.name = FONT_FAMILY
            pb.space_before = Pt(6)


# ==============================================================================
# SLIDE 6: APPLICATION SCREENS (Dual Image Layout matching Demo Slide 6)
# ==============================================================================
def build_slide_6(prs):
    slide = create_base_slide(prs, 6)
    add_slide_header(
        slide,
        "Desktop Application Screens",
        "Graphical interface and live performance benchmarking dashboard of RankWise"
    )

    card_w = Inches(5.7)
    card_h = Inches(4.4)
    top_pos = Inches(1.85)

    # Left Container: GUI Evidence
    add_demo_card(slide, Inches(0.65), top_pos, card_w, card_h, "Employee Directory & Ranking GUI")
    img_gui = os.path.join(os.getcwd(), "gui_ranking_evidence.png")
    if os.path.exists(img_gui):
        slide.shapes.add_picture(img_gui, Inches(0.8), top_pos + Inches(0.65), Inches(5.4), Inches(3.1))

    tb_cap1 = slide.shapes.add_textbox(Inches(0.8), top_pos + Inches(3.85), Inches(5.4), Inches(0.45))
    tf_c1 = tb_cap1.text_frame
    tf_c1.word_wrap = True
    p1 = tf_c1.paragraphs[0]
    p1.text = "Directory View – shows ranked employees, medal badges (#1, #2, #3) & live telemetry banner."
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = COLOR_TEXT_MUTED
    p1.font.name = FONT_FAMILY
    p1.alignment = PP_ALIGN.CENTER

    # Right Container: Benchmark Visualizer
    add_demo_card(slide, Inches(6.55), top_pos, card_w, card_h, "Live Complexity Benchmarking Curves")
    img_bench = os.path.join(os.getcwd(), "benchmark_complexity_curves.png")
    if os.path.exists(img_bench):
        slide.shapes.add_picture(img_bench, Inches(6.7), top_pos + Inches(0.65), Inches(5.4), Inches(3.1))

    tb_cap2 = slide.shapes.add_textbox(Inches(6.7), top_pos + Inches(3.85), Inches(5.4), Inches(0.45))
    tf_c2 = tb_cap2.text_frame
    tf_c2.word_wrap = True
    p2 = tf_c2.paragraphs[0]
    p2.text = "Benchmark View – empirical curves contrasting O(N log N) scaling against O(N²) quadratic curves."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.font.name = FONT_FAMILY
    p2.alignment = PP_ALIGN.CENTER


# ==============================================================================
# SLIDE 7: ALGORITHM PERFORMANCE COMPARISON (Detailed Benchmark Table + Justification)
# ==============================================================================
def build_slide_7(prs):
    slide = create_base_slide(prs, 7)
    add_slide_header(
        slide,
        "Algorithm Performance Comparison",
        "Empirical runtime, key comparisons, and stability validation on N = 1,000 records"
    )

    # Left: Empirical Benchmark Table Card
    card_w = Inches(6.8)
    card_h = Inches(4.5)
    add_demo_card(slide, Inches(0.65), Inches(1.85), card_w, card_h, "Empirical Benchmark Results (N = 1,000)")

    # Insert Table
    rows = 7
    cols = 6
    tbl_shape = slide.shapes.add_table(rows, cols, Inches(0.85), Inches(2.45), Inches(6.4), Inches(3.6))
    table = tbl_shape.table

    table.columns[0].width = Inches(1.6)  # Algorithm
    table.columns[1].width = Inches(0.9)  # Time (ms)
    table.columns[2].width = Inches(1.0)  # Comparisons
    table.columns[3].width = Inches(0.9)  # Moves
    table.columns[4].width = Inches(1.1)  # Complexity
    table.columns[5].width = Inches(0.9)  # Stability

    headers = ["Algorithm", "Time (ms)", "Comparisons", "Data Moves", "Complexity", "Stability"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_TEAL_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_WHITE
        p.font.name = FONT_FAMILY
        p.alignment = PP_ALIGN.CENTER

    data = [
        ("Merge Sort [BEST]", "2.81", "8,720", "19,944", "O(N log N)", "STABLE"),
        ("Quick Sort (Med-3)", "2.14", "10,240", "6,150", "O(N^2) worst", "UNSTABLE"),
        ("Heap Sort", "3.65", "16,842", "14,520", "O(N log N)", "UNSTABLE"),
        ("Insertion Sort", "18.40", "248,150", "249,149", "O(N^2) avg", "STABLE"),
        ("Selection Sort", "21.45", "499,500", "1,998", "O(N^2)", "UNSTABLE"),
        ("Bubble Sort", "34.10", "499,500", "496,210", "O(N^2)", "STABLE"),
    ]

    for i, row in enumerate(data):
        is_best = (i == 0)
        row_bg = COLOR_TEAL_LIGHT if is_best else (COLOR_WHITE if i % 2 == 1 else RGBColor(248, 250, 252))
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.name = FONT_FAMILY
            if is_best:
                p.font.bold = True
                p.font.color.rgb = COLOR_TEAL_PRIMARY if j == 0 or j == 5 else COLOR_TEXT_MAIN
            else:
                p.font.color.rgb = COLOR_TEXT_MAIN
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    # Right: Why Merge Sort is Chosen Card
    card_r_w = Inches(4.9)
    add_demo_card(slide, Inches(7.65), Inches(1.85), card_r_w, card_h, "Why Merge Sort is Optimal", bg_color=COLOR_TEAL_LIGHT, border_color=COLOR_TEAL_PRIMARY)
    tb_r = slide.shapes.add_textbox(Inches(7.85), Inches(2.45), card_r_w - Inches(0.4), card_h - Inches(0.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    reasons = [
        ("1. Mathematical Stability Guarantee",
         "When employees share identical appraisal ratings (e.g., 4.8), Merge Sort strictly preserves preexisting seniority/ID order. Unstable sorts (Quick/Heap) scramble equal records."),
        ("2. Invariant O(N log N) Runtime",
         "Recurrence T(N) = 2T(N/2) + O(N) guarantees Theta(N log N) via Master Theorem Case 2. Naive QuickSort degrades to O(N²) on duplicate-heavy rating scales."),
        ("3. Audit Compliance & Determinism",
         "HR appraisal decisions and financial bonuses require deterministic, reproducible execution. Auxiliary space of O(N) is trivial (<15 MB for 100k records).")
    ]
    for idx, (title, desc) in enumerate(reasons):
        p_t = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(10.5)
        p_t.font.color.rgb = COLOR_TEAL_PRIMARY
        p_t.font.name = FONT_FAMILY
        p_t.space_before = Pt(8) if idx > 0 else Pt(0)

        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = COLOR_TEXT_MAIN
        p_d.font.name = FONT_FAMILY
        p_d.space_before = Pt(2)


# ==============================================================================
# SLIDE 8: CONSOLE & COLAB DEMONSTRATION (4 Card Layout matching Demo Slide 8)
# ==============================================================================
def build_slide_8(prs):
    slide = create_base_slide(prs, 8)
    add_slide_header(
        slide,
        "Console & Colab Output Demonstration",
        "Menu-driven run of core DSA operations and Google Colab C99 execution"
    )

    card_w = Inches(5.6)
    card_h = Inches(2.2)

    positions = [
        (Inches(0.65), Inches(1.85), "1. Menu & Data Preview",
         "[EMP001] Aarav Sharma   | Dept: Engineering  | Salary: $135,000 | Rating: 4.8\n"
         "[EMP002] Priya Patel    | Dept: Data Science | Salary: $142,000 | Rating: 4.9\n"
         "[EMP003] Rohan Verma    | Dept: Product      | Salary: $115,000 | Rating: 4.2\n"
         "Loaded 25 corporate employee records into memory buffer."),
        (Inches(6.65), Inches(1.85), "2. Merge Sort by Rating (Top Ranks)",
         "Rank #1 [GOLD] : EMP002 Priya Patel    | Rating: 4.9 | Score: 70.4\n"
         "Rank #2 [SLVR] : EMP017 Dev Mukherjee  | Rating: 4.9 | Score: 83.8\n"
         "Rank #3 [BRNZ] : EMP001 Aarav Sharma   | Rating: 4.8 | Score: 70.5\n"
         "Rank #4        : EMP012 Rhea Desai     | Rating: 4.8 | Score: 65.4"),
        (Inches(0.65), Inches(4.3), "3. Sorting Telemetry Log",
         "Algorithm Used   : Merge Sort (Stable Engine)\n"
         "Records Sorted   : 25 employees\n"
         "Execution Time   : 0.124 ms (124.0 us)\n"
         "Comparisons: 88  | Data Movements: 104 | Stability: VERIFIED (100%)"),
        (Inches(6.65), Inches(4.3), "4. Google Colab C Execution",
         "!gcc -O2 -Wall employee_ranking.c -o employee_ranking && ./employee_ranking\n"
         "Benchmark N = 1,000:\n"
         "Merge Sort : 2.81 ms | Comparisons: 8,720  | STABLE [RECOMMENDED]\n"
         "Quick Sort : 2.14 ms | Comparisons: 10,240 | UNSTABLE"),
    ]

    for left, top, title, content in positions:
        add_demo_card(slide, left, top, card_w, card_h, title, bg_color=RGBColor(248, 250, 252))
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), card_w - Inches(0.4), card_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = content
        p.font.size = Pt(8.5)
        p.font.name = "Consolas"
        p.font.color.rgb = COLOR_TEXT_MAIN


# ==============================================================================
# SLIDE 9: APPLICATIONS & FUTURE SCOPE (2-Card Layout matching Demo Slide 9)
# ==============================================================================
def build_slide_9(prs):
    slide = create_base_slide(prs, 9)
    add_slide_header(
        slide,
        "Applications & Future Scope",
        "Where the ranking system applies and future technical enhancements"
    )

    card_w = Inches(5.7)
    card_h = Inches(4.4)
    top_pos = Inches(1.85)

    # Left: Applications
    add_demo_card(slide, Inches(0.65), top_pos, card_w, card_h, "Applications")
    tb1 = slide.shapes.add_textbox(Inches(0.85), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    apps = [
        ("Corporate HR Appraisal Systems: ", "Automating merit-based promotion pipelines, leadership allocations, and bonus pools."),
        ("Enterprise HRMS Platforms: ", "Core sorting integration for systems like Workday, SAP SuccessFactors, and Oracle HCM."),
        ("Academic Institution Grading: ", "Fair student performance ranking with GPA tie-breakers preserving roll number order."),
        ("Sales & Quota Leaderboards: ", "Real-time revenue generator rankings across corporate sales territories."),
        ("Audit Compliance & Payroll: ", "Deterministic data organization fulfilling stringent financial compliance audits.")
    ]
    for idx, (title, desc) in enumerate(apps):
        p = tf1.paragraphs[0] if idx == 0 else tf1.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL_PRIMARY
        r1.font.name = FONT_FAMILY

        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        r2.font.name = FONT_FAMILY
        p.space_before = Pt(8)

    # Right: Future enhancements
    add_demo_card(slide, Inches(6.55), top_pos, card_w, card_h, "Future enhancements")
    tb2 = slide.shapes.add_textbox(Inches(6.75), top_pos + Inches(0.7), card_w - Inches(0.4), card_h - Inches(0.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    enhancements = [
        ("Database Integration: ", "Connect PostgreSQL or MongoDB backends for enterprise scale."),
        ("External Merge Sort: ", "Implement chunk-based k-way external sorting for multi-gigabyte datasets exceeding RAM."),
        ("Parallel Multi-Threading: ", "Utilize multi-core CPU threads via OpenMP / multiprocessing for concurrent sublist sorting."),
        ("Role-Based Access Control: ", "Implement manager vs HR administrator permissions with encrypted compensation records."),
        ("Automated Appraisal Alerts: ", "Automated notifications for bottom-quartile performance counseling and promotion flags.")
    ]
    for idx, (title, desc) in enumerate(enhancements):
        p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEAL_PRIMARY
        r1.font.name = FONT_FAMILY

        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        r2.font.name = FONT_FAMILY
        p.space_before = Pt(8)


# ==============================================================================
# SLIDE 10: CONCLUSION & THANK YOU (Identical to Demo Slide 10)
# ==============================================================================
def build_slide_10(prs):
    slide = create_base_slide(prs, 10)

    # Title: Conclusion
    tb_title = slide.shapes.add_textbox(Inches(0.65), Inches(0.55), Inches(12.0), Inches(0.8))
    tf_t = tb_title.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "Conclusion"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_MAIN
    p_t.font.name = FONT_FAMILY

    # Centered Summary paragraph lines (matching Demo Slide 10)
    tb_summary = slide.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.9), Inches(2.6))
    tf_s = tb_summary.text_frame
    tf_s.word_wrap = True

    lines = [
        "Built RankWise, an Employee Ranking and Appraisal Management System.",
        "A multi-criteria data model evaluates employees by Performance, Salary, Experience, and Composite Score.",
        "Merge Sort was proven as the optimal algorithm due to mathematical stability and guaranteed O(N log N) time.",
        "The dashboard highlights top performers (#1, #2, #3), execution telemetry, and complexity curves.",
        "The project demonstrates practical DSA concepts and can be extended with databases and external sorting."
    ]
    for idx, line in enumerate(lines):
        p = tf_s.paragraphs[0] if idx == 0 else tf_s.add_paragraph()
        p.text = line
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.font.name = FONT_FAMILY
        p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(8)

    # Big "THANK YOU" in Teal (matching Demo Slide 10)
    tb_ty = slide.shapes.add_textbox(Inches(1.5), Inches(4.3), Inches(10.3), Inches(1.0))
    tf_ty = tb_ty.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU"
    p_ty.font.size = Pt(36)
    p_ty.font.bold = True
    p_ty.font.color.rgb = COLOR_TEAL_PRIMARY
    p_ty.font.name = FONT_FAMILY
    p_ty.alignment = PP_ALIGN.CENTER

    # Project guide & college line (Professor Name: Dr. Kranthi)
    tb_foot = slide.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.0))
    tf_f = tb_foot.text_frame
    tf_f.word_wrap = True

    p_f1 = tf_f.paragraphs[0]
    p_f1.text = "Submitted by: Mani Chetan (PRN: 25070725016)"
    p_f1.font.size = Pt(11)
    p_f1.font.bold = True
    p_f1.font.color.rgb = COLOR_TEXT_MAIN
    p_f1.font.name = FONT_FAMILY
    p_f1.alignment = PP_ALIGN.CENTER

    p_f2 = tf_f.add_paragraph()
    p_f2.text = "Project guide: Dr. Kranthi  •  Symbiosis Institute of Technology, Hyderabad"
    p_f2.font.size = Pt(11)
    p_f2.font.color.rgb = COLOR_TEXT_MUTED
    p_f2.font.name = FONT_FAMILY
    p_f2.alignment = PP_ALIGN.CENTER
    p_f2.space_before = Pt(4)

    p_f3 = tf_f.add_paragraph()
    p_f3.text = "GitHub: github.com/chetan-hub-bot/dsa-mini-project"
    p_f3.font.size = Pt(10)
    p_f3.font.color.rgb = COLOR_TEAL_PRIMARY
    p_f3.font.name = FONT_FAMILY
    p_f3.alignment = PP_ALIGN.CENTER
    p_f3.space_before = Pt(4)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building 10 slides matching demo template...")
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs)
    build_slide_9(prs)
    build_slide_10(prs)

    output_filename = "Employee_Ranking_System_DemoMatched.pptx"
    workspace_path = os.path.join(r"c:\Users\6tan5\OneDrive\Desktop\dsa mini project", output_filename)
    downloads_path = os.path.join(r"C:\Users\6tan5\Downloads", output_filename)

    prs.save(workspace_path)
    print(f"Saved matched presentation to workspace: {workspace_path}")

    try:
        prs.save(downloads_path)
        print(f"Saved matched presentation to Downloads: {downloads_path}")
    except Exception as e:
        print(f"Could not save to downloads: {e}")


if __name__ == "__main__":
    main()
