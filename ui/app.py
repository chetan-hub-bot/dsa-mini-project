"""Modern Desktop GUI for Task 35 - Employee Ranking System."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from typing import List, Optional

from core.employee import Employee, CRITERIA_MAP
from core.sorting import ALGORITHMS, sort_employees, SortResult
from data.generator import load_sample_employees, save_employees_to_csv
from .benchmark_view import BenchmarkView


class EmployeeRankingApp:
    """Main desktop application window managing the employee ranking interface."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Task 35 – Employee Ranking System | DSA Lab CA-2")
        self.root.geometry("1100x720")
        self.root.minsize(950, 600)

        # Style configuration
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self._configure_styles()

        # In-memory employee records
        self.employees: List[Employee] = load_sample_employees()
        self.last_result: Optional[SortResult] = None

        # Build Notebook with 3 tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self._build_ranking_tab()
        self._build_benchmark_tab()
        self._build_viva_tab()

        # Initial sort on launch
        self._on_rank_click()

    def _configure_styles(self):
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), padding=4)
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        self.style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), foreground="#ffffff", background="#007bff")
        self.style.configure("Best.TLabel", font=("Segoe UI", 9, "bold"), foreground="#28a745")

    # ==========================================================================
    # TAB 1: RANKING APPLICATION
    # ==========================================================================
    def _build_ranking_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="  🏆 Employee Directory & Ranking  ")

        # Top Control Panel
        ctrl_frame = ttk.LabelFrame(tab, text="Ranking Controls & Algorithm Selection", padding=10)
        ctrl_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 8))

        # Row 1: Controls
        r1 = ttk.Frame(ctrl_frame)
        r1.pack(fill=tk.X, expand=True)

        # Criterion dropdown
        ttk.Label(r1, text="Rank By:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 4))
        self.crit_var = tk.StringVar(value="performance")
        crit_combo = ttk.Combobox(
            r1, textvariable=self.crit_var, state="readonly", width=18,
            values=[
                ("Performance Rating", "performance"),
                ("Salary ($)", "salary"),
                ("Experience (Years)", "experience"),
                ("Composite Score", "composite"),
                ("Employee ID", "id"),
            ]
        )
        # Custom display mapping for combo
        self.crit_display_map = {
            "Performance Rating": "performance",
            "Salary ($)": "salary",
            "Experience (Years)": "experience",
            "Composite Score": "composite",
            "Employee ID": "id",
        }
        self.crit_reverse_map = {v: k for k, v in self.crit_display_map.items()}
        crit_combo.config(values=list(self.crit_display_map.keys()))
        crit_combo.set("Performance Rating")
        crit_combo.pack(side=tk.LEFT, padx=(0, 15))
        crit_combo.bind("<<ComboboxSelected>>", lambda e: self._on_crit_changed(crit_combo.get()))

        # Algorithm dropdown
        ttk.Label(r1, text="Algorithm:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 4))
        self.algo_var = tk.StringVar(value="merge_sort")
        self.algo_display_map = {
            "Merge Sort (Best - Stable O(N log N))": "merge_sort",
            "Quick Sort (In-Place O(N log N))": "quick_sort",
            "Heap Sort (Heap Tree O(N log N))": "heap_sort",
            "Insertion Sort (Adaptive O(N²))": "insertion_sort",
            "Selection Sort (Baseline O(N²))": "selection_sort",
            "Bubble Sort (Baseline O(N²))": "bubble_sort",
        }
        self.algo_reverse_map = {v: k for k, v in self.algo_display_map.items()}
        algo_combo = ttk.Combobox(
            r1, textvariable=self.algo_var, state="readonly", width=34,
            values=list(self.algo_display_map.keys())
        )
        algo_combo.set("Merge Sort (Best - Stable O(N log N))")
        algo_combo.pack(side=tk.LEFT, padx=(0, 15))
        algo_combo.bind("<<ComboboxSelected>>", lambda e: self._on_algo_changed(algo_combo.get()))

        # Direction radio
        self.dir_var = tk.StringVar(value="desc")
        rb_desc = ttk.Radiobutton(r1, text="Highest First (Desc)", variable=self.dir_var, value="desc")
        rb_asc = ttk.Radiobutton(r1, text="Lowest First (Asc)", variable=self.dir_var, value="asc")
        rb_desc.pack(side=tk.LEFT, padx=3)
        rb_asc.pack(side=tk.LEFT, padx=3)

        # Action Button
        btn_rank = ttk.Button(r1, text="⚡ Rank Employees", command=self._on_rank_click)
        btn_rank.pack(side=tk.RIGHT, padx=5)

        # Telemetry Banner
        self.telemetry_var = tk.StringVar(value="Ready. Select criteria and click 'Rank Employees'.")
        telemetry_lbl = ttk.Label(
            tab, textvariable=self.telemetry_var,
            font=("Segoe UI", 9, "bold"), foreground="#0056b3",
            background="#e9ecef", padding=(8, 5), relief=tk.SOLID
        )
        telemetry_lbl.pack(fill=tk.X, side=tk.TOP, pady=(0, 6))

        # Table (Treeview)
        table_container = ttk.Frame(tab)
        table_container.pack(fill=tk.BOTH, expand=True)

        cols = ("rank", "emp_id", "name", "dept", "salary", "exp", "rating", "score")
        self.tree = ttk.Treeview(table_container, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("rank", text="Rank")
        self.tree.heading("emp_id", text="Employee ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("salary", text="Salary ($)")
        self.tree.heading("exp", text="Experience")
        self.tree.heading("rating", text="Rating (1-5)")
        self.tree.heading("score", text="Composite Score (0-100)")

        self.tree.column("rank", width=55, anchor=tk.CENTER)
        self.tree.column("emp_id", width=95, anchor=tk.CENTER)
        self.tree.column("name", width=170, anchor=tk.W)
        self.tree.column("dept", width=120, anchor=tk.W)
        self.tree.column("salary", width=110, anchor=tk.E)
        self.tree.column("exp", width=100, anchor=tk.E)
        self.tree.column("rating", width=95, anchor=tk.CENTER)
        self.tree.column("score", width=140, anchor=tk.CENTER)

        # Tags for rank highlighting
        self.tree.tag_configure("rank1", background="#fff3cd", font=("Segoe UI", 9, "bold"))
        self.tree.tag_configure("rank2", background="#e2e3e5", font=("Segoe UI", 9, "bold"))
        self.tree.tag_configure("rank3", background="#fbebe1", font=("Segoe UI", 9, "bold"))

        scroll_y = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom Button Bar
        btn_bar = ttk.Frame(tab, padding=(0, 8))
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(btn_bar, text="➕ Add Employee", command=self._open_add_dialog).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_bar, text="🗑 Delete Selected", command=self._delete_selected).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_bar, text="📂 Import CSV", command=self._import_csv).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_bar, text="💾 Export Ranked CSV", command=self._export_csv).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_bar, text="🔄 Reset Sample Dataset", command=self._reset_sample).pack(side=tk.RIGHT, padx=3)

    def _on_crit_changed(self, display_val):
        self.crit_var.set(self.crit_display_map.get(display_val, "performance"))

    def _on_algo_changed(self, display_val):
        self.algo_var.set(self.algo_display_map.get(display_val, "merge_sort"))

    def _on_rank_click(self):
        crit_key = self.crit_var.get()
        algo_key = self.algo_var.get()
        reverse = (self.dir_var.get() == "desc")

        result = sort_employees(self.employees, algorithm_key=algo_key, criterion_key=crit_key, reverse=reverse)
        self.employees = result.sorted_items
        self.last_result = result

        # Refresh table
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, emp in enumerate(self.employees, 1):
            tag = ""
            rank_label = f"#{idx}"
            if idx == 1:
                tag = "rank1"
                rank_label = "🥇 #1"
            elif idx == 2:
                tag = "rank2"
                rank_label = "🥈 #2"
            elif idx == 3:
                tag = "rank3"
                rank_label = "🥉 #3"

            self.tree.insert(
                "", tk.END,
                values=(
                    rank_label,
                    emp.emp_id,
                    emp.name,
                    emp.department,
                    f"${emp.salary:,.2f}",
                    f"{emp.experience_years:.1f} yrs",
                    f"{emp.performance_rating:.1f} / 5.0",
                    f"{emp.composite_score:.1f}",
                ),
                tags=(tag,) if tag else ()
            )

        # Update telemetry
        crit_name = CRITERIA_MAP.get(crit_key, {}).get("name", crit_key)
        self.telemetry_var.set(
            f"⚡ {result.algorithm_name} | {crit_name} | "
            f"Time: {result.time_taken_ms:.3f} ms ({result.time_taken_us:.1f} µs) | "
            f"Comparisons: {result.comparisons:,} | Data Moves: {result.data_moves:,} | "
            f"Complexity: {result.time_complexity_avg} | Stability: {'STABLE' if result.is_stable else 'UNSTABLE'}"
        )

    def _open_add_dialog(self):
        """Modal dialog to enter a new employee record."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Employee")
        dlg.geometry("380, 320")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        fields = [
            ("Employee ID:", f"EMP{len(self.employees)+1:03d}"),
            ("Full Name:", ""),
            ("Department:", "Engineering"),
            ("Annual Salary ($):", "95000"),
            ("Experience (Years):", "4.0"),
            ("Performance Rating (1.0-5.0):", "4.5"),
        ]

        entries = {}
        for row_idx, (label_text, default_val) in enumerate(fields):
            ttk.Label(dlg, text=label_text).grid(row=row_idx, column=0, sticky=tk.W, padx=15, pady=6)
            ent = ttk.Entry(dlg, width=24)
            ent.insert(0, default_val)
            ent.grid(row=row_idx, column=1, padx=15, pady=6)
            entries[label_text] = ent

        def _save():
            try:
                emp_id = entries["Employee ID:"].get().strip()
                name = entries["Full Name:"].get().strip()
                dept = entries["Department:"].get().strip()
                sal = float(entries["Annual Salary ($):"].get().strip())
                exp = float(entries["Experience (Years):"].get().strip())
                rating = float(entries["Performance Rating (1.0-5.0):"].get().strip())

                if not emp_id or not name or not dept:
                    messagebox.showerror("Validation Error", "All fields are required.", parent=dlg)
                    return

                new_emp = Employee(emp_id, name, dept, sal, exp, rating)
                self.employees.append(new_emp)
                dlg.destroy()
                self._on_rank_click()
                messagebox.showinfo("Success", f"Added {name} ({emp_id}) successfully!", parent=self.root)
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid numeric value: {e}", parent=dlg)

        btn_box = ttk.Frame(dlg)
        btn_box.grid(row=len(fields), column=0, columnspan=2, pady=15)
        ttk.Button(btn_box, text="Save Employee", command=_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Cancel", command=dlg.destroy).pack(side=tk.LEFT, padx=5)

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Notice", "Please select an employee row to delete.", parent=self.root)
            return

        item = self.tree.item(sel[0])
        emp_id = item["values"][1]

        self.employees = [e for e in self.employees if e.emp_id != emp_id]
        self._on_rank_click()
        messagebox.showinfo("Deleted", f"Employee {emp_id} deleted.", parent=self.root)

    def _import_csv(self):
        path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            parent=self.root
        )
        if path:
            try:
                loaded = load_sample_employees(path)
                self.employees = loaded
                self._on_rank_click()
                messagebox.showinfo("Imported", f"Successfully loaded {len(loaded)} records.", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {e}", parent=self.root)

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            parent=self.root
        )
        if path:
            try:
                save_employees_to_csv(self.employees, path)
                messagebox.showinfo("Exported", f"Ranked records saved to: {path}", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {e}", parent=self.root)

    def _reset_sample(self):
        self.employees = load_sample_employees()
        self._on_rank_click()
        messagebox.showinfo("Reset", "Dataset reset to default 25 sample employees.", parent=self.root)

    # ==========================================================================
    # TAB 2: BENCHMARK SUITE
    # ==========================================================================
    def _build_benchmark_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="  📈 Benchmark & Complexity Curves  ")
        self.benchmark_view = BenchmarkView(tab)
        self.benchmark_view.pack(fill=tk.BOTH, expand=True)

    # ==========================================================================
    # TAB 3: ALGORITHM JUSTIFICATION & VIVA PREPARATION
    # ==========================================================================
    def _build_viva_tab(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="  🎓 'Why Merge Sort?' & Viva Prep  ")

        # Scrollable text widget with viva answers
        text_frame = ttk.Frame(tab)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(
            text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
            font=("Consolas", 10), padx=12, pady=12,
            background="#ffffff", foreground="#212529"
        )
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)

        viva_content = """================================================================================
