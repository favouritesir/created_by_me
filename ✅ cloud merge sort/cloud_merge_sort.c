/**
 * ============================================================================
 * Cloud Merge Sort vs Standard Merge Sort (C Reference)
 * ============================================================================
 * Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * This file contains BOTH clean implementations side-by-side:
 *   1. cloud_merge_sort()    : The modern 3-loop, ⌊N/2⌋ auxiliary overhead merge.
 *   2. standard_merge_sort() : The canonical 4-loop, N auxiliary textbook merge.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

/* ============================================================================
 * 1. CLOUD MERGE SORT (Ashikur Rahman)
 *    - Auxiliary buffer: ceil(N / 2) elements
 *    - Merge loops: exactly 3 loops (Right-side drain loop is 0 lines)
 * ============================================================================ */

void c_merge(int arr[], int l, int m, int r, int cloud[]) {
    // Optimization: Already sorted across boundary
    if (arr[m] <= arr[m + 1]) return;

    // Phase 1: Lift left-half elements to overhead cloud
    int lp = l;
    int cloud_len = 0;
    while (lp <= m) {
        cloud[cloud_len++] = arr[lp++];
    }

    // Phase 2: In-situ battle between overhead cloud and ground right-half
    int cp = 0;
    int rp = m + 1;
    while (cp < cloud_len && rp <= r) {
        if (cloud[cp] <= arr[rp]) {
            arr[l++] = cloud[cp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

    // Phase 3: Descend remaining cloud elements
    // (If cloud finishes first, right-half is already in final place: 0 moves!)
    while (cp < cloud_len) {
        arr[l++] = cloud[cp++];
    }
}

static void cloud_merge_sort_rec(int arr[], int l, int r, int cloud[]) {
    if (l < r) {
        int mid = l + (r - l) / 2;
        cloud_merge_sort_rec(arr, l, mid, cloud);
        cloud_merge_sort_rec(arr, mid + 1, r, cloud);
        c_merge(arr, l, mid, r, cloud);
    }
}

void cloud_merge_sort(int arr[], int n) {
    if (n <= 1) return;
    int cloud_size = (n + 1) / 2;
    int *cloud = (int *)malloc(cloud_size * sizeof(int));
    if (!cloud) return;

    cloud_merge_sort_rec(arr, 0, n - 1, cloud);

    free(cloud);
}


/* ============================================================================
 * 2. STANDARD TEXTBOOK MERGE SORT (Canonical Reference)
 *    - Auxiliary buffer: full N elements
 *    - Merge loops: 4 loops (Compare + Left Drain + Right Drain + Full Back-Copy)
 * ============================================================================ */

void standard_merge(int arr[], int l, int m, int r, int temp[]) {
    if (arr[m] <= arr[m + 1]) return;

    int lp = l;
    int rp = m + 1;
    int k = l;

    // Loop 1: Compare into temp
    while (lp <= m && rp <= r) {
        if (arr[lp] <= arr[rp]) temp[k++] = arr[lp++];
        else temp[k++] = arr[rp++];
    }

    // Loop 2: Drain left half into temp
    while (lp <= m) temp[k++] = arr[lp++];

    // Loop 3: Drain right half into temp (mandatory in standard!)
    while (rp <= r) temp[k++] = arr[rp++];

    // Loop 4: Copy entire merged range back from temp to arr
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


/* ============================================================================
 * DEMONSTRATION & COMPARISON
 * ============================================================================ */
int main() {
    int arr1[] = {38, 27, 43, 3, 9, 82, 10, 19, 50, 61};
    int arr2[] = {38, 27, 43, 3, 9, 82, 10, 19, 50, 61};
    int n = sizeof(arr1) / sizeof(arr1[0]);

    printf("Original Input Array:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr1[i]);
    printf("\n\n");

    cloud_merge_sort(arr1, n);
    printf("1. Sorted with Cloud Merge Sort (Aux Space: %d ints, 3 loops):\n  ", (n + 1) / 2);
    for (int i = 0; i < n; i++) printf("%d ", arr1[i]);
    printf("\n\n");

    standard_merge_sort(arr2, n);
    printf("2. Sorted with Standard Merge Sort (Aux Space: %d ints, 4 loops):\n  ", n);
    for (int i = 0; i < n; i++) printf("%d ", arr2[i]);
    printf("\n");

    return 0;
}
