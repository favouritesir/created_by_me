# ============================================================================
# FULL 3-LAYER STRESS TEST HARNESS for the In-Place Infix to Prefix converter
# Author : Ashikur Rahman (2026)
#
# Run with:  python tests/test_stress.py            (default: 40,000 expressions)
#            python tests/test_stress.py --n 20000  (smaller/faster run)
#
# Layers (as described in the README Robustness Report):
#   Layer 1 (L1): Differential - output compared against an INDEPENDENT 3-pass
#                 textbook implementation (reverse -> postfix -> reverse),
#                 itself pre-verified against published reference outputs.
#   Layer 2 (L2): Soundness - instrumented pointer tracing. Every write is
#                 asserted to target a previously-READ cell (in-place
#                 corruption check) at index >= 0 (underflow check).
#   Layer 3 (L3): Semantic truth - the raw infix string is evaluated with an
#                 independent recursive-descent parser and the produced prefix
#                 output is evaluated with a stack machine; values must agree.
# ============================================================================

import argparse
import random
import sys

# ---------------------------- Production logic ------------------------------
def priority(x):
    if x in ('+', '-'):
        return 1
    if x in ('*', '/', '%'):
        return 2
    if x == '^':
        return 3
    return 0

def is_right_assoc(op):
    return op == '^'

def in_place_sim(expr):
    """Exact mirror of the C algorithm with instrumentation for Layer 2."""
    s = list(expr)
    n = len(s)
    read_flags = [False] * n          # has this cell's content been read yet?
    stack = []
    corrupt = False                   # wrote into an unread cell
    underflow = False                 # wrote below index 0
    max_depth = 0
    r, w = n - 1, n - 1

    while r >= 0:
        c = s[r]
        read_flags[r] = True
        if c == ')':
            stack.append(c)
            if len(stack) > max_depth:
                max_depth = len(stack)
        elif c == '(':
            while stack and stack[-1] != ')':
                x = stack.pop()
                if w < 0 or not read_flags[w]:
                    corrupt = True
                s[w] = x
                w -= 1
            if stack and stack[-1] == ')':
                stack.pop()
        elif priority(c) > 0:
            while stack and stack[-1] != ')' and (
                (priority(c) < priority(stack[-1])) or
                (priority(c) == priority(stack[-1]) and is_right_assoc(c))):
                x = stack.pop()
                if w < 0 or not read_flags[w]:
                    corrupt = True
                s[w] = x
                w -= 1
            stack.append(c)
            if len(stack) > max_depth:
                max_depth = len(stack)
        elif c.isalnum():
            if w < 0 or not read_flags[w]:
                corrupt = True
            s[w] = c
            w -= 1
        r -= 1

    while stack:
        x = stack.pop()
        if x not in '()':
            if w < 0 or not read_flags[w]:
                corrupt = True
            s[w] = x
            w -= 1

    if w < -1:
        underflow = True
    new_len = n - 1 - w
    return ''.join(s[w+1:w+1+new_len]), corrupt, underflow, max_depth

# ---------------- Layer 1 reference (independent 3-pass method) -------------
def ref_textbook(s):
    def postfix_for_prefix(t):
        stack, out = [], []
        for c in t:
            if c.isalnum():
                out.append(c)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    out.append(stack.pop())
                if stack:
                    stack.pop()
            else:
                while stack and stack[-1] != '(' and (
                    priority(stack[-1]) > priority(c) or
                    (priority(stack[-1]) == priority(c) and is_right_assoc(c))):
                    out.append(stack.pop())
                stack.append(c)
        while stack:
            x = stack.pop()
            if x not in '()':
                out.append(x)
        return ''.join(out)
    rev = s[::-1].replace('(', '\x01').replace(')', '(').replace('\x01', ')')
    return postfix_for_prefix(rev)[::-1]

# ---------------- Layer 3 evaluators (independent of each other) ------------
class _Fail(Exception):
    pass

def eval_infix_string(expr):
    """Recursive-descent evaluator: '^' right-assoc highest, then * / %, then + -."""
    pos = [0]
    n = len(expr)

    def peek():
        return expr[pos[0]] if pos[0] < n else None

    def advance():
        pos[0] += 1

    def expr_primary():
        c = peek()
        if c is None:
            raise _Fail()
        if c == '(':
            advance()
            v = expr_sum()
            if peek() != ')':
                raise _Fail()
            advance()
            return v
        if c.isdigit():
            advance()
            return float(int(c))
        raise _Fail()

    def expr_pow():
        base = expr_primary()
        if base is None:
            return None
        if peek() == '^':
            advance()
            expo = expr_pow()  # right-associative
            if expo is None:
                return None
            if base == 0 and expo <= 0:
                return None
            try:
                r = base ** expo
                if isinstance(r, complex) or abs(r) > 1e15:
                    return None
                return r
            except (OverflowError, ValueError, ZeroDivisionError):
                return None
        return base

    def expr_term():
        v = expr_pow()
        while True:
            if v is None:
                return None
            c = peek()
            if c in ('*', '/', '%'):
                advance()
                rhs = expr_pow()
                if rhs is None:
                    return None
                if c == '*':
                    v = v * rhs
                else:
                    if rhs == 0:
                        return None
                    v = v / rhs if c == '/' else v % rhs
            else:
                return v

    def expr_sum():
        v = expr_term()
        while True:
            if v is None:
                return None
            c = peek()
            if c in ('+', '-'):
                advance()
                rhs = expr_term()
                if rhs is None:
                    return None
                v = v + rhs if c == '+' else v - rhs
                if v is None:
                    return None
            else:
                return v

    try:
        v = expr_sum()
        if pos[0] != n or v is None:
            return None
        return v
    except _Fail:
        return None

