#include <stdio.h>

// Example program to test LICM pass
int test(int x) {
    int y = 0;
    for (int i = 0; i < 10; i++) {
        int j = 1;  // loop invariant
        y = y + j;
    }
    return y;
}

int main() {
    int x = 0;
    for (int i = 0; i < 5; i++) {
        int j = 2;  // loop invariant
        x = x + j;
    }
    printf("x = %d\n", x);
    return 0;
}