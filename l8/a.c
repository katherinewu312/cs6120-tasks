#include <stdio.h>

// Example program to test LICM pass
int main() {
    int x = 0;
    for (int i = 0; i < 5; i++) {
        int j = 2;  // loop invariant
        x = x + j;
    }
    printf("x = %d\n", x);
    return 0;
}