Group (@katherinewu312, @ngernest, @samuelbreckenridge)          
[(Code)](https://github.com/katherinewu312/cs6120-tasks/tree/main/l8)

We implemented LICM in LLVM. 

We ran into an issue involving `load`s and `store`s, where our pass would keep 
running over because we weren't handling these instructions properly. To solve this issue, we first ran LLVM's `mem2reg` pass before running our LICM pass -- `mem2reg` converts memory references to register references, removing `load` and `store` instructions. We also use LLVM's `Instruction::mayReadOrWriteMemory` helper function to identify instructions which access memory and only move instructions for which this instruction returns `false`. 

