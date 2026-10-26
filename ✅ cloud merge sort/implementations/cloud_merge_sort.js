/**
 * ============================================================================
 * Cloud Merge Sort vs Standard Merge Sort (JavaScript Implementation)
 * ============================================================================
 * Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * This file contains BOTH clean implementations side-by-side without any
 * benchmark/test instrumentation overhead.
 * ============================================================================
 */

/* ============================================================================
 * 1. CLOUD MERGE SORT (Ashikur Rahman)
 *    - Auxiliary buffer: ceil(N / 2) elements
 *    - Merge loops: exactly 3 loops
 * ============================================================================ */

function cMerge(l, m, r, arr, cloud) {
    if (arr[m] <= arr[m + 1]) return;

    // Phase 1: Lift left-half elements to overhead cloud
    let lp = l;
    let cloudLen = 0;
    while (lp <= m) {
        cloud[cloudLen++] = arr[lp++];
    }

    // Phase 2: In-situ battle between overhead cloud and ground right-half
    let cp = 0;
    let rp = m + 1;
    while (cp < cloudLen && rp <= r) {
        if (cloud[cp] <= arr[rp]) {
            arr[l++] = cloud[cp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

    // Phase 3: Descend remaining cloud elements
    // (If cloud finishes first, right-half is already in final place: 0 moves!)
    while (cp < cloudLen) {
        arr[l++] = cloud[cp++];
    }
}

function cloudMergeSortRec(l, r, arr, cloud) {
    if (l < r) {
        const mid = Math.floor((l + r) / 2);
        cloudMergeSortRec(l, mid, arr, cloud);
        cloudMergeSortRec(mid + 1, r, arr, cloud);
        cMerge(l, mid, r, arr, cloud);
    }
}

function cloudMergeSort(arr) {
    const n = arr.length;
    if (n <= 1) return arr;
    const cloud = new Array(Math.ceil(n / 2));
    cloudMergeSortRec(0, n - 1, arr, cloud);
    return arr;
}


/* ============================================================================
 * 2. STANDARD TEXTBOOK MERGE SORT (Canonical Reference)
 *    - Auxiliary buffer: full N elements
 *    - Merge loops: 4 loops
 * ============================================================================ */

function standardMerge(l, m, r, arr, temp) {
    if (arr[m] <= arr[m + 1]) return;

    let lp = l;
    let rp = m + 1;
    let k = l;

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
    for (let i = l; i <= r; i++) {
        arr[i] = temp[i];
    }
}

function standardMergeSortRec(l, r, arr, temp) {
    if (l < r) {
        const mid = Math.floor((l + r) / 2);
        standardMergeSortRec(l, mid, arr, temp);
        standardMergeSortRec(mid + 1, r, arr, temp);
        standardMerge(l, mid, r, arr, temp);
    }
}

function standardMergeSort(arr) {
    const n = arr.length;
    if (n <= 1) return arr;
    const temp = new Array(n);
    standardMergeSortRec(0, n - 1, arr, temp);
    return arr;
}


/* ============================================================================
 * EXPORTS & CLI DEMO
 * ============================================================================ */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { cloudMergeSort, standardMergeSort, cMerge, standardMerge };
}

if (typeof require !== 'undefined' && require.main === module) {
    const a1 = [38, 27, 43, 3, 9, 82, 10];
    const a2 = [38, 27, 43, 3, 9, 82, 10];
    console.log("Original:     ", a1);
    cloudMergeSort(a1);
    console.log("Cloud Sorted:   ", a1);
    standardMergeSort(a2);
    console.log("Standard Sorted:", a2);
}
