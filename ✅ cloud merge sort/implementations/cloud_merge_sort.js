/**
 * Cloud Merge Sort - JavaScript Implementation
 * Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 */

/**
 * Core Cloud Merge Routine
 * @param {number} l - Left boundary
 * @param {number} m - Midpoint
 * @param {number} r - Right boundary
 * @param {Array} arr - The Ground array
 * @param {Array} cloud - The Overhead Cloud buffer
 */
function cMerge(l, m, r, arr, cloud) {
    if (arr[m] <= arr[m + 1]) return;

    let lp = l;
    let rp = m + 1;
    let step = 0;

    // Phase 1: Ascend left-half ground elements to overhead cloud
    while (lp <= m) {
        cloud[step++] = arr[lp++];
    }

    // Phase 2: In-situ battle between cloud and right-half ground
    lp = 0;
    while (lp < step && rp <= r) {
        if (cloud[lp] <= arr[rp]) {
            arr[l++] = cloud[lp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

    // Phase 3: Descend any remaining cloud elements back to ground
    // Note: If cloud drains first, right-half is ALREADY in final place! Zero moves!
    while (lp < step) {
        arr[l++] = cloud[lp++];
    }
}

function cloudMergeSortRecursive(l, r, arr, cloud) {
    if (l < r) {
        const mid = Math.floor((l + r) / 2);
        cloudMergeSortRecursive(l, mid, arr, cloud);
        cloudMergeSortRecursive(mid + 1, r, arr, cloud);
        cMerge(l, mid, r, arr, cloud);
    }
}

/**
 * Public Cloud Merge Sort API
 * @param {Array} arr - Array to sort in-place
 */
function cloudMergeSort(arr) {
    const n = arr.length;
    if (n <= 1) return arr;

    // Single shared overhead cloud allocation: exactly ceil(N / 2)
    const cloud = new Array(Math.ceil(n / 2));
    cloudMergeSortRecursive(0, n - 1, arr, cloud);
    return arr;
}

/**
 * Standard Merge Sort (Included for comparison)
 */
function standardMerge(l, m, r, arr, temp) {
    if (arr[m] <= arr[m + 1]) return;
    let lp = l, rp = m + 1, k = l;
    while (lp <= m && rp <= r) {
        if (arr[lp] <= arr[rp]) temp[k++] = arr[lp++];
        else temp[k++] = arr[rp++];
    }
    while (lp <= m) temp[k++] = arr[lp++];
    while (rp <= r) temp[k++] = arr[rp++];
    for (let i = l; i <= r; i++) arr[i] = temp[i];
}

function standardMergeSortRecursive(l, r, arr, temp) {
    if (l < r) {
        const mid = Math.floor((l + r) / 2);
        standardMergeSortRecursive(l, mid, arr, temp);
        standardMergeSortRecursive(mid + 1, r, arr, temp);
        standardMerge(l, mid, r, arr, temp);
    }
}

function standardMergeSort(arr) {
    const n = arr.length;
    if (n <= 1) return arr;
    const temp = new Array(n);
    standardMergeSortRecursive(0, n - 1, arr, temp);
    return arr;
}

// Module exports for test runners
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { cloudMergeSort, standardMergeSort, cMerge };
}

// Demo CLI run
if (typeof require !== 'undefined' && require.main === module) {
    const demo = [38, 27, 43, 3, 9, 82, 10];
    console.log("Original:", demo);
    cloudMergeSort(demo);
    console.log("Cloud Sorted:", demo);
}
