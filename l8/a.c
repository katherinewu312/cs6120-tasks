#include <stdio.h>

// Example program to test LICM pass
int main() {
    int x = 0;
    int a = 4;
    int b = 2;
    for (int i = 0; i < 5; i++) {
        x = x + a*b;
    }
    printf("x = %d\n", x);
    return 0;
}