/**
 * ============================================================================
 * Cloud Merge Sort (C Reference)
 * ============================================================================
 * Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * Architecture:
 *   - Ground Array (arr)  : The in-situ buffer where recursive partitioning occurs
 *   - Overhead Cloud      : A single floating buffer allocated once at root
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

void c_merge(int arr[], int l, int m, int r, int cloud[]) {
    if (arr[m] <= arr[m + 1]) return;

    int lp = l;
    int cloud_len = 0;
    while (lp <= m) {
        cloud[cloud_len++] = arr[lp++];
    }

    int cp = 0;
    int rp = m + 1;
    while (cp < cloud_len && rp <= r) {
        if (cloud[cp] <= arr[rp]) {
            arr[l++] = cloud[cp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

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

int main() {
    int arr[] = {38, 27, 43, 3, 9, 82, 10, 19, 50, 61};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original Array:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n\n");

    cloud_merge_sort(arr, n);

    printf("Sorted with Cloud Merge Sort:\n  ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
