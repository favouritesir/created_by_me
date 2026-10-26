/**
 * ============================================================================
 * Cloud Sort Precursor: Queue-Merge (qMarge) Experiment (JavaScript)
 * ============================================================================
 * Author: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 *
 * Historical Context:
 *   Explored rotational queue-like element swapping (qMarge) where partition
 *   elements were shifted and swapped in steps to simulate FIFO consumption.
 *   Contains the early move-counter instrumentation comparing standard merge,
 *   quick sort, and cloud merge.
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

// Queue-based rotational merge prototype
function qMarge(l, m, r, arr) {
    let lp = l, rp = m + 1, step = 0;
    while (step < m / 2) swap(r - step, rp + step++, arr);
    lp = rp = r;
    swap(l++, lp--, arr);
    while (l + 1 < lp) {
        if (arr[lp] < arr[rp]) {
            swap(l++, lp--, arr);
        } else {
            swap(l++, rp--, arr);
            if (rp - 1 < lp) rp = l;
        }
    }
    while (rp <= r) {
        swap(l++, rp++, arr);
    }
}

function queueSort(l, r, arr) {
    const mid = Math.floor((l + r) / 2);
    if (l < r) {
        queueSort(l, mid, arr);
        queueSort(mid + 1, r, arr);
        qMarge(l, mid, r, arr);
    }
}

const testArray = [9, 3, 7, 5, 6, 1, 8, 2];
console.log("Before queueSort:", testArray.join(", "));
queueSort(0, testArray.length - 1, testArray);
console.log("After queueSort: ", testArray.join(", "));

module.exports = { queueSort, qMarge };
