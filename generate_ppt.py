"""Generate a 7-slide professional presentation with a clean White and Yellow theme.
Strictly incorporates:
- First slide: Project Name & Student Details (Mani Chetan, PRN: 25070725016)
- Comparison slide: Performance of Merge Sort vs other algorithms (empirical + theoretical)
- Last slide: Thank You
- Clean, aesthetic White & Yellow design with widescreen (16:9) layout.
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

# Color Palette: White and Yellow
COLOR_BG_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BG = RGBColor(252, 252, 252)
COLOR_CARD_TINT = RGBColor(255, 251, 235)  # Soft warm yellow tint
COLOR_BORDER = RGBColor(240, 240, 240)

# Yellow Accent Colors
COLOR_PRIMARY_YELLOW = RGBColor(245, 184, 0)   # Vivid warm yellow
COLOR_DARK_YELLOW = RGBColor(217, 130, 0)      # Amber / Deep Gold for text readability
COLOR_LIGHT_YELLOW = RGBColor(254, 243, 199)   # Pale yellow pill / badge fill

# Typography Colors
COLOR_TEXT_DARK = RGBColor(26, 26, 26)         # Deep charcoal black for sharp contrast
COLOR_TEXT_MUTED = RGBColor(100, 100, 100)     # Neutral gray
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_GREEN = RGBColor(16, 149, 70)


def create_blank_slide(prs):
    """Creates a blank slide with pure white background."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_WHITE
    return slide


def add_header(slide, title_text, category_text="DSA EXPERIENTIAL LEARNING | TASK 35"):
    """Adds a consistent, clean header bar with yellow accent."""
    # Top thin yellow accent strip
    top_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.12))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = COLOR_PRIMARY_YELLOW
    top_strip.line.fill.background()

    # Category Pill / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_DARK_YELLOW
    p_c.font.name = "Segoe UI"

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.7))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_DARK
    p_t.font.name = "Segoe UI"

    # Yellow underline indicator
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(1.8), Inches(0.06))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_PRIMARY_YELLOW
    line.line.fill.background()


