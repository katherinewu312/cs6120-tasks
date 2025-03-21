#include <stdio.h>

// Example program to test LICM pass
int main() {
    int x = 0;
    int a = 4;
    int b = 2;
    for (int i = 0; i < 5; i++) {
        int c = 1+a*b;
        x = x + a*c;
    }
    printf("x = %d\n", x);
    return 0;
}