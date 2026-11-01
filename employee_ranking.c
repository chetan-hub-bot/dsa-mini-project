/**
 * ============================================================================
 * Symbiosis Institute of Technology (SIT) - Department of CSE
 * CS201: Data Structures and Algorithms - Lab CA-2 Experiential Learning
 * 
 * Task 35: Employee Ranking System
 * Student: Mani Chetan | PRN: 25070725016
 * 
 * Implements pure DSA sorting algorithms from scratch in ANSI/ISO C99:
 * 1. Merge Sort (Primary Recommended - Stable, Invariant O(N log N))
 * 2. Quick Sort (In-place with Median-of-Three Pivot - Unstable, O(N log N) avg)
 * 3. Heap Sort (Binary Max-Heap Selection - Unstable, In-place O(N log N))
 * 4. Insertion Sort (Adaptive O(N) best case - Stable, O(N^2))
 * 5. Selection Sort (Minimal swaps - Unstable, O(N^2))
 * 6. Bubble Sort (Adjacent pass with swapped flag - Stable, O(N^2))
 * ============================================================================
 */

#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#define MAX_NAME_LEN 32
#define MAX_DEPT_LEN 24
#define MAX_ID_LEN 16
#define SAMPLE_SIZE 25

/* -------------------------------------------------------------------------
 * Data Model: Employee Record
 * ------------------------------------------------------------------------- */
typedef struct {
    char emp_id[MAX_ID_LEN];
    char name[MAX_NAME_LEN];
    char department[MAX_DEPT_LEN];
    double salary;
    double experience_years;
    double performance_rating; // 1.0 to 5.0 scale
    double composite_score;    // 0.0 to 100.0 weighted score
} Employee;

/* -------------------------------------------------------------------------
 * Telemetry Tracker for Academic Analysis (Comparisons & Data Moves)
 * ------------------------------------------------------------------------- */
typedef struct {
    long long comparisons;
    long long data_moves;
    double time_ms;
    double time_us;
    bool is_stable;
    const char *algo_name;
    const char *complexity;
} SortTelemetry;

/* Function pointer type for flexible sorting criteria */
typedef int (*CompareFn)(const Employee *a, const Employee *b);

/* High-resolution timer compatible with POSIX (Colab/Linux) and standard C */
static double get_time_in_ms(void) {
#if defined(CLOCK_MONOTONIC)
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1000.0 + (double)ts.tv_nsec / 1000000.0;
#else
    return ((double)clock() / (double)CLOCKS_PER_SEC) * 1000.0;
#endif
}

/* Calculate multi-factor composite score:
 * 50% Performance (norm 5.0), 30% Experience (norm 25 yrs), 20% Salary (norm $200k) */
double calculate_composite_score(double rating, double exp, double salary) {
    double norm_perf = rating / 5.0;
    if (norm_perf > 1.0) norm_perf = 1.0;
    if (norm_perf < 0.0) norm_perf = 0.0;

    double norm_exp = exp / 25.0;
    if (norm_exp > 1.0) norm_exp = 1.0;
    if (norm_exp < 0.0) norm_exp = 0.0;

    double norm_salary = salary / 200000.0;
    if (norm_salary > 1.0) norm_salary = 1.0;
    if (norm_salary < 0.0) norm_salary = 0.0;

    double weighted = (norm_perf * 0.50) + (norm_exp * 0.30) + (norm_salary * 0.20);
    return weighted * 100.0;
}

/* Helper to initialize an Employee record */
Employee create_employee(const char *id, const char *name, const char *dept,
                        double salary, double exp, double rating) {
    Employee emp;
    strncpy(emp.emp_id, id, sizeof(emp.emp_id) - 1);
    emp.emp_id[sizeof(emp.emp_id) - 1] = '\0';

    strncpy(emp.name, name, sizeof(emp.name) - 1);
    emp.name[sizeof(emp.name) - 1] = '\0';

    strncpy(emp.department, dept, sizeof(emp.department) - 1);
    emp.department[sizeof(emp.department) - 1] = '\0';

    emp.salary = salary;
    emp.experience_years = exp;
    emp.performance_rating = rating;
    emp.composite_score = calculate_composite_score(rating, exp, salary);
    return emp;
}

