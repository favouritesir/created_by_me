/**
 * ============================================================================
 * Cloud Merge Sort (JavaScript Implementation)
 * ============================================================================
 * Conceived by: Ashikur Rahman (Spring 2023, Green University of Bangladesh)
 * ============================================================================
 */

function cMerge(l, m, r, arr, cloud) {
    if (arr[m] <= arr[m + 1]) return;

    let lp = l;
    let cloudLen = 0;
    while (lp <= m) {
        cloud[cloudLen++] = arr[lp++];
    }

    let cp = 0;
    let rp = m + 1;
    while (cp < cloudLen && rp <= r) {
        if (cloud[cp] <= arr[rp]) {
            arr[l++] = cloud[cp++];
        } else {
            arr[l++] = arr[rp++];
        }
    }

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

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { cloudMergeSort, cMerge };
}

if (typeof require !== 'undefined' && require.main === module) {
    const demo = [38, 27, 43, 3, 9, 82, 10];
    console.log("Original:    ", demo);
    cloudMergeSort(demo);
    console.log("Cloud Sorted:", demo);
}
