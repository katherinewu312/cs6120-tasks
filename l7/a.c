#include <stdio.h>
int main(int argc, char** argv) {
    float zero = 0;
    float result = 5 / zero;
    float use_site = result + 1;
    int another_use_site = (int) result + 2;
    printf("%d\n", another_use_site);
    return another_use_site;	
}
