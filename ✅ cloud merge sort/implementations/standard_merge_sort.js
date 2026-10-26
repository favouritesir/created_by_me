/**
 * ============================================================================
 * Standard Textbook Merge Sort (JavaScript Implementation)
 * ============================================================================
 */

function standardMerge(l, m, r, arr, temp) {
    if (arr[m] <= arr[m + 1]) return;

    let lp = l;
    let rp = m + 1;
    let k = l;

    while (lp <= m && rp <= r) {
        if (arr[lp] <= arr[rp]) temp[k++] = arr[lp++];
        else temp[k++] = arr[rp++];
    }

    while (lp <= m) temp[k++] = arr[lp++];
    while (rp <= r) temp[k++] = arr[rp++];

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

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { standardMergeSort, standardMerge };
}

if (typeof require !== 'undefined' && require.main === module) {
    const demo = [38, 27, 43, 3, 9, 82, 10];
    console.log("Original:       ", demo);
    standardMergeSort(demo);
    console.log("Standard Sorted:", demo);
}
