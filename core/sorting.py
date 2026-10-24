"""Pure Data Structures & Algorithms implementations of Sorting Algorithms with Telemetry.

This module provides academic, from-scratch implementations of fundamental sorting
algorithms without using Python's built-in .sort() or sorted().
Each algorithm records:
- Execution time (microseconds and milliseconds)
- Number of key comparisons
- Number of data movements (swaps / array assignments)
"""
import time
from dataclasses import dataclass
from typing import List, Callable, Any, Tuple


@dataclass
class SortResult:
    """Encapsulates sorted output and empirical runtime telemetry."""
    sorted_items: List[Any]
    algorithm_name: str
    time_taken_ms: float
    time_taken_us: float
    comparisons: int
    data_moves: int
    is_stable: bool
    time_complexity_best: str
    time_complexity_avg: str
    time_complexity_worst: str
    space_complexity: str
    stability_guarantee: str


class _SortTracker:
    """Internal counter for comparisons and element moves during sorting."""
    def __init__(self, key_func: Callable[[Any], Any], reverse: bool = False):
        self.key_func = key_func
        self.reverse = reverse
        self.comparisons = 0
        self.data_moves = 0

    def should_come_before(self, a: Any, b: Any) -> bool:
        """
        Returns True if item 'a' should strictly precede 'b' according to
        the ranking criteria and sort direction (reverse=True means descending).
        """
        self.comparisons += 1
        ka = self.key_func(a)
        kb = self.key_func(b)
        if self.reverse:
            return ka > kb
        return ka < kb

    def is_equal_or_comes_before(self, a: Any, b: Any) -> bool:
        """
        Used for stable partitioning and merging: returns True if 'a' has equal
        or higher priority than 'b'.
        """
        self.comparisons += 1
        ka = self.key_func(a)
        kb = self.key_func(b)
        if self.reverse:
            return ka >= kb
        return ka <= kb


