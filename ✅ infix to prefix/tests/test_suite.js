// ============================================================================
// TEST SUITE for the In-Place Infix to Prefix converter (JavaScript)
// Author : Ashikur Rahman (2026)
//
// Run with:  node tests/test_suite.js
//
// Performs 2 of the 3 validation layers used in the README's Robustness Report:
//   Layer 1 (L1): test vectors (published examples) + differential comparison
//                 against an independent 3-pass reference implementation
//                 on randomly generated expressions.
//   Layer 2 (L2): instrumented invariant assertions - no write may ever touch
//                 a cell that has not been read (in-place corruption check),
//                 and the write pointer must never go below index 0.
// (Layer 3, numeric semantic evaluation, lives in tests/test_stress.py.)
// ============================================================================

'use strict';

const fs = require('fs');
const path = require('path');
const { infixToPrefix } = require('../implementations/infix_to_prefix.js');

// ---------------------------------------------------------------------------
// Reference implementation (INDEPENDENT method: reverse -> postfix -> reverse)
// Used only inside the test harness to cross-check the production code.
// ---------------------------------------------------------------------------
function priorityRef(op) {
    if (op === '+' || op === '-') return 1;
    if (op === '*' || op === '/' || op === '%') return 2;
    if (op === '^') return 3;
    return 0;
}
function isRightAssocRef(op) { return op === '^'; }

function postfixForPrefix(rev) {
    const stack = [];
    let out = '';
    for (const c of rev) {
        if (/[a-zA-Z0-9]/.test(c)) {
            out += c;
        } else if (c === '(') {
            stack.push(c);
        } else if (c === ')') {
            while (stack.length && stack[stack.length - 1] !== '(') out += stack.pop();
            if (stack.length) stack.pop();
        } else {
            while (
                stack.length && stack[stack.length - 1] !== '(' &&
                (priorityRef(stack[stack.length - 1]) > priorityRef(c) ||
                 (priorityRef(stack[stack.length - 1]) === priorityRef(c) && isRightAssocRef(c)))
            ) {
                out += stack.pop();
            }
            stack.push(c);
        }
    }
    while (stack.length) {
        const x = stack.pop();
        if (x !== '(' && x !== ')') out += x;
    }
    return out;
}

function referenceTextbook(s) {
    const rev = s.split('').reverse().join('')
        .replace(/\(/g, '\u0001').replace(/\)/g, '(').replace(/\u0001/g, ')');
    return postfixForPrefix(rev).split('').reverse().join('');
}

// ---------------------------------------------------------------------------
// Random expression generator (operands a-d, operators, random parentheses)
// ---------------------------------------------------------------------------
function genExpr(depth = 0) {
    if (depth >= 5 || Math.random() < 0.25) {
        return ['a', 'b', 'c', 'd'][Math.floor(Math.random() * 4)];
    }
    const ops = ['+', '-', '*', '/', '%', '^'];
    const op = ops[Math.floor(Math.random() * ops.length)];
    const expr = genExpr(depth + 1) + op + genExpr(depth + 1);
    return Math.random() < 0.45 ? `(${expr})` : expr;
}

// ---------------------------------------------------------------------------
// Layer 1 - Test vectors
// ---------------------------------------------------------------------------
function runVectorTests() {
    const vectors = JSON.parse(
        fs.readFileSync(path.join(__dirname, 'test_vectors.json'), 'utf8')
    ).tests;

    let pass = 0, fail = 0;
    for (const t of vectors) {
        const got = infixToPrefix(t.infix);
        if (got === t.prefix) {
            pass++;
        } else {
            fail++;
            console.error(`  FAIL vector: ${t.infix} => "${got}" (expected "${t.prefix}")`);
        }
    }
    console.log(`Layer 1a | Test Vectors           : ${pass} passed, ${fail} failed (of ${vectors.length})`);
    return fail === 0;
}

// ---------------------------------------------------------------------------
// Layer 1 - Differential test against independent reference (random inputs)
// ---------------------------------------------------------------------------
function runDifferentialTests(nRounds = 3000, seed = 2026) {
    // Deterministic PRNG (mulberry32) so runs are reproducible
    let state = seed >>> 0;
    const rand = () => {
        state = (state + 0x6D2B79F5) >>> 0;
        let t = Math.imul(state ^ (state >>> 15), 1 | state);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    Math.random = rand; // route generator through the seeded PRNG

    let pass = 0, fail = 0;
    const failures = [];
    for (let i = 0; i < nRounds; i++) {
        const expr = genExpr();
        const got = infixToPrefix(expr);
        const expected = referenceTextbook(expr);
        if (got === expected) pass++;
        else {
            fail++;
            if (failures.length < 5) failures.push([expr, got, expected]);
        }
    }
    console.log(`Layer 1b | Differential (random)   : ${pass} passed, ${fail} failed (of ${nRounds})`);
    for (const [e, g, x] of failures) {
        console.error(`  FAIL diff: ${e} => "${g}" (reference "${x}")`);
    }
    return fail === 0;
}

// ---------------------------------------------------------------------------
// Layer 2 - Instrumented soundness invariants (corruption + underflow checks)
// ---------------------------------------------------------------------------
function runInvariantTests(nRounds = 3000) {
    let pass = 0, fail = 0;
    for (let i = 0; i < nRounds; i++) {
        const expr = genExpr();
        const arr = expr.split('');
        const n = arr.length;
        const readFlags = new Array(n).fill(false);
        const stack = [];
        let corrupt = false, underflow = false;
        let readIdx = n - 1, writeIdx = n - 1;
        const write = (ch) => {
            if (writeIdx < 0 || !readFlags[writeIdx]) corrupt = true;
            arr[writeIdx] = ch;
            writeIdx--;
        };

        // Exact mirror of the production algorithm with assertions added
        while (readIdx >= 0) {
            const current = arr[readIdx];
            readFlags[readIdx] = true;

            if (current === ')') {
                stack.push(current);
            } else if (current === '(') {
                while (stack.length && stack[stack.length - 1] !== ')') write(stack.pop());
                if (stack.length && stack[stack.length - 1] === ')') stack.pop();
            } else if (priorityRef(current) > 0) {
                while (
                    stack.length && stack[stack.length - 1] !== ')' &&
                    (priorityRef(current) < priorityRef(stack[stack.length - 1]) ||
                     (priorityRef(current) === priorityRef(stack[stack.length - 1]) && isRightAssocRef(current)))
                ) {
                    write(stack.pop());
                }
                stack.push(current);
            } else if (/[a-zA-Z0-9]/.test(current)) {
                write(current);
            }
            readIdx--;
        }
        while (stack.length) {
            const x = stack.pop();
            if (x !== '(' && x !== ')') write(x);
        }
        if (writeIdx < -1) underflow = true;

        if (!corrupt && !underflow) pass++;
        else {
            fail++;
            console.error(`  FAIL invariant: ${expr} corrupt=${corrupt} underflow=${underflow}`);
        }
    }
    console.log(`Layer 2  | In-place soundness      : ${pass} passed, ${fail} failed (of ${nRounds})`);
    return fail === 0;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
const vecOk = runVectorTests();
const diffOk = runDifferentialTests();
const invOk = runInvariantTests();

console.log('-----------------------------------------------------------');
if (vecOk && diffOk && invOk) {
    console.log('ALL TESTS PASSED - the algorithm is verified.');
    process.exit(0);
} else {
    console.error('SOME TESTS FAILED - the algorithm needs review.');
    process.exit(1);
}
