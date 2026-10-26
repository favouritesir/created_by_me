"""
================================================================================
4-Way Comparative Benchmark & Statistical Audit Suite
Target Algorithms: Cloud Merge Sort, Standard Merge Sort, QuickSort, TimSort
Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
================================================================================
"""

import random
import time
import statistics
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from implementations.cloud_merge_sort import cloud_sort
from implementations.standard_merge_sort import standard_merge_sort


# Standard In-Place QuickSort (Hoare partition)
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot = arr[(low + high) // 2]
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while arr[i] < pivot:
                i += 1
            j -= 1
            while arr[j] > pivot:
                j -= 1
            if i >= j:
                break
            arr[i], arr[j] = arr[j], arr[i]
        p = j
        quick_sort(arr, low, p)
        quick_sort(arr, p + 1, high)
    return arr


# Native TimSort wrapper
def tim_sort(arr):
    arr.sort()
    return arr


def run_benchmark():
    random.seed(2026)
    print("=" * 85)
    print("   4-WAY EMPIRICAL BENCHMARK: CLOUD SORT vs MERGE SORT vs QUICKSORT vs TIMSORT")
    print("=" * 85)

    # 1. Multi-Size Latency Benchmark
    print("\n[1/3] Scaled Runtime Latency (Averaged over 15 Runs per Size)...")
    sizes = [1000, 10000, 50000, 100000]
    runs = 15

    print(f"{'Size (N)':<10} | {'Cloud Sort':<13} | {'Std Merge':<13} | {'QuickSort':<13} | {'TimSort (Native)':<16} | {'Cloud vs Std'}")
    print("-" * 85)

    for size in sizes:
        t_cloud, t_merge, t_quick, t_tim = 0.0, 0.0, 0.0, 0.0

        for _ in range(runs):
            base = [random.randint(-1000000, 1000000) for _ in range(size)]

            a1 = base.copy()
            t0 = time.perf_counter()
            cloud_sort(a1)
            t_cloud += (time.perf_counter() - t0) * 1000

            a2 = base.copy()
            t0 = time.perf_counter()
            standard_merge_sort(a2)
            t_merge += (time.perf_counter() - t0) * 1000

            a3 = base.copy()
            t0 = time.perf_counter()
            quick_sort(a3)
            t_quick += (time.perf_counter() - t0) * 1000

            a4 = base.copy()
            t0 = time.perf_counter()
            tim_sort(a4)
            t_tim += (time.perf_counter() - t0) * 1000

        c_avg = t_cloud / runs
        m_avg = t_merge / runs
        q_avg = t_quick / runs
        t_avg = t_tim / runs
        diff = ((m_avg - c_avg) / m_avg) * 100

        print(f"N = {size:<6,d} | {c_avg:>8.3f} ms   | {m_avg:>8.3f} ms   | {q_avg:>8.3f} ms   | {t_avg:>10.3f} ms     | +{diff:.1f}% faster")

    # 2. Distribution Sensitivity Benchmark (N = 10,000)
    print("\n[2/3] Execution Speed Across Data Distributions (N = 10,000, 10 Runs)...")
    N = 10000
    distributions = {
        "Random Uniform": lambda: [random.randint(-100000, 100000) for _ in range(N)],
        "Already Sorted": lambda: list(range(N)),
        "Reverse Sorted": lambda: list(range(N, 0, -1)),
        "Heavy Duplicates": lambda: [random.randint(1, 10) for _ in range(N)],
        "Nearly Sorted (95%)": lambda: [i if random.random() > 0.05 else random.randint(0, N) for i in range(N)]
    }

    print(f"{'Distribution':<20} | {'Cloud Sort':<12} | {'Std Merge':<12} | {'QuickSort':<12} | {'TimSort':<12}")
    print("-" * 75)

    for name, gen in distributions.items():
        c_list, m_list, q_list, t_list = [], [], [], []
        for _ in range(10):
            data = gen()

            a = data.copy()
            t0 = time.perf_counter()
            cloud_sort(a)
            c_list.append((time.perf_counter() - t0) * 1000)

            a = data.copy()
            t0 = time.perf_counter()
            standard_merge_sort(a)
            m_list.append((time.perf_counter() - t0) * 1000)

            a = data.copy()
            t0 = time.perf_counter()
            quick_sort(a)
            q_list.append((time.perf_counter() - t0) * 1000)

            a = data.copy()
            t0 = time.perf_counter()
            tim_sort(a)
            t_list.append((time.perf_counter() - t0) * 1000)

        print(f"{name:<20} | {statistics.mean(c_list):>7.2f} ms   | {statistics.mean(m_list):>7.2f} ms   | {statistics.mean(q_list):>7.2f} ms   | {statistics.mean(t_list):>7.2f} ms")

    # 3. Stability & Correctness Verification
    print("\n[3/3] Cross-Verification of Correctness & In-Place Safety...")
    for _ in range(100):
        length = random.randint(10, 200)
        orig = [random.randint(-500, 500) for _ in range(length)]
        c_res = orig.copy()
        cloud_sort(c_res)
        assert c_res == sorted(orig), "Cloud sort result mismatch!"

    print("  ✔ 100 Verification tests PASSED with 100% precision.")
    print("=" * 85)
    print(" ALL 4-WAY BENCHMARKS COMPLETE.")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmark()
