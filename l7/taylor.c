// Adapted from https://github.com/destro014/Numerical-Method-In-C/blob/master/taylors%20series.c

#include <stdio.h>
#include <conio.h>
#include <math.h>

long int factorial(int n) {
  if (n <= 1) {
    return 1;
  } else {
    n = n * factorial(n - 1);
    return n;
  }   
}

int main() {
  int x, i;
  float s, r;
  char c;

  printf("Consider the Taylor series of e^x minus the 1st term: -1 + x/1! + x^2/2! + x^3/3! + x^4/4! ... + x^x/x!");
  printf("Enter the no. of sums to which you'd like the sum to be computed:");
  scanf("%d", & x);
  s = 0;
  for (i = 1; i <= x; i++) {
    s = s + ((float) pow(x, i) / (float) factorial(i));
  }
  printf("The sum of %d terms is %f\n", x, 1 + s);
}

