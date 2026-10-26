"""
================================================================================
Standard Textbook Merge Sort (Python Implementation)
================================================================================
"""

def standard_merge(l, m, r, arr, temp):
    lp = l
    rp = m + 1
    k = l

    while lp <= m and rp <= r:
        if arr[lp] <= arr[rp]:
            temp[k] = arr[lp]
            lp += 1
        else:
            temp[k] = arr[rp]
            rp += 1
        k += 1

    while lp <= m:
        temp[k] = arr[lp]
        lp += 1
        k += 1

    while rp <= r:
        temp[k] = arr[rp]
        rp += 1
        k += 1

    for i in range(l, r + 1):
        arr[i] = temp[i]


def standard_merge_sort(arr, l=0, r=None, temp=None):
    if r is None:
        r = len(arr) - 1
        temp = [None] * len(arr)

    if l < r:
        mid = (l + r) // 2
        standard_merge_sort(arr, l, mid, temp)
        standard_merge_sort(arr, mid + 1, r, temp)
        standard_merge(l, mid, r, arr, temp)
    return arr
