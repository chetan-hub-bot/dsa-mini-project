"""Interactive Command-Line Interface (CLI) for Employee Ranking Demonstration."""
import sys
import copy
from typing import List
from core.employee import Employee, CRITERIA_MAP
from core.sorting import ALGORITHMS, sort_employees, SortResult
from data.generator import load_sample_employees, generate_synthetic_employees


def print_header(title: str):
    """Print an eye-catching formatted section header."""
    line = "=" * 78
    print(f"\n{line}")
    print(f"  {title.center(74)}")
    print(f"{line}")


def print_table(employees: List[Employee], criterion_key: str = "performance", max_rows: int = 25):
    """Prints a neat ASCII table of employee records with ranks."""
    crit_info = CRITERIA_MAP.get(criterion_key, CRITERIA_MAP["performance"])
    crit_header = crit_info["name"]

    print("\n" + "-" * 88)
    print(f"{'Rank':<5} | {'ID':<7} | {'Name':<18} | {'Department':<13} | {'Salary':<12} | {'Exp':<8} | {'Rating':<7} | {'Score':<6}")
    print("-" * 88)

    for idx, emp in enumerate(employees[:max_rows], 1):
        print(
            f"{idx:<5} | {emp.emp_id:<7} | {emp.name:<18} | {emp.department:<13} | "
            f"${emp.salary:>10,.2f} | {emp.experience_years:>4.1f} yrs | {emp.performance_rating:>4.1f}   | {emp.composite_score:>5.1f}"
        )

    if len(employees) > max_rows:
        print(f"... and {len(employees) - max_rows} more records.")
    print("-" * 88)


def print_telemetry(result: SortResult, criterion_key: str, count: int):
    """Prints algorithm execution statistics."""
    crit_name = CRITERIA_MAP.get(criterion_key, {}).get("name", criterion_key)
    print("\n📊 SORTING TELEMETRY & PERFORMANCE METRICS:")
    print(f"  • Algorithm Used    : {result.algorithm_name}")
    print(f"  • Ranking Criterion : {crit_name}")
    print(f"  • Records Sorted    : {count:,}")
    print(f"  • Execution Time    : {result.time_taken_ms:.4f} ms ({result.time_taken_us:.1f} µs)")
    print(f"  • Key Comparisons   : {result.comparisons:,}")
    print(f"  • Data Swaps/Moves  : {result.data_moves:,}")
    print(f"  • Time Complexity   : Best: {result.time_complexity_best} | Avg: {result.time_complexity_avg} | Worst: {result.time_complexity_worst}")
    print(f"  • Space Complexity  : {result.space_complexity}")
    print(f"  • Stability         : {result.stability_guarantee}")


def show_why_merge_sort():
    """Explains academic justification for choosing Merge Sort for Task 35."""
    print_header("ACADEMIC JUSTIFICATION: WHY MERGE SORT WAS CHOSEN")
    print("""
1. CRUCIAL REQUIREMENT: STABILITY
   • In multi-criteria employee evaluation (e.g., sort by Performance Rating first,
     then by Experience, then by Salary), equal rating scores occur frequently.
   • Merge Sort is guaranteed STABLE: it preserves the previous relative ordering
     of employees with identical scores.
   • Quick Sort and Heap Sort are inherently UNSTABLE, scrambling prior ties.

2. GUARANTEED WORST-CASE BOUND OF O(N log N)
   • Merge Sort consistently divides the dataset into halves:
     Recurrence: T(N) = 2T(N/2) + O(N)  --> Master Theorem Case 2: Theta(N log N)
   • Unlike naive Quick Sort which degrades to O(N^2) on duplicate-heavy or
     already-sorted corporate payroll lists, Merge Sort never degrades.

3. PREDICTABLE & DETERMINISTIC FOR ENTERPRISE AUDITS
   • HR decisions and bonuses require audit reproducibility.
   • Merge Sort's execution tree is completely deterministic.
   • The auxiliary space tradeoff of O(N) is negligible for employee record lists.
    """)


def run_benchmark_suite():
    """Runs all 6 algorithms on identical synthetic datasets of size N."""
    print_header("PERFORMANCE BENCHMARK OF ALL 6 ALGORITHMS")
    print("Select dataset size to benchmark:")
    print("  1. Small  (N = 250 records)")
    print("  2. Medium (N = 1,000 records)")
    print("  3. Large  (N = 3,000 records)")
    print("  4. Custom N")
    
    choice = input("\nEnter choice [1-4] (default=2): ").strip() or "2"
    if choice == "1":
        n = 250
    elif choice == "3":
        n = 3000
    elif choice == "4":
        try:
            n = int(input("Enter record count N (e.g. 500-10000): ").strip())
        except ValueError:
            n = 1000
    else:
        n = 1000

    print(f"\nGenerating {n:,} synthetic employee records...")
    dataset = generate_synthetic_employees(n, seed=42)

    print(f"\nBenchmarking all 6 algorithms sorting by 'Performance Rating' (Descending)...\n")
    print("-" * 84)
    print(f"{'Algorithm':<16} | {'Time (ms)':<10} | {'Comparisons':<14} | {'Data Moves':<12} | {'Stability':<10} | {'Complexity'}")
    print("-" * 84)

    for algo_key, algo_info in ALGORITHMS.items():
        # Copy dataset to give every algorithm identical input
        dataset_copy = copy.copy(dataset)
        res = sort_employees(dataset_copy, algorithm_key=algo_key, criterion_key="performance", reverse=True)
        stable_str = "Stable" if res.is_stable else "Unstable"
        print(
            f"{res.algorithm_name:<16} | {res.time_taken_ms:>10.3f} | {res.comparisons:>14,d} | "
            f"{res.data_moves:>12,d} | {stable_str:<10} | {res.time_complexity_avg}"
        )

    print("-" * 84)
    print("\nKey Insight: Notice how Merge Sort, Quick Sort, and Heap Sort complete in O(N log N),")
    print("whereas Bubble Sort and Selection Sort scale exponentially as O(N^2).")


