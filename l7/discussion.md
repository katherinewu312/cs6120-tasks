Group (@ngernest, @katherinewu312, @samuelbreckenridge)          
[(Code)](https://github.com/katherinewu312/cs6120-tasks/tree/main/l7)

We implemented a pass which replaces every division instruction with a `select`
instruction (the LLVM equivalent of a ternary statement in C) that checks if we're dividing by 0 
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
We support both unsigned/signed integer division (`udiv`, `sdiv`) and floating-point division (`fdiv`). 

To aid debugging, every time our pass replaces a division instruction with 
a select instruction, we print to `stdout` the original & new instructions, along with 
info about how the uses of the division have been updated:  
```
Found floating-point division :
  %25 = fdiv float %21, %24
Created new instructions:
  %25 = fcmp oeq float %24, 0.0
  %26 = fdiv float %21, %24
  %27 = select i1 %25, float 0.0, float %26
Original use:
  %29 = fadd float %15, %28
Updated use:
  %29 = fadd float %15, %27
```

Implementing this pass was relatively straightforward, although we realized we 
had to handle integer & floating-point division separately, since LLVM has separate comparison 
instructions for ints and FPs (`icmp` and `fcmp`). Initially, we naively tried to handle both int & FP cases at the same time, but we quickly realized this was not possible since LLVM instructions are not "polymorphic", i.e. there are different comparison/division instructions for ints/FPs, and LLVM stipulates that arguments' types have to be explicitly stated. When figuring out operands' types, we found the `isIntegerTy` and `isFloatingPointTy` functions in the [`llvm::Type` class](https://llvm.org/doxygen/classllvm_1_1Type.html) to be extremely helpful! The plethora of possible int types in C (`long`, `short`, `unsigned ...`, `signed ...`) are all instances of LLVM's general `IntegerType` (similarly for FP types), so helper functions like `isIntegerTy` remove the need for us to explicitly handle different numeric types in C.


**Simple example:**
Consider this C program which contains a division-by-zero statement:
```c
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

**More complicated examples:**         
To demonstrate that our pass works on larger programs, we have C implementations of [Taylor series](./taylor.c), a [probabilistic approximation of pi](./pi.c), and an [n-body simulation](./nbody.c) (the latter two of which are taken from the official LLVM test suite). 
These latter two files contain multiple division instructions (as opposed to the first simple C file above which only has one division), which 
helped us realize that we had two bugs in our initial implementation, one where our pass prematurely finishes after updating the first division instructions it sees, and one where we forgot to ignore non-division instructions in our pass. After fixing these bugs, we manually checked
that the executables produced by `clang` return the same result with and without our pass.




