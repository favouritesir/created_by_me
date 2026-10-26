"""
Cloud Merge Sort - Python Implementation
Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
"""

def c_merge(l, m, r, arr, cloud):
    """
    Core Cloud Merge Routine.
    Ascends left-half to overhead cloud buffer, then battles ground right-half.
    """
    if arr[m] <= arr[m + 1]:
        return

    lp = l
    rp = m + 1
    step = 0

    # Phase 1: Ascend left-half ground elements to overhead cloud
    while lp <= m:
        cloud[step] = arr[lp]
        step += 1
        lp += 1

    # Phase 2: In-situ battle between cloud and right-half ground
    lp = 0
    while lp < step and rp <= r:
        if cloud[lp] <= arr[rp]:
            arr[l] = cloud[lp]
            lp += 1
        else:
            arr[l] = arr[rp]
            rp += 1
        l += 1

    # Phase 3: Descend any remaining cloud elements back to ground
    # NOTE: Right-half elements (rp..r) require ZERO moves if cloud drains first!
    while lp < step:
        arr[l] = cloud[lp]
        lp += 1
        l += 1


def _cloud_merge_sort_rec(l, r, arr, cloud):
    if l < r:
        mid = (l + r) // 2
        _cloud_merge_sort_rec(l, mid, arr, cloud)
        _cloud_merge_sort_rec(mid + 1, r, arr, cloud)
        c_merge(l, mid, r, arr, cloud)


def cloud_merge_sort(arr):
    """
    Public API: Sorts list in-place using a single shared overhead cloud of size ceil(N/2).
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Single shared overhead cloud allocation: exactly ceil(N / 2)
    cloud_size = (n + 1) // 2
    cloud = [None] * cloud_size
    _cloud_merge_sort_rec(0, n - 1, arr, cloud)
    return arr


def standard_merge_sort(arr):
    """
    Canonical standard merge sort using full N auxiliary space and 4 loops.
    """
    n = len(arr)
    if n <= 1:
        return arr

    temp = [None] * n

    def _merge(l, m, r):
        if arr[m] <= arr[m + 1]:
            return
        lp, rp, k = l, m + 1, l
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

    def _rec(l, r):
        if l < r:
            mid = (l + r) // 2
            _rec(l, mid)
            _rec(mid + 1, r)
            _merge(l, mid, r)

    _rec(0, n - 1)
    return arr


if __name__ == "__main__":
    demo = [38, 27, 43, 3, 9, 82, 10, 19, 50, 61]
    print("Original:", demo)
    cloud_merge_sort(demo)
    print("Cloud Sorted:", demo)
