// ============================================================================
// IN-PLACE INFIX TO PREFIX CONVERTER - JavaScript Implementation
// Author  : Ashikur Rahman (2026)
// Concept : O(N) Time, O(1) auxiliary string space (two-pointer, right-to-left)
//
// Note: JavaScript strings are immutable, so the in-place technique operates on
// a character array that stands in for the original C-style string buffer.
// The read/write pointer discipline is identical to the C version.
// ============================================================================

'use strict';

const MAX = 100;

function priority(op) {
    if (op === '+' || op === '-') return 1;
    if (op === '*' || op === '/' || op === '%') return 2;
    if (op === '^') return 3;
    return 0;
}

function isRightAssociative(op) {
    return op === '^';
}

// Core Algorithm: In-place Infix to Prefix (operates on arr = char array)
function makePrefixInPlace(arr) {
    const len = arr.length;
    let readIdx = len - 1;   // moves right to left, reading characters
    let writeIdx = len - 1;  // moves right to left, writing the output
    const stack = [];        // operator stack

    while (readIdx >= 0) {
        const current = arr[readIdx];

        if (current === ')') {
            stack.push(current);
        } else if (current === '(') {
            // Pop operators until the matching ')' is consumed; drop both parens
            while (stack.length > 0 && stack[stack.length - 1] !== ')') {
                arr[writeIdx--] = stack.pop(); // Write directly on the same array
            }
            if (stack.length > 0 && stack[stack.length - 1] === ')') {
                stack.pop();
            }
        } else if (priority(current) > 0) {
            // Operator handling with (inverted) associativity rules.
            // Left-associative: pop only on strictly greater precedence.
            // Right-associative (^): pop on greater or equal precedence.
            while (stack.length > 0 && stack[stack.length - 1] !== ')') {
                const topOp = stack[stack.length - 1];
                const pCurr = priority(current);
                const pTop = priority(topOp);
                if (pCurr < pTop || (pCurr === pTop && isRightAssociative(current))) {
                    arr[writeIdx--] = stack.pop();
                } else {
                    break;
                }
            }
            stack.push(current);
        } else if (/[a-zA-Z0-9]/.test(current)) {
            arr[writeIdx--] = current; // Operand: written immediately
        }

        readIdx--;
    }

    // Flush remaining operators from the stack
    while (stack.length > 0) {
        const x = stack.pop();
        if (x !== ')' && x !== '(') {
            arr[writeIdx--] = x;
        }
    }

    // The valid prefix result sits at the tail: shift it to index 0
    const newLen = len - 1 - writeIdx;
    let out = '';
    for (let i = writeIdx + 1; i < len; i++) {
        out += arr[i];
    }
    return { result: out, newLen };
}

// Convenience wrapper: takes an infix string, returns the prefix string
function infixToPrefix(expr) {
    const arr = expr.split('');
    const { result } = makePrefixInPlace(arr);
    return result;
}

module.exports = { infixToPrefix, makePrefixInPlace, priority, isRightAssociative, MAX };

// ---------------------------------------------------------------------------
// Demo mode: node implementations/infix_to_prefix.js
// ---------------------------------------------------------------------------
if (require.main === module) {
    const samples = ['(a-b/c)*(a/k-l)', 'A+B*C/D-E', 'A^B^C', 'a-b-c'];
    for (const s of samples) {
        console.log(`${s.padEnd(20)} => ${infixToPrefix(s)}`);
    }
}
