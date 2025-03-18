# Lesson 8: Loop Optimizations

See [`skeleton.cpp`](./skeleton/Skeleton.cpp) for the C++ code containing our LLVM pass. 


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

## Pass managers
From the LLVM docs (https://llvm.org/docs/NewPassManager.html):

```
LLVM currently contains two pass managers, the legacy PM and the new PM. The optimization pipeline (aka the middle-end) uses the new PM, whereas the backend target-dependent code generation uses the legacy PM.

The legacy PM somewhat works with the optimization pipeline, but this is deprecated and there are ongoing efforts to remove its usage.

Some IR passes are considered part of the backend codegen pipeline even if they are LLVM IR passes (whereas all MIR passes are codegen passes). This includes anything added via TargetPassConfig hooks, e.g. TargetPassConfig::addCodeGenPrepare().

The TargetMachine::adjustPassManager() function that was used to extend a legacy PM with passes on a per target basis has been removed. It was mainly used from opt, but since support for using the default pipelines has been removed in opt the function isn’t needed any longer. In the new PM such adjustments are done by using TargetMachine::registerPassBuilderCallbacks().

Currently there are efforts to make the codegen pipeline work with the new PM.
```