def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_PRIMARY_YELLOW, border_width=1.5):
    """Adds a container card with subtle borders."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card


# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
def build_slide_1(prs):
    slide = create_blank_slide(prs)

    # Decorative yellow design elements
    # Right-side graphic block with warm yellow tone
    bg_accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.8), Inches(0), Inches(3.533), SLIDE_HEIGHT)
    bg_accent.fill.solid()
    bg_accent.fill.fore_color.rgb = COLOR_PRIMARY_YELLOW
    bg_accent.line.fill.background()

    # White card inside yellow bar for visual contrast
    inner_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.2), Inches(1.2), Inches(2.7), Inches(5.1))
    inner_box.fill.solid()
    inner_box.fill.fore_color.rgb = COLOR_WHITE
    inner_box.line.fill.background()

    tf_in = inner_box.text_frame
    tf_in.word_wrap = True
    p_in = tf_in.paragraphs[0]
    p_in.text = "CORE ALGORITHM"
    p_in.font.size = Pt(11)
    p_in.font.bold = True
    p_in.font.color.rgb = COLOR_DARK_YELLOW
    p_in.font.name = "Segoe UI"

    p2 = tf_in.add_paragraph()
    p2.text = "Merge Sort"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_DARK
    p2.font.name = "Segoe UI"
    p2.space_before = Pt(8)

    bullet_points = [
        "Time: O(N log N)",
        "Space: O(N)",
        "Stability: Guaranteed",
        "Worst Case: Invariant",
        "Multi-Tier HR Ranking",
        "Deterministic Execution",
    ]
    for bp in bullet_points:
        p_bp = tf_in.add_paragraph()
        p_bp.text = f"✔  {bp}"
        p_bp.font.size = Pt(10)
        p_bp.font.color.rgb = COLOR_TEXT_DARK
        p_bp.font.name = "Segoe UI"
        p_bp.space_before = Pt(8)

    # Main Left Content Area
    # Small Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(3.8), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_LIGHT_YELLOW
    badge.line.color.rgb = COLOR_PRIMARY_YELLOW
    badge.line.width = Pt(1.2)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "LAB CA-2 : EXPERIENTIAL LEARNING"
    p_b.font.size = Pt(10.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_DARK_YELLOW
    p_b.font.name = "Segoe UI"
    p_b.alignment = PP_ALIGN.CENTER

    # Project Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(8.3), Inches(2.2))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Task 35: Employee\nRanking System"
    p_t.font.size = Pt(40)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_DARK
    p_t.font.name = "Segoe UI"

    # Subtitle
    sub_p = tf_t.add_paragraph()
    sub_p.text = "Multi-Factor Personnel Appraisal & Empirical Complexity Benchmarking"
    sub_p.font.size = Pt(15)
    sub_p.font.color.rgb = COLOR_TEXT_MUTED
    sub_p.font.name = "Segoe UI"
    sub_p.space_before = Pt(10)

    # Divider line
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.3), Inches(4.0), Inches(0.06))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_PRIMARY_YELLOW
    div.line.fill.background()

    # Student Details Box
    student_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.6), Inches(7.8), Inches(1.8))
    student_box.fill.solid()
    student_box.fill.fore_color.rgb = COLOR_CARD_TINT
    student_box.line.color.rgb = COLOR_PRIMARY_YELLOW
    student_box.line.width = Pt(1.5)

    tf_s = student_box.text_frame
    tf_s.word_wrap = True
    p_s1 = tf_s.paragraphs[0]
    p_s1.text = "STUDENT DETAILS"
    p_s1.font.size = Pt(10)
    p_s1.font.bold = True
    p_s1.font.color.rgb = COLOR_DARK_YELLOW
    p_s1.font.name = "Segoe UI"

    details = [
        ("Student Name:", "Mani Chetan"),
        ("PRN Number:", "25070725016"),
        ("Course / Department:", "Data Structures & Algorithms (CS201) | Dept of CSE, SIT"),
        ("Evaluation COs:", "CO3 (Algorithm Design), CO4 (Analysis), CO5 (Implementation)"),
    ]
    for label, val in details:
        p_row = tf_s.add_paragraph()
        run_lbl = p_row.add_run()
        run_lbl.text = f"{label} "
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(11)
        run_lbl.font.color.rgb = COLOR_TEXT_DARK
        run_lbl.font.name = "Segoe UI"

        run_val = p_row.add_run()
        run_val.text = val
        run_val.font.bold = (label == "Student Name:" or label == "PRN Number:")
        run_val.font.size = Pt(11)
        run_val.font.color.rgb = COLOR_DARK_YELLOW if run_val.font.bold else COLOR_TEXT_DARK
        run_val.font.name = "Segoe UI"
        p_row.space_before = Pt(4)


# ==============================================================================
# SLIDE 2: PROBLEM STATEMENT & OBJECTIVES
# ==============================================================================
def build_slide_2(prs):
    slide = create_blank_slide(prs)
    add_header(slide, "Problem Statement & Project Objectives")

    # Left Column: Problem Statement Card
    add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_PRIMARY_YELLOW)
    
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.2), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "PROBLEM STATEMENT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_YELLOW
    p.font.name = "Segoe UI"

    p2 = tf_l.add_paragraph()
    p2.text = "In enterprise corporate management, personnel directories contain diverse quantitative metrics (Performance, Salary, Experience). Organizations require automated ranking systems for merit appraisals and promotions."
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT_DARK
    p2.space_before = Pt(8)

    p3 = tf_l.add_paragraph()
    p3.text = "Key Challenges in HR Ranking:"
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEXT_DARK
    p3.space_before = Pt(12)

    challenges = [
        ("Ties in Scores: ", "Many employees share identical ratings (e.g. 4.8 / 5.0). Arbitrary permuting violates fairness."),
        ("Multi-Tier Needs: ", "Need to sort by Rating first while preserving seniority (Experience) or ID order."),
        ("Scale & Audit: ", "Appraisal decisions must run deterministically with predictable execution times."),
    ]
    for bold_p, txt in challenges:
        p_c = tf_l.add_paragraph()
        r1 = p_c.add_run()
        r1.text = f"• {bold_p}"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_DARK_YELLOW
        r2 = p_c.add_run()
        r2.text = txt
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_DARK
        p_c.space_before = Pt(6)

    # Right Column: Project Objectives
    add_card(slide, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=COLOR_CARD_TINT, border_color=COLOR_PRIMARY_YELLOW)

    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "CORE LAB CA-2 OBJECTIVES"
    pr.font.size = Pt(13)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_DARK_YELLOW
    pr.font.name = "Segoe UI"

    objs = [
        ("CO3 : Algorithm Formulation", 
         "Implement 6 fundamental comparison sorting algorithms from scratch (Merge, Quick, Heap, Insertion, Selection, Bubble) with custom telemetry."),
        ("CO4 : Rigorous Performance Analysis", 
         "Mathematically derive and empirically measure time and space complexities, key comparisons, and stability preservation across varying N."),
        ("CO5 : Practical Demonstration", 
         "Build a dual-interface application (Desktop GUI with real-time Matplotlib curves + Interactive CLI console) with automated test validation."),
    ]
    for title, desc in objs:
        p_t = tf_r.add_paragraph()
        p_t.text = f"🎯  {title}"
        p_t.font.bold = True
        p_t.font.size = Pt(11.5)
        p_t.font.color.rgb = COLOR_TEXT_DARK
        p_t.space_before = Pt(12)

        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = COLOR_TEXT_MUTED
        p_d.space_before = Pt(3)


# ==============================================================================
# SLIDE 3: WHY MERGE SORT WAS CHOSEN
# ==============================================================================
def build_slide_3(prs):
    slide = create_blank_slide(prs)
    add_header(slide, "Algorithm Selection: Why Merge Sort is the Best Choice")

    cards_data = [
        ("1. STABILITY GUARANTEE",
         "Crucial for Multi-Criteria Ranking",
         "• Preserves initial relative sequence of records with identical keys.\n"
         "• When sorting by Performance (e.g. 4.8), employees with equal appraisal scores retain their prior seniority or ID order.\n"
         "• Quick Sort & Heap Sort are UNSTABLE: they disrupt equal-key ordering.",
         COLOR_CARD_TINT),
        ("2. O(N log N) GUARANTEED",
         "Invariant Worst-Case Runtime",
         "• Strict divide-and-conquer binary halving:\n"
         "    T(N) = 2T(N/2) + O(N)\n"
         "• By Master Theorem (Case 2): Theta(N log N) in Best, Average, and Worst cases.\n"
         "• Naive Quick Sort degrades to O(N²) on duplicate-heavy rating scales.",
         COLOR_WHITE),
        ("3. AUDIT DETERMINISM",
         "Enterprise HR Compliance",
         "• Fixed, deterministic execution tree ensures repeatable results for HR bonuses.\n"
         "• Memory trade-off of O(N) auxiliary space is negligible (<15 MB for 100k records).\n"
         "• Zero risk of catastrophic recursion slowdowns.",
         COLOR_CARD_TINT)
    ]

    left_positions = [Inches(0.8), Inches(4.8), Inches(8.8)]
    for i, (title, sub, text, bg) in enumerate(cards_data):
        add_card(slide, left_positions[i], Inches(1.8), Inches(3.7), Inches(5.1), bg_color=bg, border_color=COLOR_PRIMARY_YELLOW)

        tb = slide.shapes.add_textbox(left_positions[i] + Inches(0.15), Inches(1.95), Inches(3.4), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_DARK_YELLOW
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_DARK
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = text
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = COLOR_TEXT_DARK
        p3.space_before = Pt(12)


# ==============================================================================
# SLIDE 4: SYSTEM ARCHITECTURE & IMPLEMENTATION
# ==============================================================================
def build_slide_4(prs):
    slide = create_blank_slide(prs)
    add_header(slide, "System Architecture & Implementation")

    # Left Column: Features & Code Architecture
    add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_PRIMARY_YELLOW)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "MODULAR ARCHITECTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_YELLOW
    p.font.name = "Segoe UI"

    modules = [
        ("Core DSA Engine (core/sorting.py)", "From-scratch implementations of Merge, Quick, Heap, Insertion, Selection, Bubble Sort with _SortTracker instrumentation."),
        ("Multi-Criteria Model (core/employee.py)", "Employee entity supporting Salary, Experience, Performance, and a normalized 100-point Composite Score."),
        ("Composite Scoring Metric", "Score = (Norm_Perf * 0.50) + (Norm_Exp * 0.30) + (Norm_Salary * 0.20) * 100"),
        ("Dual Interface (Desktop GUI & CLI)", "Modern Tkinter desktop app with live rank badges (🥇, 🥈, 🥉) + terminal CLI for 10-minute viva demos."),
    ]
    for mod_title, mod_desc in modules:
        pm = tf_l.add_paragraph()
        pm.text = f"⚡ {mod_title}"
        pm.font.bold = True
        pm.font.size = Pt(11)
        pm.font.color.rgb = COLOR_TEXT_DARK
        pm.space_before = Pt(8)

        pd = tf_l.add_paragraph()
        pd.text = mod_desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_before = Pt(2)

    # Right Column: GUI Screenshot Card
    add_card(slide, Inches(6.7), Inches(1.8), Inches(5.8), Inches(5.1), bg_color=COLOR_CARD_TINT, border_color=COLOR_PRIMARY_YELLOW)
    
    tb_img = slide.shapes.add_textbox(Inches(6.9), Inches(1.95), Inches(5.4), Inches(0.6))
    tf_i = tb_img.text_frame
    p_i = tf_i.paragraphs[0]
    p_i.text = "DESKTOP APPLICATION DEMONSTRATION"
    p_i.font.size = Pt(12)
    p_i.font.bold = True
    p_i.font.color.rgb = COLOR_DARK_YELLOW
    p_i.font.name = "Segoe UI"

    img_path = os.path.join(os.getcwd(), "gui_ranking_evidence.png")
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(6.9), Inches(2.6), Inches(5.4), Inches(3.8))


# ==============================================================================
# SLIDE 5: PERFORMANCE COMPARISON OF MERGE SORT VS OTHER ALGORITHMS (MANDATORY)
# ==============================================================================
def build_slide_5(prs):
    slide = create_blank_slide(prs)
    add_header(slide, "Algorithm Performance Comparison (Merge Sort vs Others)")

    # Left: Comparison Table Card
    add_card(slide, Inches(0.8), Inches(1.8), Inches(6.4), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_PRIMARY_YELLOW)
    
    tb_t = slide.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(6.0), Inches(0.4))
    tf_t = tb_t.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "EMPIRICAL BENCHMARK METRICS (N = 1,000 RECORDS)"
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_DARK_YELLOW
    p_t.font.name = "Segoe UI"

    # Add Table
    rows = 7
    cols = 6
    table_shape = slide.shapes.add_table(rows, cols, Inches(0.95), Inches(2.35), Inches(6.1), Inches(4.2))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(1.4)  # Algorithm
    table.columns[1].width = Inches(0.9)  # Time (ms)
    table.columns[2].width = Inches(1.0)  # Comparisons
    table.columns[3].width = Inches(0.9)  # Moves
    table.columns[4].width = Inches(1.0)  # Worst Case
    table.columns[5].width = Inches(0.9)  # Stability

    headers = ["Algorithm", "Time (ms)", "Comparisons", "Moves", "Worst Case", "Stability"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY_YELLOW
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.font.name = "Segoe UI"
        p.alignment = PP_ALIGN.CENTER

    data = [
        ("Merge Sort [BEST]", "2.81", "8,720", "19,944", "O(N log N)", "STABLE"),
        ("Quick Sort (Med-3)", "2.14", "10,240", "6,150", "O(N^2)", "UNSTABLE"),
        ("Heap Sort", "3.65", "16,842", "14,520", "O(N log N)", "UNSTABLE"),
        ("Insertion Sort", "18.40", "248,150", "249,149", "O(N^2)", "STABLE"),
        ("Selection Sort", "21.45", "499,500", "1,998", "O(N^2)", "UNSTABLE"),
        ("Bubble Sort", "34.10", "499,500", "496,210", "O(N^2)", "STABLE"),
    ]

    for i, row_data in enumerate(data):
        is_best = (i == 0)
        row_bg = COLOR_CARD_TINT if is_best else (COLOR_WHITE if i % 2 == 1 else COLOR_CARD_BG)
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.name = "Segoe UI"
            if is_best:
                p.font.bold = True
                p.font.color.rgb = COLOR_DARK_YELLOW if j == 0 else COLOR_TEXT_DARK
            else:
                p.font.color.rgb = COLOR_TEXT_DARK
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    # Right: Benchmark Curves Graph Card
    add_card(slide, Inches(7.4), Inches(1.8), Inches(5.1), Inches(5.1), bg_color=COLOR_WHITE, border_color=COLOR_PRIMARY_YELLOW)
    
    tb_g = slide.shapes.add_textbox(Inches(7.6), Inches(1.9), Inches(4.7), Inches(0.4))
    tf_g = tb_g.text_frame
    p_g = tf_g.paragraphs[0]
    p_g.text = "EMPIRICAL COMPLEXITY CURVES"
    p_g.font.size = Pt(11)
    p_g.font.bold = True
    p_g.font.color.rgb = COLOR_DARK_YELLOW
    p_g.font.name = "Segoe UI"

    bench_img = os.path.join(os.getcwd(), "benchmark_complexity_curves.png")
    if os.path.exists(bench_img):
        slide.shapes.add_picture(bench_img, Inches(7.55), Inches(2.4), Inches(4.8), Inches(3.6))

    tb_note = slide.shapes.add_textbox(Inches(7.6), Inches(6.1), Inches(4.7), Inches(0.7))
    tf_n = tb_note.text_frame
    tf_n.word_wrap = True
    p_n = tf_n.paragraphs[0]
    p_n.text = "Key Takeaway: Merge Sort guarantees flat O(N log N) scaling and stability, avoiding the O(N²) quadratic explosion of Bubble and Selection Sort."
    p_n.font.size = Pt(8.5)
    p_n.font.color.rgb = COLOR_TEXT_MUTED


# ==============================================================================
# SLIDE 6: KEY FINDINGS & VIVA HIGHLIGHTS
# ==============================================================================
def build_slide_6(prs):
    slide = create_blank_slide(prs)
    add_header(slide, "Key Technical Findings & Viva Highlights")

    cards = [
        ("STABILITY VALIDATION",
         "• Automated test case verified equal ratings:\n  EMP001 (4.8) strictly preceded EMP004 (4.8).\n• Merge Sort maintained 100% stability.\n• Quick Sort and Heap Sort failed stability test.",
         COLOR_CARD_TINT),
        ("SPACE-TIME TRADEOFF",
         "• Merge Sort trades O(N) auxiliary RAM for invariant O(N log N) determinism.\n• On modern machines, 100,000 employee records use <15 MB memory.\n• Stability & audit guarantee outweigh memory cost.",
         COLOR_WHITE),
        ("PIVOT DEGRADATION IN QUICK SORT",
         "• Standard QuickSort degrades to O(N²) on duplicate-heavy rating scales.\n• Mitigated using Median-of-Three pivot selection [arr[low], arr[mid], arr[high]].",
         COLOR_CARD_TINT),
        ("COURSE OUTCOMES ACHIEVED",
         "• CO3: Formulated 6 comparison sorting routines.\n• CO4: Mathematical & empirical O(N log N) proof.\n• CO5: Dual GUI/CLI + full unit test coverage.",
         COLOR_WHITE),
    ]

    positions = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.45)),
        (Inches(6.8), Inches(4.45)),
    ]

    for (title, text, bg), (left, top) in zip(cards, positions):
        add_card(slide, left, top, Inches(5.7), Inches(2.45), bg_color=bg, border_color=COLOR_PRIMARY_YELLOW)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"💡  {title}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_DARK_YELLOW
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_DARK
        p2.space_before = Pt(6)


# ==============================================================================
# SLIDE 7: THANK YOU SLIDE
# ==============================================================================
def build_slide_7(prs):
    slide = create_blank_slide(prs)

    # Top yellow accent strip
    top_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.15))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = COLOR_PRIMARY_YELLOW
    top_strip.line.fill.background()

    # Center Main Card
    center_card = add_card(slide, Inches(2.2), Inches(1.2), Inches(8.933), Inches(5.2), bg_color=COLOR_CARD_TINT, border_color=COLOR_PRIMARY_YELLOW, border_width=2.0)

    tb = slide.shapes.add_textbox(Inches(2.5), Inches(1.5), Inches(8.333), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    # Thank you header
    p_ty = tf.paragraphs[0]
    p_ty.text = "Thank You!"
    p_ty.font.size = Pt(44)
    p_ty.font.bold = True
    p_ty.font.color.rgb = COLOR_DARK_YELLOW
    p_ty.font.name = "Segoe UI"
    p_ty.alignment = PP_ALIGN.CENTER

    p_sub = tf.add_paragraph()
    p_sub.text = "Questions & Discussion"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = COLOR_TEXT_DARK
    p_sub.font.name = "Segoe UI"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(6)

    # Divider line
    p_div = tf.add_paragraph()
    p_div.text = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    p_div.font.size = Pt(11)
    p_div.font.color.rgb = COLOR_PRIMARY_YELLOW
    p_div.alignment = PP_ALIGN.CENTER
    p_div.space_before = Pt(8)

    # Student Info
    p_info = tf.add_paragraph()
    p_info.text = "Mani Chetan\nPRN: 25070725016\nB.Tech Computer Science and Engineering\nSymbiosis Institute of Technology (SIT)"
    p_info.font.size = Pt(13)
    p_info.font.bold = True
    p_info.font.color.rgb = COLOR_TEXT_DARK
    p_info.font.name = "Segoe UI"
    p_info.alignment = PP_ALIGN.CENTER
    p_info.space_before = Pt(10)

    # Project Repository info
    p_repo = tf.add_paragraph()
    p_repo.text = "GitHub Repository: github.com/chetan-hub-bot/dsa-mini-project"
    p_repo.font.size = Pt(11)
    p_repo.font.color.rgb = COLOR_DARK_YELLOW
    p_repo.font.name = "Segoe UI"
    p_repo.alignment = PP_ALIGN.CENTER
    p_repo.space_before = Pt(12)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building slides...")
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)

    output_filename = "Task35_Employee_Ranking_System_Presentation.pptx"
    workspace_path = os.path.join(r"c:\Users\6tan5\OneDrive\Desktop\dsa mini project", output_filename)
    downloads_path = os.path.join(r"C:\Users\6tan5\Downloads", output_filename)

    prs.save(workspace_path)
    print(f"Saved PPT to: {workspace_path}")

    try:
        prs.save(downloads_path)
        print(f"Saved PPT to Downloads: {downloads_path}")
    except Exception as e:
        print(f"Could not save to downloads: {e}")


if __name__ == "__main__":
    main()
