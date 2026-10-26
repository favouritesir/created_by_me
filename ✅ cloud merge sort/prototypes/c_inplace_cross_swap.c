/**
 * ============================================================================
 * Cloud Sort Precursor: Pure In-Place Cross-Swap Trial (C)
 * ============================================================================
 * Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * Historical Context:
 *   An early exploratory attempt at achieving 100% in-place merge sorting
 *   without auxiliary memory buffers by applying bidirectional pointer swaps
 *   (bd) and crossed neighbor rotations (cross).
 *
 * Outcome:
 *   Partially sorted ~70-80% of arrays, but demonstrated the theoretical
 *   need for dedicated buffer headroom to guarantee strictly stable O(N log N)
 *   worst-case runtime without cascaded shift cascades. Led directly to the
 *   overhead cloud concept.
 * ============================================================================
 */

#include <stdio.h>

int temp;

void swap(int l, int r, int arr[]) {
    if (arr[l] > arr[r]) {
        temp = arr[l];
        arr[l] = arr[r];
        arr[r] = temp;
    }
}

void printarr(int l, int r, int arr[]) {
    while (l <= r) printf("%d ", arr[l++]);
    printf("\n");
}

void cross(int l, int r, int arr[]) {
    while (l < r) swap(l++, l + 1, arr);
    l = 0;
    while (l < r) swap(l++, l + 1, arr);
}

void bd(int l, int r, int m, int arr[]) {
    int lp = l + 1, rp = m + 1, ll = l, rr = r;
    while (ll < rr) swap(ll++, rr--, arr);
    while (lp <= m) swap(lp++, rp++, arr);
}

void divided(int l, int r, int arr[]) {
    if (l < r) {
        int m = (l + r) / 2;
        bd(l, r, m, arr);
        cross(l, r, arr);
        divided(l, m, arr);
        divided(m + 1, r, arr);
    }
}

int main() {
    int arr[] = {40, 39, 5, 27, 47, 35, 51, 58, 59, 64, 52, 37, 34, 31, 48, 25, 23, 8};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original array:\n");
    printarr(0, n - 1, arr);

    divided(0, n - 1, arr);

    printf("Array after in-place cross-swap experiment:\n");
    printarr(0, n - 1, arr);

    return 0;
}