def eval_prefix(p):
    """Stack-machine evaluator for the produced prefix string."""
    def power_safe(a, b):
        if a == 0 and b <= 0:
            return None
        if b != int(b) and a < 0:
            return None
        try:
            r = a ** b
            if isinstance(r, complex) or abs(r) > 1e15:
                return None
            return r
        except (OverflowError, ValueError):
            return None

    vals = []
    for token in reversed(p):
        if token.isdigit():
            vals.append(float(int(token)))
        else:
            if len(vals) < 2:
                return None
            a = vals.pop()
            b = vals.pop()
            if a is None or b is None:
                return None
            if token == '+':
                vals.append(a + b)
            elif token == '-':
                vals.append(a - b)
            elif token == '*':
                vals.append(a * b)
            elif token == '/':
                vals.append(None if b == 0 else a / b)
            elif token == '%':
                vals.append(None if b == 0 else a % b)
            elif token == '^':
                vals.append(power_safe(a, b))
            if vals and vals[-1] is None:
                return None
    return vals[-1] if vals else None

# ---------------------------- Test vector suite -----------------------------
def run_vectors():
    import json
    import os
    path = os.path.join(os.path.dirname(__file__), 'test_vectors.json')
    with open(path, encoding='utf-8') as f:
        vectors = json.load(f)['tests']
    ok, bad = 0, 0
    for t in vectors:
        out1, corrupt, underflow, _ = in_place_sim(t['infix'])
        if out1 == t['prefix'] and not corrupt and not underflow:
            ok += 1
        else:
            bad += 1
            print(f"  FAIL vector: {t['infix']} => '{out1}' (expected '{t['prefix']}')")
    print(f"Layer 1a | Test Vectors           : {ok} passed, {bad} failed (of {len(vectors)})")
    return bad == 0

# ------------------------ Random expression generator ----------------------
_OPS = ['+', '-', '*', '/', '%', '^']
_DIGITS = '23456789'

def gen(depth=0):
    if depth >= 5 or random.random() < 0.25:
        return random.choice(_DIGITS)
    op = random.choice(_OPS)
    expr = gen(depth + 1) + op + gen(depth + 1)
    if random.random() < 0.45:
        return f'({expr})'
    return expr

# ------------------------------ Main driver --------------------------------
def main():
    parser = argparse.ArgumentParser(description='3-layer stress test for the in-place converter')
    parser.add_argument('--n', type=int, default=40000, help='number of random expressions')
    parser.add_argument('--seed', type=int, default=2026, help='PRNG seed for reproducibility')
    args = parser.parse_args()

    N = args.n
    random.seed(args.seed)

    agree = disagree = corrupt_ct = underflow_ct = 0
    numeric_ok = numeric_fail = numeric_skip = 0
    max_depth_seen = 0
    mismatches = []

    for _ in range(N):
        e = gen()
        out1, corrupt, underflow, depth = in_place_sim(e)
        out2 = ref_textbook(e)
        corrupt_ct += corrupt
        underflow_ct += underflow
        max_depth_seen = max(max_depth_seen, depth)

        if out1 == out2:
            agree += 1
        else:
            disagree += 1
            if len(mismatches) < 6:
                mismatches.append(('DIFF', e, out1, out2))

        vinf = eval_infix_string(e)
        if vinf is None:
            numeric_skip += 1
        else:
            vpre = eval_prefix(out1)
            if vpre is None:
                numeric_skip += 1
            elif vinf != vinf and vpre != vpre:      # both NaN = identical behaviour
                numeric_ok += 1
            elif vinf == vinf and vpre == vpre and abs(vinf - vpre) < 1e-9 * max(1.0, abs(vinf)):
                numeric_ok += 1
            else:
                numeric_fail += 1
                if len(mismatches) < 6:
                    mismatches.append(('NUM', e, out1, vinf, vpre))

    print('=' * 64)
    print('   IN-PLACE ALGORITHM 3-LAYER STRESS TEST REPORT')
    print('=' * 64)
    print(f'Random expressions tested                      : {N:,}')
    print(f'L1 | In-Place == Independent 3-pass Reference  : {agree:,} ({agree*100.0/N:.4f}%)')
    print(f'L1 | Disagreements                             : {disagree}')
    print(f'L2 | In-place overwrite corruption events      : {corrupt_ct}')
    print(f'L2 | Write-pointer underflow events            : {underflow_ct}')
    print(f'L3 | Numeric: eval(infix) == eval(prefix out)  : {numeric_ok:,} passed')
    print(f'L3 | Numeric semantically FAILED               : {numeric_fail}')
    print(f'L3 | Skipped (div-by-zero / overflow guard)    : {numeric_skip:,}')
    print(f'Max operator-stack depth observed              : {max_depth_seen}')
    if mismatches:
        for m in mismatches:
            print('  MISMATCH:', m)

    vec_ok = run_vectors()

    if disagree == 0 and corrupt_ct == 0 and underflow_ct == 0 and numeric_fail == 0 and vec_ok:
        print('-' * 64)
        print('ALL LAYERS PASSED - the algorithm is verified.')
        sys.exit(0)
    else:
        print('-' * 64)
        print('SOME LAYERS FAILED - the algorithm needs review.')
        sys.exit(1)

if __name__ == '__main__':
    main()
