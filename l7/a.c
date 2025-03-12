#include <stdio.h>
int main(int argc, char** argv) {
    int zero = 0;
    int result = 5 / zero;
    int use_site = result + 1;
    int another_use_site = result + 2;
    printf("%d\n", another_use_site);
    return another_use_site;	
}
