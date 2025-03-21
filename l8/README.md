# Lesson 8: Loop Optimizations

See [`licm.cpp`](./licm/licm.cpp) for the C++ code containing our LLVM pass. 


To build:
```bash
$ mkdir build
$ cd build
$ cmake ..
$ make
$ cd ..
```

When you edit `licm.cpp`, run the following to recompile & execute `test/licm_base.c`:
```bash
$ make -C build && `brew --prefix llvm`/bin/clang -fpass-plugin=build/licm/LICMPass.dylib test/licm_base.c
```

To see the emitted LLVM code produced by `clang` (with our modifications), run:
```bash
$ `brew --prefix llvm`/bin/clang -fpass-plugin=build/licm/LICMPass.dylib -emit-llvm -S -o - test/licm_base.c
```

To run the loop pass, we use LLVM [opt](https://rocm.docs.amd.com/projects/llvm-project/en/latest/LLVM/llvm/html/CommandGuide/opt.html):
```
$ `brew --prefix llvm`/bin/clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone test/licm_base.c -o licm_base.ll 

$ `brew --prefix llvm`/bin/opt -load-pass-plugin=build/licm/LICMPass.dylib -passes='LICMPass' licm_base.ll -S > licm_base_opt.ll
```

The first command compiles the file `licm_base.c` into unoptimized LLVM IR and saves it as `licm_base.ll`. The second command applies the LICM optimization pass to `licm_base.ll` and outputs the optimized IR to `licm_base_opt.ll`.

## Pass managers
From the LLVM docs (https://llvm.org/docs/NewPassManager.html):

> LLVM currently contains two pass managers, the legacy PM and the new PM. The optimization pipeline (aka the middle-end) uses the new PM, whereas the backend target-dependent code generation uses the legacy PM. The legacy PM somewhat works with the optimization pipeline, but this is deprecated and there are ongoing efforts to remove its usage. Some IR passes are considered part of the backend codegen pipeline even if they are LLVM IR passes (whereas all MIR passes are codegen passes). This includes anything added via TargetPassConfig hooks, e.g. TargetPassConfig::addCodeGenPrepare(). The TargetMachine::adjustPassManager() function that was used to extend a legacy PM with passes on a per target basis has been removed. It was mainly used from opt, but since support for using the default pipelines has been removed in opt the function isn’t needed any longer. In the new PM such adjustments are done by using TargetMachine::registerPassBuilderCallbacks(). Currently there are efforts to make the codegen pipeline work with the new PM.

[This link](https://discourse.llvm.org/t/how-to-write-a-loop-pass-using-new-pass-manager/70240) was particularly helpful in getting us set up to write a loop pass using the new pass manager.