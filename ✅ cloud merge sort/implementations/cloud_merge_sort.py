"""
================================================================================
Cloud Merge Sort (Python Implementation)
================================================================================
Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
================================================================================
"""

def c_merge(l, m, r, arr, cloud):
    if arr[m] <= arr[m + 1]:
        return

    lp = l
    cloud_len = 0
    while lp <= m:
        cloud[cloud_len] = arr[lp]
        cloud_len += 1
        lp += 1

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


if __name__ == "__main__":
    demo = [38, 27, 43, 3, 9, 82, 10, 19, 50, 61]
    print("Original:    ", demo)
    cloud_merge_sort(demo)
    print("Cloud Sorted:", demo)
