# ============================================================================
# IN-PLACE INFIX TO PREFIX CONVERTER - Python Implementation
# Author  : Ashikur Rahman (2026)
# Concept : O(N) Time, O(1) auxiliary string space (two-pointer, right-to-left)
#
# Note: Python strings are immutable, so the in-place technique operates on a
# character list that stands in for the original C-style string buffer.
# The read/write pointer discipline is identical to the C version.
# ============================================================================

MAX = 100

def priority(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/', '%'):
        return 2
    if op == '^':
        return 3
    return 0

def is_right_associative(op):
    return op == '^'

def make_prefix_in_place(arr):
    """Convert arr (a mutable char list) from infix to prefix, in place.
    Returns the resulting prefix string."""
    n = len(arr)
    read_idx = n - 1    # moves right to left, reading characters
    write_idx = n - 1   # moves right to left, writing the output
    stack = []          # operator stack

    while read_idx >= 0:
        current = arr[read_idx]

        if current == ')':
            stack.append(current)
        elif current == '(':
            # Pop operators until the matching ')' is consumed; drop both parens
            while stack and stack[-1] != ')':
                arr[write_idx] = stack.pop()
                write_idx -= 1
            if stack and stack[-1] == ')':
                stack.pop()
        elif priority(current) > 0:
            # Operator handling with (inverted) associativity rules.
            while stack and stack[-1] != ')':
                p_curr = priority(current)
                p_top = priority(stack[-1])
                if p_curr < p_top or (p_curr == p_top and is_right_associative(current)):
                    arr[write_idx] = stack.pop()
                    write_idx -= 1
                else:
                    break
            stack.append(current)
        elif current.isalnum():
            arr[write_idx] = current   # Operand: written immediately
            write_idx -= 1

        read_idx -= 1

    # Flush remaining operators from the stack
    while stack:
        x = stack.pop()
        if x not in '()':
            arr[write_idx] = x
            write_idx -= 1

    # The valid prefix result sits at the tail: build it out (shift to index 0)
    new_len = n - 1 - write_idx
    result = ''.join(arr[write_idx + 1: write_idx + 1 + new_len])

    # True "shift to 0" step, mirroring the C implementation:
    for i in range(new_len):
        arr[i] = result[i]
    del arr[new_len:]

    return result

def infix_to_prefix(expr):
    """Convenience wrapper: infix string -> prefix string."""
    arr = list(expr)
    return make_prefix_in_place(arr)

if __name__ == '__main__':
    samples = ['(a-b/c)*(a/k-l)', 'A+B*C/D-E', 'A^B^C', 'a-b-c']
    for s in samples:
        print(f'{s:20} => {infix_to_prefix(s)}')