/* -------------------------------------------------------------------------
 * Comparison Comparators (Descending Order for Ranking)
 * Return:
 *   < 0 if 'a' has higher priority than 'b' (should come first)
 *   > 0 if 'b' has higher priority than 'a'
 *   = 0 if identical
 * ------------------------------------------------------------------------- */
int cmp_by_performance_desc(const Employee *a, const Employee *b) {
    if (a->performance_rating > b->performance_rating) return -1;
    if (a->performance_rating < b->performance_rating) return 1;
    return 0; // Equal
}

int cmp_by_salary_desc(const Employee *a, const Employee *b) {
    if (a->salary > b->salary) return -1;
    if (a->salary < b->salary) return 1;
    return 0;
}

int cmp_by_experience_desc(const Employee *a, const Employee *b) {
    if (a->experience_years > b->experience_years) return -1;
    if (a->experience_years < b->experience_years) return 1;
    return 0;
}

int cmp_by_composite_desc(const Employee *a, const Employee *b) {
    if (a->composite_score > b->composite_score) return -1;
    if (a->composite_score < b->composite_score) return 1;
    return 0;
}

/* -------------------------------------------------------------------------
 * 1. MERGE SORT (Chosen Best Algorithm - Stable, Invariant O(N log N))
 * ------------------------------------------------------------------------- */
static void merge(Employee arr[], Employee temp[], int left, int mid, int right,
                 CompareFn cmp, SortTelemetry *t) {
    int i = left;
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        t->comparisons++;
        /* CRUCIAL FOR STABILITY:
         * If cmp <= 0, element from left sub-array is picked first.
         * Equal elements preserve their original relative positioning. */
        if (cmp(&arr[i], &arr[j]) <= 0) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
        t->data_moves++;
    }

    while (i <= mid) {
        temp[k++] = arr[i++];
        t->data_moves++;
    }

    while (j <= right) {
        temp[k++] = arr[j++];
        t->data_moves++;
    }

    for (i = left; i <= right; i++) {
        arr[i] = temp[i];
        t->data_moves++;
    }
}

static void merge_sort_recursive(Employee arr[], Employee temp[], int left, int right,
                                CompareFn cmp, SortTelemetry *t) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        merge_sort_recursive(arr, temp, left, mid, cmp, t);
        merge_sort_recursive(arr, temp, mid + 1, right, cmp, t);
        merge(arr, temp, left, mid, right, cmp, t);
    }
}

SortTelemetry merge_sort(Employee arr[], int n, CompareFn cmp) {
    SortTelemetry t = {0, 0, 0.0, 0.0, true, "Merge Sort", "O(N log N)"};
    if (n <= 1) return t;

    Employee *temp = (Employee *)malloc(n * sizeof(Employee));
    if (!temp) {
        fprintf(stderr, "Error: Memory allocation failed for Merge Sort.\n");
        return t;
    }

    double start = get_time_in_ms();
    merge_sort_recursive(arr, temp, 0, n - 1, cmp, t);
    double elapsed = get_time_in_ms() - start;

    t.time_ms = elapsed;
    t.time_us = elapsed * 1000.0;
    free(temp);
    return t;
}

/* -------------------------------------------------------------------------
 * 2. QUICK SORT (Median-of-Three Pivot - Unstable, O(N log N) avg)
 * ------------------------------------------------------------------------- */
static void swap_emp(Employee *a, Employee *b, SortTelemetry *t) {
    Employee tmp = *a;
    *a = *b;
    *b = tmp;
    t->data_moves += 3;
}

static int median_of_three(Employee arr[], int low, int high, CompareFn cmp, SortTelemetry *t) {
    int mid = low + (high - low) / 2;
    t->comparisons++;
    if (cmp(&arr[low], &arr[mid]) > 0) swap_emp(&arr[low], &arr[mid], t);
    t->comparisons++;
    if (cmp(&arr[low], &arr[high]) > 0) swap_emp(&arr[low], &arr[high], t);
    t->comparisons++;
    if (cmp(&arr[mid], &arr[high]) > 0) swap_emp(&arr[mid], &arr[high], t);
    return mid;
}

