"""Core DSA package for Employee Ranking System."""
from .employee import Employee
from .sorting import (
    SortResult,
    merge_sort,
    quick_sort,
    heap_sort,
    insertion_sort,
    selection_sort,
    bubble_sort,
    ALGORITHMS,
    sort_employees
)

__all__ = [
    "Employee",
    "SortResult",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "insertion_sort",
    "selection_sort",
    "bubble_sort",
    "ALGORITHMS",
    "sort_employees",
]
