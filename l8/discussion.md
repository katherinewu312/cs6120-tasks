Group (@katherinewu312, @ngernest, @samuelbreckenridge)          
[(Code)](https://github.com/katherinewu312/cs6120-tasks/tree/main/l8)

We implemented LICM in LLVM. Our implementation follows roughly the high-level pseudocode mentioned in lecture, where for every instruction in the loop, we mark it as loop invariant iff for all its operands, either all their reaching definitions are outside the loop or there is exactly one definition and it is already marked as loop invariant. We then iterate this to convergence. After identifying all possible loop invariant instructions, we make sure to move them up to the preheader block.

The implementation was more challenging than we initially thought, mainly due to difficulties in navigating and understanding the LLVM docs. In the beginning, we were looking into using provided helper functions from LLVM such as Loop::hasLoopInvariantOperands and Loop::makeLoopInvariant and had a preliminary implementation that called these methods, which essentially outsourced the work for us. We then decided to revamp our implementation so that we were actually implementing the specifics of the LICM pass ourselves, following the high-level pseudocode from lecture and checking explicitly when it is safe to move a loop-invariant instruction to the preheader.

Specfically, getting the pass manager to work was challenging. We learned that LLVM currently contains two pass managers, the legacy PM and the new PM. The optimization pipeline (aka the middle-end) uses the new PM, whereas the backend target-dependent code generation uses the legacy PM. We realized that to add a pass, we must match the pass type and the pass manager type: this was the underlying cause of an issue that arose for us. We were trying to reuse the pass manager from the skeleton-llvm-pass from lecture and ended up running into issues due to us directly adding a LoopPassManager pass type to a ModulePassManager pass manager type. Luckily, [this link](https://discourse.llvm.org/t/how-to-write-a-loop-pass-using-new-pass-manager/70240) was helpful in resolving the issue!

We also ran into an issue involving `load`s and `store`s, where our pass would keep 
running over because we weren't handling these instructions properly. To solve this issue, we first ran LLVM's `mem2reg` pass before running our LICM pass -- `mem2reg` converts memory references to register references, removing `load` and `store` instructions. 

We tested our implementation ... [to finish]

