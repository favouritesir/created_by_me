// ============================================================================
// IN-PLACE INFIX TO PREFIX CONVERTER
// Original Algorithm : Ashikur Rahman (Created: Spring 2022)
// Refactored & Tested: Ashikur Rahman (2026)
// Concept            : O(N) Time, O(1) Auxiliary String Space (Dual-Pointer)
// ============================================================================

#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 100

char stack[MAX];
int top = -1;

// Function to check operator priority
int priority(char x) {
    if (x == '+' || x == '-') return 1;
    if (x == '*' || x == '/' || x == '%') return 2;
    if (x == '^') return 3;
    return 0;
}

// Function to check if an operator is right-associative
int isRightAssociative(char op) {
    return (op == '^');
}

// Stack Push (guarded: prevents buffer overflow on adversarial inputs)
void push(char x) {
    if (top < MAX - 1) {
        stack[++top] = x;
    }
}

// Stack Pop
char pop() {
    if (top == -1) return -1;
    return stack[top--];
}

// Core Algorithm: In-place Infix to Prefix
void makePrefixInPlace(char str[]) {
    int len = strlen(str);
    int read_idx = len - 1;   // Moves right to left reading characters
    int write_idx = len - 1;  // Moves right to left writing the output

    while (read_idx >= 0) {
        char current = str[read_idx];

        if (current == ')') {
            push(current);
        } 
        else if (current == '(') {
            char x;
            while ((x = pop()) != ')' && x != -1) {
                str[write_idx--] = x; // Write directly to the same array
            }
        } 
        else if (priority(current) > 0) { // It's an Operator
            // For Right-to-Left scan:
            // - Left-associative (+, -, *, /, %): pop only when incoming priority < stack top priority
            // - Right-associative (^): pop when incoming priority <= stack top priority
            while (top != -1 && stack[top] != ')') {
                int p_curr = priority(current);
                int p_top = priority(stack[top]);
                if (p_curr < p_top || (p_curr == p_top && isRightAssociative(current))) {
                    str[write_idx--] = pop();
                } else {
                    break;
                }
            }
            push(current);
        } 
        else if (isalnum(current)) { // It's an Operand (a-z, A-Z, 0-9)
            str[write_idx--] = current;
        }
        
        read_idx--;
    }

    // Pop any remaining operators from the stack
    while (top != -1) {
        char x = pop();
        if (x != ')' && x != '(') {
            str[write_idx--] = x;
        }
    }

    // Since parentheses are removed, the final prefix expression is shorter.
    // The valid result is currently sitting at the end of the array.
    // We shift it to the beginning of the string [index 0].
    int new_len = len - 1 - write_idx;
    for (int i = 0; i < new_len; i++) {
        str[i] = str[write_idx + 1 + i];
    }
    str[new_len] = '\0'; // Null-terminate the new string
}

int main() {
    char exp[100]; // Fixed: Safe memory allocation
    
    printf("Enter the Infix expression : ");
    if (fgets(exp, sizeof(exp), stdin) != NULL) {
        // Remove the trailing newline character added by fgets
        exp[strcspn(exp, "\n")] = '\0'; 
        
        makePrefixInPlace(exp);
        
        printf("\nResult (Prefix Expression): %s\n", exp);
    }
    return 0;
}
