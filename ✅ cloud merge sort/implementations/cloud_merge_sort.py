"""
================================================================================
Cloud Sort (Python Implementation)
================================================================================
Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)

Core Concept:
  - Ground Array (arr) : Primary in-situ array to sort
  - Overhead Cloud     : Passed by caller, size ceil(N / 2)
================================================================================
"""

def cloud_merge(l, m, r, arr, cloud):
    lp = l
    rp = m + 1
    step = 0

    # Phase 1: arr[l..m] ascends to overhead cloud
    while lp <= m:
        cloud[step] = arr[lp]
        step += 1
        lp += 1

    # Phase 2: In-situ merge between cloud and ground
    lp = 0
    while lp < step and rp <= r:
        if cloud[lp] <= arr[rp]:
            arr[l] = cloud[lp]
            lp += 1
        else:
            arr[l] = arr[rp]
            rp += 1
        l += 1

    # Phase 3: Drain remaining cloud elements (ground right tail needs 0 moves)
    while lp < step:
        arr[l] = cloud[lp]
        lp += 1
        l += 1


def cloud_sort(arr, l=0, r=None, cloud=None):
    if r is None:
        r = len(arr) - 1
        cloud = [None] * ((len(arr) + 1) // 2)

    if l < r:
        mid = (l + r) // 2
        cloud_sort(arr, l, mid, cloud)
        cloud_sort(arr, mid + 1, r, cloud)
        cloud_merge(l, mid, r, arr, cloud)
    return arr
