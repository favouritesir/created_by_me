"""
================================================================================
Cloud Merge Sort vs Standard Merge Sort (Python Implementation)
================================================================================
Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)

This file contains BOTH clean implementations side-by-side without any
benchmark/test instrumentation overhead.
================================================================================
"""

# ==============================================================================
# 1. CLOUD MERGE SORT (Ashikur Rahman)
#    - Auxiliary buffer: ceil(N / 2) elements
#    - Merge loops: exactly 3 loops
# ==============================================================================

def c_merge(l, m, r, arr, cloud):
    if arr[m] <= arr[m + 1]:
        return

    # Phase 1: Lift left-half elements to overhead cloud
    lp = l
    cloud_len = 0
    while lp <= m:
        cloud[cloud_len] = arr[lp]
        cloud_len += 1
        lp += 1

    # Phase 2: In-situ battle between overhead cloud and ground right-half
    cp = 0
    rp = m + 1
    while cp < cloud_len and rp <= r:
        if cloud[cp] <= arr[rp]:
            arr[l] = cloud[cp]
            cp += 1
        else:
            arr[l] = arr[rp]
            rp += 1
        l += 1

    # Phase 3: Descend remaining cloud elements
    # (If cloud finishes first, right-half is already in final place: 0 moves!)
    while cp < cloud_len:
        arr[l] = cloud[cp]
        cp += 1
        l += 1


def _cloud_merge_sort_rec(l, r, arr, cloud):
    if l < r:
        mid = (l + r) // 2
        _cloud_merge_sort_rec(l, mid, arr, cloud)
        _cloud_merge_sort_rec(mid + 1, r, arr, cloud)
        c_merge(l, mid, r, arr, cloud)


def cloud_merge_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    cloud_size = (n + 1) // 2
    cloud = [None] * cloud_size
    _cloud_merge_sort_rec(0, n - 1, arr, cloud)
    return arr


# ==============================================================================
# 2. STANDARD TEXTBOOK MERGE SORT (Canonical Reference)
#    - Auxiliary buffer: full N elements
#    - Merge loops: 4 loops
# ==============================================================================

def standard_merge(l, m, r, arr, temp):
    if arr[m] <= arr[m + 1]:
        return

    lp = l
    rp = m + 1
    k = l

    # Loop 1: Compare into temp
    while lp <= m and rp <= r:
        if arr[lp] <= arr[rp]:
            temp[k] = arr[lp]
            lp += 1
        else:
            temp[k] = arr[rp]
            rp += 1
        k += 1

    # Loop 2: Drain left half into temp
    while lp <= m:
        temp[k] = arr[lp]
        lp += 1
        k += 1

    # Loop 3: Drain right half into temp (mandatory in standard!)
    while rp <= r:
        temp[k] = arr[rp]
        rp += 1
        k += 1

    # Loop 4: Copy entire merged range back from temp to arr
    for i in range(l, r + 1):
        arr[i] = temp[i]


def _standard_merge_sort_rec(l, r, arr, temp):
    if l < r:
        mid = (l + r) // 2
        _standard_merge_sort_rec(l, mid, arr, temp)
        _standard_merge_sort_rec(mid + 1, r, arr, temp)
        standard_merge(l, mid, r, arr, temp)


def standard_merge_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    temp = [None] * n
    _standard_merge_sort_rec(0, n - 1, arr, temp)
    return arr


# ==============================================================================
# DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    a1 = [38, 27, 43, 3, 9, 82, 10, 19, 50, 61]
    a2 = [38, 27, 43, 3, 9, 82, 10, 19, 50, 61]
    print("Original:       ", a1)
    cloud_merge_sort(a1)
    print("Cloud Sorted:   ", a1)
    standard_merge_sort(a2)
    print("Standard Sorted:", a2)
