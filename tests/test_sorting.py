"""Unit tests for sorting algorithms and employee ranking logic."""
import unittest
import random
from core.employee import Employee
from core.sorting import (
    merge_sort,
    quick_sort,
    heap_sort,
    insertion_sort,
    selection_sort,
    bubble_sort,
    ALGORITHMS,
    sort_employees,
)


class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a small controlled cohort of employees
        self.employees = [
            Employee("E01", "Alice Smith", "Engineering", 120000.0, 6.0, 4.8),
            Employee("E02", "Bob Jones", "Marketing", 85000.0, 3.5, 3.9),
            Employee("E03", "Charlie Brown", "Finance", 145000.0, 10.0, 4.2),
            Employee("E04", "Diana Prince", "HR", 92000.0, 5.0, 4.8),  # Same rating as Alice
            Employee("E05", "Evan Wright", "Engineering", 75000.0, 2.0, 3.5),
        ]

    def test_all_algorithms_correctness_numbers(self):
        """Verify all 6 algorithms correctly sort numbers in both ascending and descending order."""
        raw_numbers = [42, 17, -5, 88, 0, 17, 999, -100, 23]
        expected_asc = sorted(raw_numbers)
        expected_desc = sorted(raw_numbers, reverse=True)

        for algo_key, algo_info in ALGORITHMS.items():
            sort_fn = algo_info["func"]

            # Ascending test
            res_asc = sort_fn(raw_numbers, key=lambda x: x, reverse=False)
            self.assertEqual(res_asc.sorted_items, expected_asc, f"{algo_key} failed ascending sort")

            # Descending test
            res_desc = sort_fn(raw_numbers, key=lambda x: x, reverse=True)
            self.assertEqual(res_desc.sorted_items, expected_desc, f"{algo_key} failed descending sort")

    def test_all_algorithms_edge_cases(self):
        """Test empty list and single element list across all algorithms."""
        for algo_key, algo_info in ALGORITHMS.items():
            sort_fn = algo_info["func"]

            # Empty list
            res_empty = sort_fn([], key=lambda x: x)
            self.assertEqual(res_empty.sorted_items, [])

            # Single item
            res_single = sort_fn([42], key=lambda x: x)
            self.assertEqual(res_single.sorted_items, [42])

            # All identical items
            res_ident = sort_fn([7, 7, 7, 7, 7], key=lambda x: x)
            self.assertEqual(res_ident.sorted_items, [7, 7, 7, 7, 7])

    def test_employee_ranking_by_criteria(self):
        """Test ranking employees by different criteria."""
        # 1. By salary descending
        res_salary = sort_employees(self.employees, algorithm_key="merge_sort", criterion_key="salary", reverse=True)
        salaries = [e.salary for e in res_salary.sorted_items]
        self.assertEqual(salaries, [145000.0, 120000.0, 92000.0, 85000.0, 75000.0])

        # 2. By experience ascending
        res_exp = sort_employees(self.employees, algorithm_key="merge_sort", criterion_key="experience", reverse=False)
        exp_years = [e.experience_years for e in res_exp.sorted_items]
        self.assertEqual(exp_years, [2.0, 3.5, 5.0, 6.0, 10.0])

    def test_merge_sort_stability(self):
        """
        Verify that Merge Sort is STABLE:
        Employees E01 (Alice) and E04 (Diana) have the exact same performance rating (4.8).
        In the original list, E01 precedes E04.
        Merge Sort must preserve E01 before E04 when sorting by performance rating descending.
        """
        res_merge = sort_employees(self.employees, algorithm_key="merge_sort", criterion_key="performance", reverse=True)
        top_two_ids = [res_merge.sorted_items[0].emp_id, res_merge.sorted_items[1].emp_id]
        self.assertEqual(top_two_ids, ["E01", "E04"], "Merge Sort violated stability for equal keys!")

    def test_large_random_input(self):
        """Test algorithms with a randomized list of 100 elements."""
        random.seed(42)
        random_data = [random.randint(1, 1000) for _ in range(100)]
        expected = sorted(random_data)

        for algo_key, algo_info in ALGORITHMS.items():
            res = algo_info["func"](random_data, key=lambda x: x, reverse=False)
            self.assertEqual(res.sorted_items, expected, f"{algo_key} failed on random 100 elements")


if __name__ == "__main__":
    unittest.main()
