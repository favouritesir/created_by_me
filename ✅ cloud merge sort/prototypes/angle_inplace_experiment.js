/**
 * ============================================================================
 * Cloud Sort Precursor: AngleSort In-Place Experiment (JavaScript)
 * ============================================================================
 * Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * Historical Context:
 *   Hand-simulated on door panels and notebook margins to test whether
 *   elements could be rotated into order across adjacent partitions using
 *   an angular sweep (angle) without allocating auxiliary scratchpads.
 *
 * Outcome:
 *   Verified the limits of in-situ element displacement and inspired the
 *   realization that vacating ground slots via an overhead buffer eliminates
 *   displacement conflicts entirely.
 * ============================================================================
 */

const swap = (i, j, arr) => {
    if (arr[i] > arr[j]) {
        const temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
        return 1;
    }
    return 0;
};

function cross(l, r, arr) {
    let stop = l;
    while (stop < r) {
        swap(l, l + 1, arr);
        swap(r - 1, r, arr);
        l++;
        r--;
    }
}

function angle(l, m, r, arr) {
    let lp = l, rp = m + 1;

    // Phase 1: Prepare partition boundaries
    while (lp <= m) swap(lp++, rp++, arr);

    if (l + 1 < r) {
        lp = m + 1;
        rp = m + 2;
        while (l <= m) {
            (arr[lp] < arr[rp]) ? swap(l, lp, arr) : swap(l, rp, arr);
            swap(lp, rp, arr);
            swap(lp, lp + 1, arr);
            if (arr[rp] > arr[rp + 1] && rp < r) rp++;
            l++;
        }
    } else {
        swap(l, r, arr);
    }
}

function angleSort(l, r, arr) {
    const mid = Math.floor((l + r) / 2);
    if (l < r) {
        angleSort(l, mid, arr);
        angleSort(mid + 1, r, arr);
        angle(l, mid, r, arr);
    }
}

// Sample trial run
const testArray = [14, 6, 9, 13, 1, 11, 7, 15, 3, 10, 16, 2, 4, 8, 12, 5];
console.log("Before angleSort:", testArray.join(", "));
angleSort(0, testArray.length - 1, testArray);
console.log("After angleSort: ", testArray.join(", "));

module.exports = { angleSort, angle, cross };