TASK 35 – EMPLOYEE RANKING SYSTEM: DSA LAB CA-2 VIVA PREPARATION GUIDE
================================================================================

1. WHY DID WE CHOOSE MERGE SORT AS THE PRIMARY ALGORITHM?
--------------------------------------------------------------------------------
1. Stability:
   In employee ranking, stability is mandatory. If two employees share the same
   Performance Rating (e.g. 4.8), a stable sort ensures their prior order
   (such as Experience or Seniority) remains intact. Merge Sort guarantees stability.
   Quick Sort and Heap Sort are UNSTABLE and disrupt equal-key ordering.

2. Guaranteed O(N log N) Worst-Case Time Complexity:
   Merge Sort strictly divides the array into halves regardless of initial ordering:
     Recurrence: T(N) = 2*T(N/2) + O(N)
     By Master Theorem Case 2: T(N) = Theta(N log N).
   Quick Sort degrades to O(N^2) on sorted/duplicate-heavy inputs (common in HR rating scales).
   Merge Sort never suffers from this degradation.

3. Predictable & Deterministic Execution:
   Corporate payroll, appraisals, and promotions require audit reproducibility.
   Merge Sort produces deterministic execution passes without recursion depth risks.


2. THEORETICAL COMPLEXITY COMPARISON MATRIX
--------------------------------------------------------------------------------
Algorithm      | Best Case   | Average Case | Worst Case  | Space   | Stability
--------------------------------------------------------------------------------
Merge Sort     | O(N log N)  | O(N log N)   | O(N log N)  | O(N)    | STABLE (YES)
Quick Sort     | O(N log N)  | O(N log N)   | O(N^2)      | O(log N)| UNSTABLE
Heap Sort      | O(N log N)  | O(N log N)   | O(N log N)  | O(1)    | UNSTABLE
Insertion Sort | O(N)        | O(N^2)       | O(N^2)      | O(1)    | STABLE (YES)
Selection Sort | O(N^2)      | O(N^2)       | O(N^2)      | O(1)    | UNSTABLE
Bubble Sort    | O(N)        | O(N^2)       | O(N^2)      | O(1)    | STABLE (YES)
--------------------------------------------------------------------------------