static int partition(Employee arr[], int low, int high, CompareFn cmp, SortTelemetry *t) {
    int pivot_idx = median_of_three(arr, low, high, cmp, t);
    swap_emp(&arr[pivot_idx], &arr[high], t);
    Employee pivot = arr[high];

    int i = low - 1;
    for (int j = low; j < high; j++) {
        t->comparisons++;
        if (cmp(&arr[j], &pivot) <= 0) {
            i++;
            swap_emp(&arr[i], &arr[j], t);
        }
    }
    swap_emp(&arr[i + 1], &arr[high], t);
    return (i + 1);
}

static void quick_sort_recursive(Employee arr[], int low, int high, CompareFn cmp, SortTelemetry *t) {
    if (low < high) {
        int pi = partition(arr, low, high, cmp, t);
        quick_sort_recursive(arr, low, pi - 1, cmp, t);
        quick_sort_recursive(arr, pi + 1, high, cmp, t);
    }
}

SortTelemetry quick_sort(Employee arr[], int n, CompareFn cmp) {
    SortTelemetry t = {0, 0, 0.0, 0.0, false, "Quick Sort", "O(N log N)"};
    if (n <= 1) return t;

    double start = get_time_in_ms();
    quick_sort_recursive(arr, 0, n - 1, cmp, t);
    double elapsed = get_time_in_ms() - start;

    t.time_ms = elapsed;
    t.time_us = elapsed * 1000.0;
    return t;
}

/* -------------------------------------------------------------------------
 * 3. HEAP SORT (In-place Binary Heap - Unstable, O(N log N))
 * ------------------------------------------------------------------------- */
static void heapify(Employee arr[], int n, int i, CompareFn cmp, SortTelemetry *t) {
    int target = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    /* For descending sorted order, we maintain a min-heap root at bottom */
    if (left < n) {
        t->comparisons++;
        if (cmp(&arr[left], &arr[target]) > 0) target = left;
    }
    if (right < n) {
        t->comparisons++;
        if (cmp(&arr[right], &arr[target]) > 0) target = right;
    }

    if (target != i) {
        swap_emp(&arr[i], &arr[target], t);
        heapify(arr, n, target, cmp, t);
    }
}

SortTelemetry heap_sort(Employee arr[], int n, CompareFn cmp) {
    SortTelemetry t = {0, 0, 0.0, 0.0, false, "Heap Sort", "O(N log N)"};
    if (n <= 1) return t;

    double start = get_time_in_ms();
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i, cmp, t);
    }
    for (int i = n - 1; i > 0; i--) {
        swap_emp(&arr[0], &arr[i], t);
        heapify(arr, i, 0, cmp, t);
    }
    double elapsed = get_time_in_ms() - start;

    t.time_ms = elapsed;
    t.time_us = elapsed * 1000.0;
    return t;
}

/* -------------------------------------------------------------------------
 * 4. INSERTION SORT (Adaptive, Stable, O(N^2))
 * ------------------------------------------------------------------------- */
SortTelemetry insertion_sort(Employee arr[], int n, CompareFn cmp) {
    SortTelemetry t = {0, 0, 0.0, 0.0, true, "Insertion Sort", "O(N^2)"};
    if (n <= 1) return t;

    double start = get_time_in_ms();
    for (int i = 1; i < n; i++) {
        Employee key = arr[i];
        t.data_moves++;
        int j = i - 1;

        while (j >= 0) {
            t.comparisons++;
            if (cmp(&key, &arr[j]) < 0) {
                arr[j + 1] = arr[j];
                t.data_moves++;
                j--;
            } else {
                break;
            }
        }
        arr[j + 1] = key;
        t.data_moves++;
    }
    double elapsed = get_time_in_ms() - start;

    t.time_ms = elapsed;
    t.time_us = elapsed * 1000.0;
    return t;
}

/* -------------------------------------------------------------------------
 * 5. SELECTION SORT (Minimal Swaps - Unstable, O(N^2))
 * ------------------------------------------------------------------------- */
