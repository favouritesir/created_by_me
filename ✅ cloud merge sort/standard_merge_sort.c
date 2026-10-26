/**
 * ============================================================================
 * Standard Textbook Merge Sort (C Reference)
 * ============================================================================
 * Canonical 4-loop merge sort requiring a full-size N auxiliary buffer.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

void standard_merge(int arr[], int l, int m, int r, int temp[]) {
    if (arr[m] <= arr[m + 1]) return;

    int lp = l;
    int rp = m + 1;
    int k = l;

    // Loop 1: Compare elements into temp
    while (lp <= m && rp <= r) {
        if (arr[lp] <= arr[rp]) temp[k++] = arr[lp++];
        else temp[k++] = arr[rp++];
    }

    // Loop 2: Drain remaining first partition into temp
    while (lp <= m) temp[k++] = arr[lp++];

    // Loop 3: Drain remaining second partition into temp
    while (rp <= r) temp[k++] = arr[rp++];

    // Loop 4: Copy entire merged slice back from temp to arr
    for (int i = l; i <= r; i++) {
        arr[i] = temp[i];
    }
}

static void standard_merge_sort_rec(int arr[], int l, int r, int temp[]) {
    if (l < r) {
        int mid = l + (r - l) / 2;
        standard_merge_sort_rec(arr, l, mid, temp);
        standard_merge_sort_rec(arr, mid + 1, r, temp);
        standard_merge(arr, l, mid, r, temp);
    }
}

void standard_merge_sort(int arr[], int n) {
    if (n <= 1) return;
    int *temp = (int *)malloc(n * sizeof(int));
    if (!temp) return;

    standard_merge_sort_rec(arr, 0, n - 1, temp);

    free(temp);
}

int main() {
    int arr[] = {38, 27, 43, 3, 9, 82, 10, 19, 50, 61};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original Array:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n\n");

    standard_merge_sort(arr, n);

    printf("Sorted with Standard Merge Sort:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
