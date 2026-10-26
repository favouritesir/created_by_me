"""
================================================================================
Standard Textbook Merge Sort (Python Implementation)
================================================================================
"""

def standard_merge(l, m, r, arr, temp):
    if arr[m] <= arr[m + 1]:
        return

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


if __name__ == "__main__":
    demo = [38, 27, 43, 3, 9, 82, 10, 19, 50, 61]
    print("Original:       ", demo)
    standard_merge_sort(demo)
    print("Standard Sorted:", demo)
