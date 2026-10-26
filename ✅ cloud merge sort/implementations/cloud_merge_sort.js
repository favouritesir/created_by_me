/**
 * ============================================================================
 * Cloud Sort (JavaScript Implementation)
 * ============================================================================
 * Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * Core Concept:
 *   - Ground Array (arr) : Primary in-situ array to sort
 *   - Overhead Cloud     : Passed by caller, size ceil(N / 2)
 * ============================================================================
 */

function cloudMerge(l, m, r, arr, cloud) {
    let lp = l, rp = m + 1, step = 0;

    // Phase 1: arr[l..m] ascends to cloud
    while (lp <= m) {
        cloud[step++] = arr[lp++];
    }

    // Phase 2: In-situ merge between cloud and ground
    lp = 0;
    while (lp < step && rp <= r) {
        if (cloud[lp] <= arr[rp]) {
            arr[l++] = cloud[lp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

    // Phase 3: Drain remaining cloud elements (ground right tail needs 0 moves)
    while (lp < step) {
        arr[l++] = cloud[lp++];
    }
}

function cloudSort(arr, l, r, cloud) {
    if (l === undefined) {
        // Ergonomic caller default: cloudSort(arr)
        l = 0;
        r = arr.length - 1;
        cloud = new Array(Math.ceil(arr.length / 2));
    }
    if (l < r) {
        const mid = Math.floor((l + r) / 2);
        cloudSort(arr, l, mid, cloud);
        cloudSort(arr, mid + 1, r, cloud);
        cloudMerge(l, mid, r, arr, cloud);
    }
    return arr;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { cloudSort, cloudMerge };
}
