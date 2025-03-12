# Lesson 7: LLVM

To build:
```bash
$ cd build
$ cmake ..
$ make
$ cd ..
```

When you edit `skeleton.cpp`, run the following to recompile & execute `a.c`:
```bash
$ make -C build && `brew --prefix llvm`/bin/clang -fpass-plugin=build/skeleton/SkeletonPass.dylib a.c
```

To see the emitted LLVM code produced by `clang` (with our modifications), run:
```bash
$ `brew --prefix llvm`/bin/clang -fpass-plugin=build/skeleton/SkeletonPass.dylib -emit-llvm -S -o - a.c
```
