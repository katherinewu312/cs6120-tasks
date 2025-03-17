# Notes from class 3/6 

```c
// install LLVM & CMake using Homebrew
// (when installing LLVM, you can ignore what Homebrew says about libunwind)
brew install llvm
brew install cmake

// Clang should already be installed on your Mac
clang --version

// this tells you where LLVM is installed
brew --prefix llvm 
```

```c
// now, create a C file `a.c` and put the following code in it:
int main(int argc, char** argv) {
  return argc + 2;	
}
```

```c
// this command prints out the text representation of the LLVM IR of `a.c` to stdout
`brew --prefix llvm`/bin/clang -emit-llvm -S -o - a.c

// Then clone Adrian's LLVM skeleton repo from here:
// https://github.com/sampsyo/llvm-pass-skeleton

cd llvm-pass-skeleton
mkdir build 

// we have to set the LLVM_DIR environment variable to tell CMake where to find
// LLVM. CMake then generates a makefile:
LLVM_DIR=`brew --prefix llvm`/lib/cmake/llvm cmake ..

// compile using make -- it should say it has built something called 
// `SkeletonPass.dylib`
make

// then, put the a.c file you built earlier and put it at the top-level folder in the 
// llvm-pass-skeleton directory. Then, run the following:
// (it should print "I saw a function called main!" to stdout)
`brew --prefix llvm`/bin/clang -fpass-plugin=build/skeleton/SkeletonPass.dylib a.c

// When you edit `skeleton.cpp`, run the following to recompile & execute a.c
make -C build && `brew --prefix llvm`/bin/clang -fpass-plugin=build/skeleton/SkeletonPass.dylib a.c
```