def run_cli_menu():
    """Main interactive terminal loop."""
    employees = load_sample_employees()

    while True:
        print_header("TASK 35: EMPLOYEE RANKING SYSTEM (DSA LAB CA-2)")
        print(f"Current Directory: {len(employees)} Employee Records Loaded")
        print("\nChoose an option:")
        print("  [1] View Current Employee Records")
        print("  [2] Rank by Performance Rating (using Best Algorithm: Merge Sort)")
        print("  [3] Rank by Salary (using Best Algorithm: Merge Sort)")
        print("  [4] Rank by Experience (using Best Algorithm: Merge Sort)")
        print("  [5] Custom Ranking (Select any Criterion, Algorithm & Direction)")
        print("  [6] Compare All 6 Algorithms (Live Empirical Benchmark)")
        print("  [7] Why Merge Sort? (Detailed Justification & Viva Notes)")
        print("  [8] Add a New Employee")
        print("  [9] Reset to Default Sample Dataset")
        print("  [0] Exit")

        choice = input("\nEnter choice [0-9]: ").strip()

        if choice == "0":
            print("\nExiting Employee Ranking System. Best of luck with Lab CA-2!\n")
            sys.exit(0)

        elif choice == "1":
            print_table(employees, "performance")

        elif choice in ("2", "3", "4"):
            criterion = "performance" if choice == "2" else ("salary" if choice == "3" else "experience")
            res = sort_employees(employees, algorithm_key="merge_sort", criterion_key=criterion, reverse=True)
            employees = res.sorted_items
            print_table(employees, criterion)
            print_telemetry(res, criterion, len(employees))

        elif choice == "5":
            print("\nSelect Criterion:")
            print("  1. Performance Rating (1.0 - 5.0)")
            print("  2. Salary ($)")
            print("  3. Experience (Years)")
            print("  4. Composite Score (50% Perf, 30% Exp, 20% Sal)")
            c_sel = input("Choice [1-4] (default=1): ").strip() or "1"
            crit_key = {"1": "performance", "2": "salary", "3": "experience", "4": "composite"}.get(c_sel, "performance")

            print("\nSelect Algorithm:")
            for idx, (k, v) in enumerate(ALGORITHMS.items(), 1):
                rec = " [RECOMMENDED BEST]" if v["recommended"] else ""
                print(f"  {idx}. {v['name']} ({v['complexity']}){rec}")
            a_sel = input("Choice [1-6] (default=1): ").strip() or "1"
            algo_keys = list(ALGORITHMS.keys())
            try:
                algo_key = algo_keys[int(a_sel) - 1]
            except (ValueError, IndexError):
                algo_key = "merge_sort"

            print("\nOrder:")
            print("  1. Highest to Lowest (Descending - Standard for Ranking)")
            print("  2. Lowest to Highest (Ascending)")
            o_sel = input("Choice [1-2] (default=1): ").strip() or "1"
            reverse = (o_sel != "2")

            res = sort_employees(employees, algorithm_key=algo_key, criterion_key=crit_key, reverse=reverse)
            employees = res.sorted_items
            print_table(employees, crit_key)
            print_telemetry(res, crit_key, len(employees))

        elif choice == "6":
            run_benchmark_suite()

        elif choice == "7":
            show_why_merge_sort()

        elif choice == "8":
            print_header("ADD NEW EMPLOYEE")
            try:
                emp_id = input("Enter ID (e.g. EMP999): ").strip() or f"EMP{len(employees)+1:03d}"
                name = input("Enter Full Name: ").strip() or "New Employee"
                dept = input("Enter Department: ").strip() or "General"
                sal = float(input("Enter Annual Salary ($): ").strip() or "90000")
                exp = float(input("Enter Experience in Years: ").strip() or "3.5")
                rating = float(input("Enter Performance Rating (1.0 to 5.0): ").strip() or "4.0")

                new_emp = Employee(emp_id, name, dept, sal, exp, rating)
                employees.append(new_emp)
                print(f"\nSuccessfully added: {new_emp}")
            except ValueError as e:
                print(f"\nInvalid input: {e}")

        elif choice == "9":
            employees = load_sample_employees()
            print(f"\nReloaded {len(employees)} default records from sample_employees.csv.")

        else:
            print("\nInvalid choice. Please select from 0 to 9.")

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    run_cli_menu()