SortTelemetry selection_sort(Employee arr[], int n, CompareFn cmp) {
    SortTelemetry t = {0, 0, 0.0, 0.0, false, "Selection Sort", "O(N^2)"};
    if (n <= 1) return t;

    double start = get_time_in_ms();
    for (int i = 0; i < n - 1; i++) {
        int best_idx = i;
        for (int j = i + 1; j < n; j++) {
            t.comparisons++;
            if (cmp(&arr[j], &arr[best_idx]) < 0) {
                best_idx = j;
            }
        }
        if (best_idx != i) {
            swap_emp(&arr[i], &arr[best_idx], t);
        }
    }
    double elapsed = get_time_in_ms() - start;

    t.time_ms = elapsed;
    t.time_us = elapsed * 1000.0;
    return t;
}

/* -------------------------------------------------------------------------
 * 6. BUBBLE SORT (Early Exit Flag - Stable, O(N^2))
 * ------------------------------------------------------------------------- */
SortTelemetry bubble_sort(Employee arr[], int n, CompareFn cmp) {
    SortTelemetry t = {0, 0, 0.0, 0.0, true, "Bubble Sort", "O(N^2)"};
    if (n <= 1) return t;

    double start = get_time_in_ms();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            t.comparisons++;
            if (cmp(&arr[j + 1], &arr[j]) < 0) {
                swap_emp(&arr[j], &arr[j + 1], t);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    double elapsed = get_time_in_ms() - start;

    t.time_ms = elapsed;
    t.time_us = elapsed * 1000.0;
    return t;
}

/* -------------------------------------------------------------------------
 * Sample Dataset: 25 Pre-Loaded Corporate Records
 * ------------------------------------------------------------------------- */
int load_sample_employees(Employee list[]) {
    list[0]  = create_employee("EMP001", "Aarav Sharma",   "Engineering",  135000.0,  7.5, 4.8);
    list[1]  = create_employee("EMP002", "Priya Patel",    "Data Science", 142000.0,  6.0, 4.9);
    list[2]  = create_employee("EMP003", "Rohan Verma",    "Product",      115000.0,  5.0, 4.2);
    list[3]  = create_employee("EMP004", "Ananya Iyer",    "Engineering",  165000.0, 11.0, 4.7);
    list[4]  = create_employee("EMP005", "Vikram Singh",   "Finance",       95000.0,  4.5, 3.8);
    list[5]  = create_employee("EMP006", "Neha Gupta",     "Marketing",     88000.0,  3.0, 4.1);
    list[6]  = create_employee("EMP007", "Kabir Reddy",    "Engineering",  125000.0,  6.5, 4.5);
    list[7]  = create_employee("EMP008", "Sanya Malhotra", "HR",            82000.0,  4.0, 4.6);
    list[8]  = create_employee("EMP009", "Aditya Roy",     "Sales",        105000.0,  5.5, 3.9);
    list[9]  = create_employee("EMP010", "Tanvi Joshi",    "Product",      138000.0,  8.0, 4.7);
    list[10] = create_employee("EMP011", "Karan Kapoor",   "Finance",      152000.0, 12.0, 4.4);
    list[11] = create_employee("EMP012", "Rhea Desai",     "Data Science", 120000.0,  4.5, 4.8);
    list[12] = create_employee("EMP013", "Arjun Nair",     "Engineering",   78000.0,  2.0, 3.6);
    list[13] = create_employee("EMP014", "Ishita Sen",     "Marketing",    110000.0,  6.5, 4.3);
    list[14] = create_employee("EMP015", "Manish Mehta",   "Sales",         92000.0,  3.5, 4.0);
    list[15] = create_employee("EMP016", "Sneha Kulkarni", "HR",            98000.0,  6.0, 4.5);
    list[16] = create_employee("EMP017", "Dev Mukherjee",  "Engineering",  180000.0, 14.0, 4.9);
    list[17] = create_employee("EMP018", "Meera Chopra",   "Product",       99000.0,  3.0, 3.7);
    list[18] = create_employee("EMP019", "Yash Singhania", "Finance",       87000.0,  2.5, 3.9);
    list[19] = create_employee("EMP020", "Pooja Bansal",   "Data Science", 160000.0,  9.5, 4.8);
    list[20] = create_employee("EMP021", "Rajesh Khanna",  "Sales",        130000.0,  8.5, 4.2);
    list[21] = create_employee("EMP022", "Tara Sundaram",  "Engineering",  102000.0,  4.0, 4.4);
    list[22] = create_employee("EMP023", "Gaurav Bhatt",   "Marketing",     76000.0,  1.5, 3.5);
    list[23] = create_employee("EMP024", "Divya Menon",    "HR",           112000.0,  7.0, 4.6);
    list[24] = create_employee("EMP025", "Siddharth Rao",  "Engineering",  148000.0,  8.5, 4.7);
    return SAMPLE_SIZE;
}

/* Generate synthetic cohort for empirical benchmarks */
Employee *generate_synthetic_employees(int n, unsigned int seed) {
    srand(seed);
    const char *depts[] = {"Engineering", "Data Science", "Product", "Marketing", "Sales", "HR", "Finance"};
    const char *names[] = {"Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Neha", "Kabir", "Sanya", "Karan", "Tanvi"};

    Employee *arr = (Employee *)malloc(n * sizeof(Employee));
    if (!arr) return NULL;

    for (int i = 0; i < n; i++) {
        char id[16];
        snprintf(id, sizeof(id), "SYN%05d", i + 1);

        char name[32];
        snprintf(name, sizeof(name), "%s_%d", names[rand() % 10], i + 1);

        const char *dept = depts[rand() % 7];
        double exp = 1.0 + ((double)(rand() % 190) / 10.0); // 1.0 to 20.0 yrs
        double salary = 45000.0 + (exp * 6500.0) + (rand() % 25000);
        double rating = 2.0 + ((double)(rand() % 31) / 10.0); // 2.0 to 5.0

        arr[i] = create_employee(id, name, dept, salary, exp, rating);
    }
    return arr;
}

/* -------------------------------------------------------------------------
 * Formatted Display Routines
 * ------------------------------------------------------------------------- */
void print_separator(char c, int len) {
    for (int i = 0; i < len; i++) putchar(c);
    putchar('\n');
}

void print_employee_table(const Employee list[], int count, const char *title) {
    printf("\n");
    print_separator('=', 95);
    printf("  %s\n", title);
    print_separator('=', 95);
    printf("%-5s | %-8s | %-18s | %-13s | %-12s | %-9s | %-7s | %-6s\n",
           "Rank", "ID", "Name", "Department", "Salary ($)", "Exp", "Rating", "Score");
    print_separator('-', 95);

    for (int i = 0; i < count; i++) {
        char rank_badge[16];
        if (i == 0) snprintf(rank_badge, sizeof(rank_badge), "#1 [GOLD]");
        else if (i == 1) snprintf(rank_badge, sizeof(rank_badge), "#2 [SLVR]");
        else if (i == 2) snprintf(rank_badge, sizeof(rank_badge), "#3 [BRNZ]");
        else snprintf(rank_badge, sizeof(rank_badge), "#%d", i + 1);

        printf("%-5s | %-8s | %-18s | %-13s | $%10.2f | %4.1f yrs | %4.1f   | %5.1f\n",
               rank_badge,
               list[i].emp_id,
               list[i].name,
               list[i].department,
               list[i].salary,
               list[i].experience_years,
               list[i].performance_rating,
               list[i].composite_score);
    }
    print_separator('=', 95);
}

void print_telemetry(const SortTelemetry *t, int count) {
    printf("\n>>> TELEMETRY FOR %s <<<\n", t->algo_name);
    printf("  * Records Sorted   : %d\n", count);
    printf("  * Execution Time   : %.4f ms (%.1f us)\n", t->time_ms, t->time_us);
    printf("  * Key Comparisons  : %lld\n", t->comparisons);
    printf("  * Data Moves/Swaps : %lld\n", t->data_moves);
    printf("  * Stability        : %s\n", t->is_stable ? "STABLE (Preserves ties)" : "UNSTABLE (Scrambles ties)");
    printf("  * Complexity Class : %s\n", t->complexity);
}

/* -------------------------------------------------------------------------
 * Empirical Benchmark across All 6 Algorithms
 * ------------------------------------------------------------------------- */
void run_empirical_benchmark(int n) {
    printf("\n");
    print_separator('=', 95);
    printf("  EMPIRICAL BENCHMARK SUITE: ALL 6 ALGORITHMS (N = %d RECORDS)\n", n);
    print_separator('=', 95);
    printf("%-16s | %-10s | %-14s | %-12s | %-10s | %s\n",
           "Algorithm", "Time (ms)", "Comparisons", "Data Moves", "Stability", "Complexity");
    print_separator('-', 95);

    Employee *base = generate_synthetic_employees(n, 42);
    if (!base) {
        printf("Memory allocation error.\n");
        return;
    }

    /* Algorithm 1: Merge Sort */
    Employee *arr1 = (Employee *)malloc(n * sizeof(Employee));
    memcpy(arr1, base, n * sizeof(Employee));
    SortTelemetry t1 = merge_sort(arr1, n, cmp_by_performance_desc);
    printf("%-16s | %10.3f | %14lld | %12lld | %-10s | %s [RECOMMENDED]\n",
           t1.algo_name, t1.time_ms, t1.comparisons, t1.data_moves, "STABLE", t1.complexity);
    free(arr1);

    /* Algorithm 2: Quick Sort */
    Employee *arr2 = (Employee *)malloc(n * sizeof(Employee));
    memcpy(arr2, base, n * sizeof(Employee));
    SortTelemetry t2 = quick_sort(arr2, n, cmp_by_performance_desc);
    printf("%-16s | %10.3f | %14lld | %12lld | %-10s | %s\n",
           t2.algo_name, t2.time_ms, t2.comparisons, t2.data_moves, "UNSTABLE", t2.complexity);
    free(arr2);

    /* Algorithm 3: Heap Sort */
    Employee *arr3 = (Employee *)malloc(n * sizeof(Employee));
    memcpy(arr3, base, n * sizeof(Employee));
    SortTelemetry t3 = heap_sort(arr3, n, cmp_by_performance_desc);
    printf("%-16s | %10.3f | %14lld | %12lld | %-10s | %s\n",
           t3.algo_name, t3.time_ms, t3.comparisons, t3.data_moves, "UNSTABLE", t3.complexity);
    free(arr3);

    /* Algorithm 4: Insertion Sort */
    Employee *arr4 = (Employee *)malloc(n * sizeof(Employee));
    memcpy(arr4, base, n * sizeof(Employee));
    SortTelemetry t4 = insertion_sort(arr4, n, cmp_by_performance_desc);
    printf("%-16s | %10.3f | %14lld | %12lld | %-10s | %s\n",
           t4.algo_name, t4.time_ms, t4.comparisons, t4.data_moves, "STABLE", t4.complexity);
    free(arr4);

    /* Algorithm 5: Selection Sort */
    Employee *arr5 = (Employee *)malloc(n * sizeof(Employee));
    memcpy(arr5, base, n * sizeof(Employee));
    SortTelemetry t5 = selection_sort(arr5, n, cmp_by_performance_desc);
    printf("%-16s | %10.3f | %14lld | %12lld | %-10s | %s\n",
           t5.algo_name, t5.time_ms, t5.comparisons, t5.data_moves, "UNSTABLE", t5.complexity);
    free(arr5);

    /* Algorithm 6: Bubble Sort */
    Employee *arr6 = (Employee *)malloc(n * sizeof(Employee));
    memcpy(arr6, base, n * sizeof(Employee));
    SortTelemetry t6 = bubble_sort(arr6, n, cmp_by_performance_desc);
    printf("%-16s | %10.3f | %14lld | %12lld | %-10s | %s\n",
           t6.algo_name, t6.time_ms, t6.comparisons, t6.data_moves, "STABLE", t6.complexity);
    free(arr6);

    print_separator('=', 95);
    free(base);
}

/* -------------------------------------------------------------------------
 * Academic Viva Justification: Why Merge Sort was Chosen
 * ------------------------------------------------------------------------- */
void print_why_merge_sort(void) {
    printf("\n");
    print_separator('=', 95);
    printf("  ACADEMIC JUSTIFICATION: WHY MERGE SORT WAS CHOSEN FOR TASK 35\n");
    print_separator('=', 95);
    printf("1. CRUCIAL STABILITY GUARANTEE:\n");
    printf("   - In employee appraisals, multiple records share identical ratings (e.g. 4.8 / 5.0).\n");
    printf("   - Merge Sort strictly preserves the prior relative order of equal records.\n");
    printf("   - Quick Sort and Heap Sort are inherently UNSTABLE, scrambling preexisting seniority.\n\n");
    printf("2. GUARANTEED O(N log N) WORST-CASE BOUND:\n");
    printf("   - Recurrence: T(N) = 2T(N/2) + O(N) --> Master Theorem Case 2: Theta(N log N).\n");
    printf("   - Naive QuickSort degrades to O(N^2) on duplicate-dense inputs. Merge Sort NEVER degrades.\n\n");
    printf("3. REPRODUCIBILITY & AUDIT COMPLIANCE:\n");
    printf("   - Financial audit rules require deterministic outcomes for bonus pools.\n");
    printf("   - Merge Sort trades O(N) auxiliary memory (<15 MB for 100k items) for complete determinism.\n");
    print_separator('=', 95);
}

/* -------------------------------------------------------------------------
 * Main Demonstration Flow (Engineered for Google Colab and ANSI Terminal)
 * ------------------------------------------------------------------------- */
int main(void) {
    Employee dataset[SAMPLE_SIZE];
    int count = load_sample_employees(dataset);

    printf("\n================================================================================\n");
    printf("        SYMBIOSIS INSTITUTE OF TECHNOLOGY (SIT) - DEPARTMENT OF CSE            \n");
    printf("           CS201: DATA STRUCTURES AND ALGORITHMS - LAB CA-2 REPORT             \n");
    printf("            TASK 35: EMPLOYEE RANKING SYSTEM (MERGE SORT ENGINE)               \n");
    printf("================================================================================\n");
    printf("Student Name : Mani Chetan\n");
    printf("PRN Number   : 25070725016\n");
    printf("Course       : CS201 Data Structures and Algorithms (CO3, CO4, CO5)\n");
    printf("Date         : 2026-11-01\n");
    print_separator('=', 80);

    /* 1. Initial Unsorted Records */
    print_employee_table(dataset, 8, "INITIAL EMPLOYEE DIRECTORY (PREVIEW OF FIRST 8 OF 25 RECORDS)");

    /* 2. Primary Ranking by Performance Rating using Merge Sort */
    SortTelemetry t_perf = merge_sort(dataset, count, cmp_by_performance_desc);
    print_employee_table(dataset, count, "RANKED BY PERFORMANCE RATING (1.0 TO 5.0 DESCENDING) [MERGE SORT]");
    print_telemetry(&t_perf, count);

    /* 3. Ranking by Salary using Merge Sort */
    SortTelemetry t_sal = merge_sort(dataset, count, cmp_by_salary_desc);
    print_employee_table(dataset, 8, "RANKED BY ANNUAL SALARY ($ DESCENDING) [PREVIEW TOP 8]");
    print_telemetry(&t_sal, count);

    /* 4. Ranking by Composite Weighted Score */
    SortTelemetry t_comp = merge_sort(dataset, count, cmp_by_composite_desc);
    print_employee_table(dataset, 8, "RANKED BY COMPOSITE SCORE (50% PERF + 30% EXP + 20% SALARY) [TOP 8]");
    print_telemetry(&t_comp, count);

    /* 5. Empirical Benchmark on N = 1,000 Records */
    run_empirical_benchmark(1000);

    /* 6. Academic Justification & Viva Notes */
    print_why_merge_sort();

    printf("\n[SUCCESS] All operations completed. Ready for Google Colab demonstration!\n\n");
    return 0;
}