3. TOP 5 VIVA QUESTIONS & DIRECT ANSWERS
--------------------------------------------------------------------------------
Q1: What is the space-time trade-off in Merge Sort?
A1: Merge Sort trades O(N) auxiliary memory for guaranteed O(N log N) time and
    stability. For an in-memory employee roster (even 100,000 records), O(N) space
    is tiny (a few megabytes), making the stability and worst-case guarantee well
    worth the memory trade-off.

Q2: Why does Quick Sort have an O(N^2) worst case, and how did we mitigate it?
A2: When the pivot chosen is consistently the extreme (smallest or largest element),
    the partition becomes completely unbalanced (1 vs N-1 elements). In our
    implementation, we mitigated this using Median-of-Three pivot selection
    (comparing arr[low], arr[mid], arr[high]).

Q3: Can Heap Sort be made stable?
A3: Standard in-place Heap Sort is inherently unstable because the binary heap
    swaps elements across distant levels of the tree. While an auxiliary index
    can artificially track original positions, it requires extra space, negating
    Heap Sort's primary advantage of O(1) auxiliary space.

Q4: When would Insertion Sort be preferred over Merge Sort?
A4: Insertion Sort outperforms Merge Sort on very small datasets (N < 20) or
    nearly-sorted datasets because it has minimal overhead and achieves O(N)
    time on already-sorted input.

Q5: How does composite scoring work in this application?
A5: It normalizes Performance (0-5.0), Experience (0-25 yrs), and Salary (0-$200k)
    into standard scales and calculates a weighted index:
      Score = (Norm_Perf * 0.50) + (Norm_Exp * 0.30) + (Norm_Salary * 0.20) * 100.
"""
        text.insert(tk.END, viva_content)
        text.config(state=tk.DISABLED)
