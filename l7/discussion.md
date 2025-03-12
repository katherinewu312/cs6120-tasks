Group (@ngernest, @katherinewu312, @samuelbreckenridge)          
[(Code)](https://github.com/katherinewu312/cs6120-tasks/tree/main/l7)

We implemented a pass which replaces every division instruction with a `select`
instruction (the LLVM of a ternary statement in C) that checks if we're dividing by 0 
and if so returns 0, otherwise returning the actual quotient that is computed. 
In other words, our pass turns instructions like:
```llvm
%11 = fdiv float 5.0, %10         ; Note that %10 may store the value 0
``` 
into:
```llvm
%11 = fcmp oeq float %10, 0.0
%12 = fdiv float 5.0, %10
%13 = select i1 %11, float 0.0, float %12     ; equivalent to the C ternary stmt `%13 = (%11 == 0) ? 0 : %12;`
```  
We support both unsigned/signed int division (`udiv`, `sdiv`) and floating-point division (`fdiv`). 


Here is a simple example demonstrating our pass:               
Consider this C program `a.c`, which contains a division-by-zero statement.
```c
// a.c
int main() {
    float zero = 0;
    float result = 5 / zero;
    int use_site = (int) result + 2;
    return use_site;	
}
```

If we use `clang` to compile this program *without* our pass and inspect the emitted LLVM with `-O` optimizations enabled, we get the following:

```c
define i32 @main() {
  ...
  ret i32 poison
}
```
After performing various local optimizations, the compiler determines that this function returns a `poison` value due to the presence of the division-by-zero, which LLVM considers undefined behavior.

However, if we use `clang` along with our pass to compile the same program (with the same `-O` optimizations), we get:
```c
define i32 @main() {
  ...
  ret i32 2
}
```
The resultant LLVM code returns a concrete non-zero value, which is expected! This is because our 
pass has determined that the denominator in the division instruction is 0 and replaces
the entire result of the division with 0, and `0 + 2 = 2`, so `main` returns `2`.


