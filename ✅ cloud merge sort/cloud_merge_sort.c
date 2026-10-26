/**
 * ============================================================================
 * Cloud Merge Sort (C Reference Implementation)
 * ============================================================================
 * Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 * Department of Computer Science and Engineering
 *
 * Conceptual Architecture:
 *   - Ground Array (arr)        : The in-situ buffer where recursive partitioning
 *                                 and final sorted writes happen.
 *   - Overhead Cloud (cloud)    : A single shared temporary buffer of size ceil(N/2).
 *                                 Left-half elements temporarily ascend to the
 *                                 cloud, then battle with in-situ right-half ground
 *                                 elements during sorted descent.
 *
 * Key Properties:
 *   1. Auxiliary Space          : exactly ceil(N/2) elements (50% reduction vs N).
 *   2. Loop Economy             : Only 3 loops per merge (Right tail needs ZERO drain).
 *   3. Stability                : Strictly stable (preserves identical key order).
 *   4. Pre-sorted Short-Circuit : O(N) best-case via arr[m] <= arr[m+1] guard.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * Core Cloud Merge Routine
 * Merges two sorted halves arr[l..m] and arr[m+1..r] using the overhead cloud buffer.
 */
void c_merge(int arr[], int l, int m, int r, int cloud[]) {
    // Optimization: If already sorted across boundary, no work needed.
    if (arr[m] <= arr[m + 1]) {
        return;
    }

    int lp = l;
    int rp = m + 1;
    int step = 0;

    // Phase 1: Ascend left-half ground elements to the overhead cloud
    while (lp <= m) {
        cloud[step++] = arr[lp++];
    }

    // Phase 2: In-situ battle between overhead cloud and ground right-half
    lp = 0;
    while (lp < step && rp <= r) {
        if (cloud[lp] <= arr[rp]) {
            arr[l++] = cloud[lp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

    // Phase 3: Descend any remaining cloud elements to ground
    // NOTE: Right-half elements (rp..r) require ZERO moves if cloud drains first!
    while (lp < step) {
        arr[l++] = cloud[lp++];
    }
}

/**
 * Recursive Cloud Merge Sort
 */
void cloud_merge_sort_recursive(int arr[], int l, int r, int cloud[]) {
    if (l < r) {
        int mid = l + (r - l) / 2;
        cloud_merge_sort_recursive(arr, l, mid, cloud);
        cloud_merge_sort_recursive(arr, mid + 1, r, cloud);
        c_merge(arr, l, mid, r, cloud);
    }
}

/**
 * Public API
 * Allocates a single shared overhead cloud buffer of size (n + 1) / 2.
 */
void cloud_merge_sort(int arr[], int n) {
    if (n <= 1) return;

    // Single shared overhead cloud allocation: exactly ceil(N / 2)
    int cloud_size = (n + 1) / 2;
    int *cloud = (int *)malloc(cloud_size * sizeof(int));
    if (!cloud) {
        fprintf(stderr, "Fatal: failed to allocate overhead cloud buffer.\n");
        return;
    }

    cloud_merge_sort_recursive(arr, 0, n - 1, cloud);

    free(cloud);
}

/**
 * Canonical Standard Merge Sort (Included for direct comparison)
 * Uses a full-size auxiliary buffer of N elements and 4 loops.
 */
void standard_merge(int arr[], int l, int m, int r, int temp[]) {
    if (arr[m] <= arr[m + 1]) return;

    int lp = l;
    int rp = m + 1;
    int k = l;

    // Loop 1: Compare both halves into temp
    while (lp <= m && rp <= r) {
        if (arr[lp] <= arr[rp]) temp[k++] = arr[lp++];
        else temp[k++] = arr[rp++];
    }
    // Loop 2: Drain remaining left half
    while (lp <= m) temp[k++] = arr[lp++];
    // Loop 3: Drain remaining right half (mandatory in standard!)
    while (rp <= r) temp[k++] = arr[rp++];
    // Loop 4: Copy entire merged slice back from temp to arr
    for (int i = l; i <= r; i++) {
        arr[i] = temp[i];
    }
}

void standard_merge_sort_recursive(int arr[], int l, int r, int temp[]) {
    if (l < r) {
        int mid = l + (r - l) / 2;
        standard_merge_sort_recursive(arr, l, mid, temp);
        standard_merge_sort_recursive(arr, mid + 1, r, temp);
        standard_merge(arr, l, mid, r, temp);
    }
}

void standard_merge_sort(int arr[], int n) {
    if (n <= 1) return;
    int *temp = (int *)malloc(n * sizeof(int));
    if (!temp) return;
    standard_merge_sort_recursive(arr, 0, n - 1, temp);
    free(temp);
}

// Simple Demo
int main() {
    int arr[] = {38, 27, 43, 3, 9, 82, 10, 19, 50, 61};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original Ground Array:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n\n");

    cloud_merge_sort(arr, n);

    printf("Sorted by Cloud Merge Sort:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