# ==============================================================================
# 1. MERGE SORT (Best Chosen Algorithm for Employee Ranking)
# ==============================================================================
def merge_sort(
    items: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> SortResult:
    """
    Merge Sort: Divide-and-Conquer, Stable, O(N log N) time in all cases.
    Ideal for multi-criteria employee ranking where stability preserves prior ties.
    """
    arr = list(items)
    n = len(arr)
    tracker = _SortTracker(key, reverse)

    start_time = time.perf_counter()

    def _merge(left: List[Any], right: List[Any]) -> List[Any]:
        merged = []
        i = j = 0
        len_l, len_r = len(left), len(right)

        # Merge elements in sorted order
        while i < len_l and j < len_r:
            # Crucial for STABILITY: when left == right, take left first!
            if tracker.is_equal_or_comes_before(left[i], right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            tracker.data_moves += 1

        # Append remaining elements
        while i < len_l:
            merged.append(left[i])
            i += 1
            tracker.data_moves += 1

        while j < len_r:
            merged.append(right[j])
            j += 1
            tracker.data_moves += 1

        return merged

    def _merge_sort_recursive(sub_arr: List[Any]) -> List[Any]:
        if len(sub_arr) <= 1:
            return sub_arr

        mid = len(sub_arr) // 2
        left_sorted = _merge_sort_recursive(sub_arr[:mid])
        right_sorted = _merge_sort_recursive(sub_arr[mid:])
        return _merge(left_sorted, right_sorted)

    sorted_arr = _merge_sort_recursive(arr)
    elapsed_s = time.perf_counter() - start_time

    return SortResult(
        sorted_items=sorted_arr,
        algorithm_name="Merge Sort",
        time_taken_ms=elapsed_s * 1000.0,
        time_taken_us=elapsed_s * 1_000_000.0,
        comparisons=tracker.comparisons,
        data_moves=tracker.data_moves,
        is_stable=True,
        time_complexity_best="O(N log N)",
        time_complexity_avg="O(N log N)",
        time_complexity_worst="O(N log N)",
        space_complexity="O(N)",
        stability_guarantee="Stable (Preserves existing ordering of equal records)",
    )


# ==============================================================================
# 2. QUICK SORT (In-place Divide-and-Conquer with Median-of-Three Pivot)
# ==============================================================================
def quick_sort(
    items: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> SortResult:
    """
    Quick Sort: In-place, average O(N log N).
    Uses median-of-three pivot selection to prevent O(N^2) on pre-sorted data.
    Standard in-place Quick Sort is Unstable.
    """
    arr = list(items)
    n = len(arr)
    tracker = _SortTracker(key, reverse)

    start_time = time.perf_counter()

    def _median_of_three(low: int, mid: int, high: int):
        # Sort arr[low], arr[mid], arr[high] so median ends up at arr[mid]
        if tracker.should_come_before(arr[mid], arr[low]):
            arr[low], arr[mid] = arr[mid], arr[low]
            tracker.data_moves += 2
        if tracker.should_come_before(arr[high], arr[low]):
            arr[low], arr[high] = arr[high], arr[low]
            tracker.data_moves += 2
        if tracker.should_come_before(arr[high], arr[mid]):
            arr[mid], arr[high] = arr[high], arr[mid]
            tracker.data_moves += 2

    def _partition(low: int, high: int) -> int:
        mid = low + (high - low) // 2
        _median_of_three(low, mid, high)

        # Place median at high - 1 as pivot
        arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
        tracker.data_moves += 2
        pivot = arr[high - 1]

        i = low
        j = high - 1

        while True:
            i += 1
            while i < high and tracker.should_come_before(arr[i], pivot):
                i += 1
            j -= 1
            while j > low and tracker.should_come_before(pivot, arr[j]):
                j -= 1

            if i >= j:
                break

            arr[i], arr[j] = arr[j], arr[i]
            tracker.data_moves += 2

        # Restore pivot to correct index
        arr[i], arr[high - 1] = arr[high - 1], arr[i]
        tracker.data_moves += 2
        return i

    def _quick_sort_recursive(low: int, high: int):
        if low + 3 <= high:
            pivot_idx = _partition(low, high)
            _quick_sort_recursive(low, pivot_idx - 1)
            _quick_sort_recursive(pivot_idx + 1, high)
        else:
            # Insertion sort fallback for small sub-arrays (<= 3 elements)
            for i in range(low + 1, high + 1):
                temp = arr[i]
                j = i - 1
                while j >= low and tracker.should_come_before(temp, arr[j]):
                    arr[j + 1] = arr[j]
                    tracker.data_moves += 1
                    j -= 1
                arr[j + 1] = temp
                tracker.data_moves += 1

    if n > 1:
        _quick_sort_recursive(0, n - 1)

    elapsed_s = time.perf_counter() - start_time

    return SortResult(
        sorted_items=arr,
        algorithm_name="Quick Sort",
        time_taken_ms=elapsed_s * 1000.0,
        time_taken_us=elapsed_s * 1_000_000.0,
        comparisons=tracker.comparisons,
        data_moves=tracker.data_moves,
        is_stable=False,
        time_complexity_best="O(N log N)",
        time_complexity_avg="O(N log N)",
        time_complexity_worst="O(N^2)",
        space_complexity="O(log N)",
        stability_guarantee="Unstable (May alter relative order of equal keys)",
    )


# ==============================================================================
# 3. HEAP SORT (Binary Heap, In-place O(N log N))
# ==============================================================================
def heap_sort(
    items: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> SortResult:
    """
    Heap Sort: In-place, guaranteed O(N log N), Unstable.
    Builds a binary heap, then repeatedly extracts root.
    """
    arr = list(items)
    n = len(arr)
    tracker = _SortTracker(key, reverse)

    start_time = time.perf_counter()

    def _heapify(heap_size: int, root_idx: int):
        target = root_idx
        left = 2 * root_idx + 1
        right = 2 * root_idx + 2

        # For normal order, heap sort builds a Max-Heap (arr[i] < root).
        # We want the root to be the element that comes LAST in sorted order,
        # so when moved to the end, it creates the desired order.
        if left < heap_size and tracker.should_come_before(arr[target], arr[left]):
            target = left

        if right < heap_size and tracker.should_come_before(arr[target], arr[right]):
            target = right

        if target != root_idx:
            arr[root_idx], arr[target] = arr[target], arr[root_idx]
            tracker.data_moves += 2
            _heapify(heap_size, target)

    # 1. Build Heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)

    # 2. Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        tracker.data_moves += 2
        _heapify(i, 0)

    elapsed_s = time.perf_counter() - start_time

    return SortResult(
        sorted_items=arr,
        algorithm_name="Heap Sort",
        time_taken_ms=elapsed_s * 1000.0,
        time_taken_us=elapsed_s * 1_000_000.0,
        comparisons=tracker.comparisons,
        data_moves=tracker.data_moves,
        is_stable=False,
        time_complexity_best="O(N log N)",
        time_complexity_avg="O(N log N)",
        time_complexity_worst="O(N log N)",
        space_complexity="O(1)",
        stability_guarantee="Unstable (Heap tree swaps disrupt relative order)",
    )


# ==============================================================================
# 4. INSERTION SORT (Adaptive, Stable, O(N) best case, O(N^2) worst case)
# ==============================================================================
def insertion_sort(
    items: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> SortResult:
    """
    Insertion Sort: Adaptive, Stable.
    Extremely efficient for small arrays (N < 20) or nearly-sorted datasets.
    """
    arr = list(items)
    n = len(arr)
    tracker = _SortTracker(key, reverse)

    start_time = time.perf_counter()

    for i in range(1, n):
        current = arr[i]
        j = i - 1
        while j >= 0 and tracker.should_come_before(current, arr[j]):
            arr[j + 1] = arr[j]
            tracker.data_moves += 1
            j -= 1
        arr[j + 1] = current
        tracker.data_moves += 1

    elapsed_s = time.perf_counter() - start_time

    return SortResult(
        sorted_items=arr,
        algorithm_name="Insertion Sort",
        time_taken_ms=elapsed_s * 1000.0,
        time_taken_us=elapsed_s * 1_000_000.0,
        comparisons=tracker.comparisons,
        data_moves=tracker.data_moves,
        is_stable=True,
        time_complexity_best="O(N)",
        time_complexity_avg="O(N^2)",
        time_complexity_worst="O(N^2)",
        space_complexity="O(1)",
        stability_guarantee="Stable (Elements only slide past strictly smaller/larger keys)",
    )


# ==============================================================================
# 5. SELECTION SORT (Comparison Baseline, In-place O(N^2), Unstable)
# ==============================================================================
def selection_sort(
    items: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> SortResult:
    """
    Selection Sort: Repeatedly scans unsorted portion to find optimal element.
    Always does N*(N-1)/2 comparisons regardless of initial order.
    """
    arr = list(items)
    n = len(arr)
    tracker = _SortTracker(key, reverse)

    start_time = time.perf_counter()

    for i in range(n):
        best_idx = i
        for j in range(i + 1, n):
            if tracker.should_come_before(arr[j], arr[best_idx]):
                best_idx = j
        if best_idx != i:
            arr[i], arr[best_idx] = arr[best_idx], arr[i]
            tracker.data_moves += 2

    elapsed_s = time.perf_counter() - start_time

    return SortResult(
        sorted_items=arr,
        algorithm_name="Selection Sort",
        time_taken_ms=elapsed_s * 1000.0,
        time_taken_us=elapsed_s * 1_000_000.0,
        comparisons=tracker.comparisons,
        data_moves=tracker.data_moves,
        is_stable=False,
        time_complexity_best="O(N^2)",
        time_complexity_avg="O(N^2)",
        time_complexity_worst="O(N^2)",
        space_complexity="O(1)",
        stability_guarantee="Unstable (Long-distance swaps jump over equal elements)",
    )


# ==============================================================================
# 6. BUBBLE SORT (Baseline Comparison, In-place O(N^2), Stable)
# ==============================================================================
def bubble_sort(
    items: List[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> SortResult:
    """
    Bubble Sort: Adjacent comparisons and swaps with early-exit flag.
    Stable, but high number of operations.
    """
    arr = list(items)
    n = len(arr)
    tracker = _SortTracker(key, reverse)

    start_time = time.perf_counter()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if tracker.should_come_before(arr[j + 1], arr[j]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                tracker.data_moves += 2
                swapped = True
        if not swapped:
            break

    elapsed_s = time.perf_counter() - start_time

    return SortResult(
        sorted_items=arr,
        algorithm_name="Bubble Sort",
        time_taken_ms=elapsed_s * 1000.0,
        time_taken_us=elapsed_s * 1_000_000.0,
        comparisons=tracker.comparisons,
        data_moves=tracker.data_moves,
        is_stable=True,
        time_complexity_best="O(N)",
        time_complexity_avg="O(N^2)",
        time_complexity_worst="O(N^2)",
        space_complexity="O(1)",
        stability_guarantee="Stable (Only swaps strictly inverted adjacent pairs)",
    )


# Registry of all implemented sorting algorithms
ALGORITHMS = {
    "merge_sort": {
        "name": "Merge Sort",
        "func": merge_sort,
        "recommended": True,
        "is_stable": True,
        "complexity": "O(N log N)",
        "badge": "BEST (Stable, Guaranteed O(N log N))",
    },
    "quick_sort": {
        "name": "Quick Sort",
        "func": quick_sort,
        "recommended": False,
        "is_stable": False,
        "complexity": "O(N log N) avg",
        "badge": "Fast In-Place (Unstable)",
    },
    "heap_sort": {
        "name": "Heap Sort",
        "func": heap_sort,
        "recommended": False,
        "is_stable": False,
        "complexity": "O(N log N)",
        "badge": "O(1) Space (Unstable)",
    },
    "insertion_sort": {
        "name": "Insertion Sort",
        "func": insertion_sort,
        "recommended": False,
        "is_stable": True,
        "complexity": "O(N^2)",
        "badge": "Adaptive O(N) for nearly-sorted",
    },
    "selection_sort": {
        "name": "Selection Sort",
        "func": selection_sort,
        "recommended": False,
        "is_stable": False,
        "complexity": "O(N^2)",
        "badge": "Minimizes swaps, O(N^2) comparisons",
    },
    "bubble_sort": {
        "name": "Bubble Sort",
        "func": bubble_sort,
        "recommended": False,
        "is_stable": True,
        "complexity": "O(N^2)",
        "badge": "Simple baseline",
    },
}


def sort_employees(
    employees: List[Any],
    algorithm_key: str = "merge_sort",
    criterion_key: str = "performance",
    reverse: bool = True
) -> SortResult:
    """
    High-level orchestrator to sort employees by any attribute using any algorithm.
    """
    from .employee import CRITERIA_MAP

    if algorithm_key not in ALGORITHMS:
        algorithm_key = "merge_sort"

    if criterion_key not in CRITERIA_MAP:
        criterion_key = "performance"

    algo_info = ALGORITHMS[algorithm_key]
    crit_info = CRITERIA_MAP[criterion_key]

    sort_func = algo_info["func"]
    key_func = crit_info["key"]

    return sort_func(employees, key=key_func, reverse=reverse)
