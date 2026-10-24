"""Benchmark View Component with Embedded Matplotlib Performance Visualizations."""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import copy
from typing import Dict, List, Any

# Matplotlib integration with Tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.sorting import ALGORITHMS, sort_employees
from data.generator import generate_synthetic_employees


class BenchmarkView(ttk.Frame):
    """Embeds live performance benchmarking graphs and comparison metrics."""

    def __init__(self, parent):
        super().__init__(parent)
        self.sizes = [100, 250, 500, 1000, 1500]
        self._build_ui()

    def _build_ui(self):
        # Top toolbar
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        title_lbl = ttk.Label(
            toolbar,
            text="Empirical Complexity Benchmark: O(N log N) vs O(N²)",
            font=("Segoe UI", 12, "bold")
        )
        title_lbl.pack(side=tk.LEFT, padx=5)

        self.btn_run = ttk.Button(
            toolbar,
            text="▶ Run Benchmark Live",
            command=self._on_run_click
        )
        self.btn_run.pack(side=tk.RIGHT, padx=5)

        self.status_var = tk.StringVar(value="Click 'Run Benchmark Live' to compare all 6 algorithms.")
        status_lbl = ttk.Label(toolbar, textvariable=self.status_var, font=("Segoe UI", 9, "italic"), foreground="#555")
        status_lbl.pack(side=tk.RIGHT, padx=15)

        # Main splitter (Top: Graphs, Bottom: Metrics Table)
        paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        # Graph Container
        graph_frame = ttk.LabelFrame(paned, text="Live Complexity Curves", padding=5)
        paned.add(graph_frame, weight=3)

        self.fig = Figure(figsize=(9, 4.2), dpi=100)
        self.fig.patch.set_facecolor("#f8f9fa")

        # Two subplots: Time vs N, and Comparisons vs N
        self.ax_time = self.fig.add_subplot(121)
        self.ax_ops = self.fig.add_subplot(122)
        self.fig.tight_layout(pad=3.0)

        self._init_plots()

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Table Container
        table_frame = ttk.LabelFrame(paned, text="Empirical Results Table (N = 1,000)", padding=5)
        paned.add(table_frame, weight=2)

        cols = ("algo", "time_ms", "comparisons", "moves", "stability", "complexity_class")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=7)
        self.tree.heading("algo", text="Algorithm")
        self.tree.heading("time_ms", text="Time (ms)")
        self.tree.heading("comparisons", text="Comparisons")
        self.tree.heading("moves", text="Data Moves")
        self.tree.heading("stability", text="Stability")
        self.tree.heading("complexity_class", text="Theoretical Complexity")

        self.tree.column("algo", width=140, anchor=tk.W)
        self.tree.column("time_ms", width=90, anchor=tk.E)
        self.tree.column("comparisons", width=110, anchor=tk.E)
        self.tree.column("moves", width=100, anchor=tk.E)
        self.tree.column("stability", width=90, anchor=tk.CENTER)
        self.tree.column("complexity_class", width=140, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_plots(self):
        """Initial placeholders for plots."""
        self.ax_time.clear()
        self.ax_time.set_title("Execution Time (ms) vs Input Size N", fontsize=10, fontweight="bold")
        self.ax_time.set_xlabel("Number of Employees (N)", fontsize=9)
        self.ax_time.set_ylabel("Time (milliseconds)", fontsize=9)
        self.ax_time.grid(True, linestyle="--", alpha=0.6)

        self.ax_ops.clear()
        self.ax_ops.set_title("Comparisons Count vs Input Size N", fontsize=10, fontweight="bold")
        self.ax_ops.set_xlabel("Number of Employees (N)", fontsize=9)
        self.ax_ops.set_ylabel("Key Comparisons", fontsize=9)
        self.ax_ops.grid(True, linestyle="--", alpha=0.6)

    def _on_run_click(self):
        self.btn_run.config(state=tk.DISABLED)
        self.status_var.set("Benchmarking algorithms across N=[100, 250, 500, 1000, 1500]...")

        # Run benchmark in worker thread so UI does not stutter
        thread = threading.Thread(target=self._execute_benchmark, daemon=True)
        thread.start()

    def _execute_benchmark(self):
        color_palette = {
            "merge_sort": "#28a745",     # Green (Best)
            "quick_sort": "#007bff",     # Blue
            "heap_sort": "#17a2b8",      # Cyan
            "insertion_sort": "#fd7e14", # Orange
            "selection_sort": "#6f42c1", # Purple
            "bubble_sort": "#dc3545",    # Red
        }

        markers = {
            "merge_sort": "o",
            "quick_sort": "s",
            "heap_sort": "^",
            "insertion_sort": "D",
            "selection_sort": "v",
            "bubble_sort": "x",
        }

        # Data collection
        time_data: Dict[str, List[float]] = {k: [] for k in ALGORITHMS}
        ops_data: Dict[str, List[int]] = {k: [] for k in ALGORITHMS}
        results_at_1000 = {}

        for n in self.sizes:
            base_data = generate_synthetic_employees(n, seed=100 + n)
            for algo_key in ALGORITHMS:
                dataset_copy = copy.copy(base_data)
                res = sort_employees(dataset_copy, algorithm_key=algo_key, criterion_key="performance", reverse=True)
                time_data[algo_key].append(res.time_taken_ms)
                ops_data[algo_key].append(res.comparisons)
                if n == 1000:
                    results_at_1000[algo_key] = res

        # Update GUI on main thread
        self.after(0, lambda: self._update_results(time_data, ops_data, results_at_1000, color_palette, markers))

    def _update_results(self, time_data, ops_data, results_at_1000, color_palette, markers):
        self._init_plots()

        # Plot curves
        for algo_key, info in ALGORITHMS.items():
            color = color_palette.get(algo_key, "#333")
            marker = markers.get(algo_key, "o")
            name = info["name"] + (" ★" if info["recommended"] else "")
            lw = 2.5 if info["recommended"] else 1.5

            self.ax_time.plot(
                self.sizes, time_data[algo_key],
                label=name, color=color, marker=marker, linewidth=lw
            )
            self.ax_ops.plot(
                self.sizes, ops_data[algo_key],
                label=name, color=color, marker=marker, linewidth=lw
            )

        self.ax_time.legend(fontsize=8, loc="upper left")
        self.ax_ops.legend(fontsize=8, loc="upper left")
        self.fig.tight_layout(pad=2.5)
        self.canvas.draw()

        # Populate metrics table
        for item in self.tree.get_children():
            self.tree.delete(item)

        for algo_key, res in results_at_1000.items():
            info = ALGORITHMS[algo_key]
            name = info["name"] + (" (BEST)" if info["recommended"] else "")
            stability = "Stable" if res.is_stable else "Unstable"
            self.tree.insert(
                "", tk.END,
                values=(
                    name,
                    f"{res.time_taken_ms:.2f}",
                    f"{res.comparisons:,}",
                    f"{res.data_moves:,}",
                    stability,
                    info["complexity"]
                )
            )

        self.btn_run.config(state=tk.NORMAL)
        self.status_var.set("Benchmark completed successfully! Notice O(N log N) vs O(N²) scaling.")
