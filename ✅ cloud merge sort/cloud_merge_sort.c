/**
 * ============================================================================
 * Cloud Sort (C Reference)
 * ============================================================================
 * Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * Core Concept:
 *   - Ground Array (arr) : Primary in-situ array to sort
 *   - Overhead Cloud     : A caller-passed floating buffer of size ceil(N / 2)
 *                          Zero malloc/free needed; pure pedagogical elegance.
 * ============================================================================
 */

void cloud_merge(int arr[], int l, int m, int r, int cloud[]) {
    int lp = l, rp = m + 1, step = 0;

    // Phase 1: arr[l..m] temporarily ascends to overhead cloud
    while (lp <= m) {
        cloud[step++] = arr[lp++];
    }

    // Phase 2: In-situ merge between overhead cloud and ground
    lp = 0;
    while (lp < step && rp <= r) {
        if (cloud[lp] <= arr[rp]) {
            arr[l++] = cloud[lp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

    // Phase 3: Unload remaining cloud elements (ground right tail needs 0 moves)
    while (lp < step) {
        arr[l++] = cloud[lp++];
    }
}

void cloud_sort(int arr[], int l, int r, int cloud[]) {
    if (l < r) {
        int mid = l + (r - l) / 2;
        cloud_sort(arr, l, mid, cloud);
        cloud_sort(arr, mid + 1, r, cloud);
        cloud_merge(arr, l, mid, r, cloud);
    }
}
