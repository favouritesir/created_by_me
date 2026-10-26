// ============================================================================
// IN-PLACE INFIX TO PREFIX CONVERTER - C# Implementation
// Author  : Ashikur Rahman (2026)
// Concept : O(N) Time, O(1) auxiliary string space (two-pointer, right-to-left)
// ============================================================================

using System;

public class InfixToPrefix
{
    const int MAX = 100;

    static char[] stack = new char[MAX];
    static int top = -1;

    static int Priority(char x)
    {
        if (x == '+' || x == '-') return 1;
        if (x == '*' || x == '/' || x == '%') return 2;
        if (x == '^') return 3;
        return 0;
    }

    static bool IsRightAssociative(char op)
    {
        return op == '^';
    }

    static void Push(char x)
    {
        if (top < MAX - 1)
        {
            stack[++top] = x;
        }
    }

    static char Pop()
    {
        if (top == -1) return '\0';
        return stack[top--];
    }

    // Core Algorithm: in-place conversion on a char array.
    // Returns the length of the resulting prefix expression.
    static int MakePrefixInPlace(char[] str)
    {
        int len = str.Length;
        int readIdx = len - 1;   // moves right to left, reading characters
        int writeIdx = len - 1;  // moves right to left, writing the output

        while (readIdx >= 0)
        {
            char current = str[readIdx];

            if (current == ')')
            {
                Push(current);
            }
            else if (current == '(')
            {
                char x;
                while ((x = Pop()) != ')' && x != '\0')
                {
                    str[writeIdx--] = x; // Write directly on the same array
                }
            }
            else if (Priority(current) > 0)
            {
                // Operator handling with (inverted) associativity rules
                while (top != -1 && stack[top] != ')')
                {
                    int pCurr = Priority(current);
                    int pTop = Priority(stack[top]);
                    if (pCurr < pTop || (pCurr == pTop && IsRightAssociative(current)))
                    {
                        str[writeIdx--] = Pop();
                    }
                    else
                    {
                        break;
                    }
                }
                Push(current);
            }
            else if (char.IsLetterOrDigit(current))
            {
                str[writeIdx--] = current; // Operand: written immediately
            }

            readIdx--;
        }

        // Flush remaining operators from the stack
        while (top != -1)
        {
            char x = Pop();
            if (x != ')' && x != '(')
            {
                str[writeIdx--] = x;
            }
        }

        // Shift the valid result (currently at the tail of the array) to index 0
        int newLen = len - 1 - writeIdx;
        for (int i = 0; i < newLen; i++)
        {
            str[i] = str[writeIdx + 1 + i];
        }
        if (newLen < str.Length) str[newLen] = '\0';
        return newLen;
    }

    // Convenience wrapper: infix string -> prefix string
    public static string Convert(string expr)
    {
        char[] buf = new char[MAX];
        char[] src = expr.ToCharArray();
        Array.Copy(src, buf, src.Length);
        int newLen = MakePrefixInPlace(buf);
        return new string(buf, 0, newLen);
    }

    static void Main()
    {
        string[] samples = { "(a-b/c)*(a/k-l)", "A+B*C/D-E", "A^B^C", "a-b-c" };
        foreach (string s in samples)
        {
            Console.WriteLine(string.Format("{0,-20} => {1}", s, Convert(s)));
        }
    }
}
