/**
 * ============================================================================
 * Standard Textbook Merge Sort (JavaScript Implementation)
 * ============================================================================
 */

function standardMerge(l, m, r, arr, temp) {
    let lp = l, rp = m + 1, k = l;

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

function standardMergeSort(arr, l, r, temp) {
    if (l === undefined) {
        l = 0;
        r = arr.length - 1;
        temp = new Array(arr.length);
    }
    if (l < r) {
        const mid = Math.floor((l + r) / 2);
        standardMergeSort(arr, l, mid, temp);
        standardMergeSort(arr, mid + 1, r, temp);
        standardMerge(l, mid, r, arr, temp);
    }
    return arr;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { standardMergeSort, standardMerge };
}
