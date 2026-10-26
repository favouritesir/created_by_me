/**
 * ============================================================================
 * Standard Textbook Merge Sort (C Reference)
 * ============================================================================
 * Canonical 4-loop merge sort requiring a full-size N auxiliary buffer.
 * ============================================================================
 */

void standard_merge(int arr[], int l, int m, int r, int temp[]) {
    int lp = l, rp = m + 1, k = l;

    // Loop 1: Compare into temp
    while (lp <= m && rp <= r) {
        if (arr[lp] <= arr[rp]) temp[k++] = arr[lp++];
        else temp[k++] = arr[rp++];
    }

    // Loop 2: Drain remaining left side into temp
    while (lp <= m) temp[k++] = arr[lp++];

    // Loop 3: Drain remaining right side into temp
    while (rp <= r) temp[k++] = arr[rp++];

    // Loop 4: Copy entire merged slice back from temp to arr
    for (int i = l; i <= r; i++) {
        arr[i] = temp[i];
    }
}

void standard_merge_sort(int arr[], int l, int r, int temp[]) {
    if (l < r) {
        int mid = l + (r - l) / 2;
        standard_merge_sort(arr, l, mid, temp);
        standard_merge_sort(arr, mid + 1, r, temp);
        standard_merge(arr, l, mid, r, temp);
    }
}
