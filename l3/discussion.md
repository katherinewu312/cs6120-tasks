Group (@katherinewu312, @samuelbreckenridge)

Our implementation of "trivial" dead code elimination matches closely what was discussed in lessons. In each 
function we loop over all basic blocks and first remove any instructions defining globally unused variables, then 
remove instructions that define variables which will be overwritten before being used, which we track using a set of 
variables that are defined but unused. We tested our implementation by ... TODO
 
Our implementation of local value numbering also closely matches the pseudocode we went over in the lesson, however 
we identified a lot of corner cases that needed to be handled. In particular, it was a bit challenging to iron out 
which instructions could be ignored, we initially just ignored labels, then found that jmps and nops caused us 
to crash because they had no args, then later on realized some rets and calls did not have args either and needed to 
be handled. Using brench to test on all benchmarks was really helpful here as it turned up a lot of cases we 
wouldn't have thought of otherwise. The hardest part of getting LVN to work was probably the variable renaming, we 
realized we needed to make our implementation aware of variable use across basic blocks to guarantee our fresh names 
didn't overwrite variables in other blocks, so we included a set of reserved variables as part of our LVN state. We 
also ran into a nasty bug where we were updating the "cloud" using newly generated variable names rather than the 
original, which caused subsequent instructions referencing the value to not get renamed correctly as they were doing 
a lookup using the original variable name (covered by the lvn chained_dest_overwrite.bril test case). We also extended 
our implementation to handle CSE exploiting commutativity and copy propagation. Copy propagation ended up being tricky 
because we ran into a corner case in the (identified from the euler.bril benchmark) where doing copy propagation on 
variables defined externally to the basic block caused incorrect execution because it would assign the same value to 
the variable throughout the block even if it was overwritten (our lvn test case func_arg_reassign.bril covers this).

To test our LVN implementation we used turnt to test cases that we knew 
would be important before beginning (variables defined in previous basic blocks, variable renaming, CSE etc.) and 
augmented these with cases to catch bugs as they came up. We also used brench to confirm that our implementation 
maintained correctness on all bril benchmarks.

We paired our LVN implementation with DCE as a post-processing step and used brench to confirm all bril benchmarks 
still ran correctly. We found that we optimized ... TODO