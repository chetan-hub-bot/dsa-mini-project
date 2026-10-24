# Task 35 – Employee Ranking System
> **Data Structures and Algorithms (DSA) – Lab CA-2 Experiential Learning Task**  
> **Course Outcomes Covered:** CO3 (Design of Algorithms), CO4 (Performance Analysis), CO5 (Practical Implementation)

---

## 📌 Project Overview

The **Employee Ranking System** is a software solution designed to evaluate, rank, and organize organizational personnel records based on multiple corporate metrics:
- **Performance Rating** ($1.0 - 5.0$)
- **Annual Compensation / Salary** ($\$$)
- **Industry Experience** (Years)
- **Composite Score** (Normalized multi-factor evaluation index)

The system features pure, academic implementations of **6 fundamental sorting algorithms** coded from scratch without using high-level built-in library sorting routines (`.sort()` or `sorted()`).

---

## 🏆 Selected Primary Algorithm: **Merge Sort**

### Why Merge Sort is the Best Choice for this Application:

1. **Stability Guarantee**:
   - In HR and payroll systems, multi-tier ranking is standard (e.g., sorting employees by Performance Rating first, while preserving previous seniority or department ordering).
   - **Merge Sort is inherently stable**: when two employees have identical performance ratings (e.g., $4.8$), their initial relative order is strictly preserved.
   - Quick Sort and Heap Sort are **unstable**, causing unpredictable tie-breaking that disrupts prior rankings.

2. **Guaranteed $O(N \log N)$ Worst-Case Bound**:
   - Merge Sort strictly follows divide-and-conquer, halving the array at every level of recursion:
     $$\text{Recurrence: } T(N) = 2T\left(\frac{N}{2}\right) + O(N)$$
     By Master Theorem (Case 2): $T(N) = \Theta(N \log N)$ for **Best, Average, and Worst cases**.
   - Naive Quick Sort degrades to $O(N^2)$ when inputs contain numerous duplicate keys (extremely common with rating scales like $1.0$ to $5.0$). Merge Sort never degrades.

3. **Deterministic & Audit-Ready**:
   - Personnel appraisals, promotion lists, and bonus pools require deterministic reproducibility for compliance audits. Merge Sort executes the exact same comparison tree regardless of key distribution.

4. **Acceptable Memory Trade-Off**:
   - The auxiliary memory cost of $O(N)$ is trivial on modern hardware for corporate rosters (even $100,000$ employee records require only a few megabytes of RAM).

---

## 📊 Theoretical vs Empirical Complexity Comparison

| Algorithm | Best Case | Average Case | Worst Case | Space Complexity | Stability | Role in Project |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Merge Sort** | $\mathbf{O(N \log N)}$ | $\mathbf{O(N \log N)}$ | $\mathbf{O(N \log N)}$ | $O(N)$ | **Stable (YES)** | **Primary Application Engine** |
| **Quick Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | Unstable | In-Place Baseline (Median-of-3) |
| **Heap Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | Unstable | In-Place Tree Selection |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Stable (YES) | Adaptive for small $N < 20$ |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Unstable | Comparison baseline |
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Stable (YES) | Simple baseline |

---

## 🏗️ Repository Architecture

```
dsa-mini-project/
├── core/
│   ├── __init__.py           # Package exports
│   ├── employee.py           # Employee dataclass, criteria keys & composite score
│   └── sorting.py            # Pure DSA sorting implementations with telemetry counters
├── ui/
│   ├── __init__.py
│   ├── app.py                # Modern Tkinter desktop application (3-tab interface)
│   └── benchmark_view.py     # Live empirical benchmarking dashboard with embedded Matplotlib curves
├── cli/
│   ├── __init__.py
│   └── menu.py               # Interactive ANSI console menu for terminal demonstration
├── data/
│   ├── __init__.py
│   ├── sample_employees.csv  # 25 pre-populated realistic corporate employee records
│   └── generator.py          # Synthetic dataset generator for benchmarking up to 20,000 records
├── tests/
│   ├── __init__.py
│   └── test_sorting.py       # Comprehensive unit tests (correctness, stability, edge cases)
├── main.py                   # Unified application entry point (GUI default, --cli flag)
├── VIVA_GUIDE.md             # 10-minute presentation guide, viva questions & answers
└── README.md                 # Complete project documentation
```

---

## 🚀 How to Run

### Option 1: Modern Desktop GUI Application (Default)
To launch the full graphical interface with employee tables, ranking selectors, live benchmark plots, and viva notes:
```bash
python main.py
```

### Option 2: Interactive Terminal CLI Mode
To run the interactive terminal menu (ideal for quick demonstration without GUI):
```bash
python main.py --cli
```

### Option 3: Automated Test Suite
To verify the correctness, stability, and edge cases across all algorithms:
```bash
python -m unittest discover tests -v
```

---

## 📈 Key Features

1. **Multi-Factor Ranking**:
   - Rank by Performance Rating ($1.0 - 5.0$), Salary, Experience, Composite Score, or Employee ID.
   - Toggle Ascending or Descending order instantly.

2. **Live Execution Telemetry**:
   - Microsecond-precision runtime measurement ($\mu s$ / $ms$).
   - Exact count of key comparisons ($C$) and element movements/swaps ($M$).

3. **Live Empirical Benchmark Dashboard**:
   - Generates synthetic cohorts from $N = 100$ to $N = 1,500+$.
   - Simultaneously plots execution time curves and operation counts comparing $O(N \log N)$ vs $O(N^2)$.

4. **Data Management**:
   - Add new employees through modal dialog.
   - Delete records.
   - Import/Export CSV files.
   - Reset dataset to standard sample with one click.
