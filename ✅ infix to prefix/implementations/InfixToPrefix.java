// ============================================================================
// IN-PLACE INFIX TO PREFIX CONVERTER - Java Implementation
// Original Algorithm : Ashikur Rahman (Created: Spring 2022)
// Refactored & Ported: Ashikur Rahman (2026)
// Concept            : O(N) Time, O(1) auxiliary string space (two-pointer, right-to-left)
// ============================================================================

public class InfixToPrefix {

    static final int MAX = 100;

    // Static operator stack (operator buffers never exceed ~MAX/2 for valid inputs)
    static char[] stack = new char[MAX];
    static int top = -1;

    static int priority(char x) {
        if (x == '+' || x == '-') return 1;
        if (x == '*' || x == '/' || x == '%') return 2;
        if (x == '^') return 3;
        return 0;
    }

    static boolean isRightAssociative(char op) {
        return op == '^';
    }

    static void push(char x) {
        if (top < MAX - 1) {
            stack[++top] = x;
        }
    }

    static char pop() {
        if (top == -1) return '\0';
        return stack[top--];
    }

    // Core Algorithm: in-place conversion on a Java char array.
    // Returns the length of the resulting prefix expression.
    static int makePrefixInPlace(char[] str) {
        int len = str.length;
        int readIdx = len - 1;   // moves right to left, reading characters
        int writeIdx = len - 1;  // moves right to left, writing the output

        while (readIdx >= 0) {
            char current = str[readIdx];

            if (current == ')') {
                push(current);
            } else if (current == '(') {
                char x;
                while ((x = pop()) != ')' && x != '\0') {
                    str[writeIdx--] = x; // Write directly on the same array
                }
            } else if (priority(current) > 0) {
                // Operator handling with (inverted) associativity rules
                while (top != -1 && stack[top] != ')') {
                    int pCurr = priority(current);
                    int pTop = priority(stack[top]);
                    if (pCurr < pTop || (pCurr == pTop && isRightAssociative(current))) {
                        str[writeIdx--] = pop();
                    } else {
                        break;
                    }
                }
                push(current);
            } else if (Character.isLetterOrDigit(current)) {
                str[writeIdx--] = current; // Operand: written immediately
            }

            readIdx--;
        }

        // Flush remaining operators from the stack
        while (top != -1) {
            char x = pop();
            if (x != ')' && x != '(') {
                str[writeIdx--] = x;
            }
        }

        // Shift the valid result (currently at the tail of the array) to index 0
        int newLen = len - 1 - writeIdx;
        for (int i = 0; i < newLen; i++) {
            str[i] = str[writeIdx + 1 + i];
        }
        if (newLen < str.length) str[newLen] = '\0';
        return newLen;
    }

    // Convenience wrapper: infix String -> prefix String
    static String infixToPrefix(String expr) {
        char[] buf = new char[MAX];
        char[] src = expr.toCharArray();
        System.arraycopy(src, 0, buf, 0, src.length);
        int newLen = makePrefixInPlace(buf);
        return new String(buf, 0, newLen);
    }

    public static void main(String[] args) {
        String[] samples = {"(a-b/c)*(a/k-l)", "A+B*C/D-E", "A^B^C", "a-b-c"};
        for (String s : samples) {
            System.out.printf("%-20s => %s%n", s, infixToPrefix(s));
        }
    }
}
