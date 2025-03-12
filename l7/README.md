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
make -C build && `brew --prefix llvm`/bin/clang -fpass-plugin=build/skeleton/SkeletonPass.dylib a.c
```
