Group (@ngernest, @katherinewu312, @samuelbreckenridge)

[Code](https://github.com/katherinewu312/cs6120-tasks/tree/main/l6)

For our conversion into SSA we use the basic approach of introducing a unique copy of each variable for every basic 
block. We do not ever construct explicit phi nodes but rather iterate over basic blocks adding the necessary get and 
set instructions to each. To handle variables that are undefined at certain basic blocks we explicitly set all 
variables to `undef` at the beginning of the function. The trickiest part of this implementation was figuring out 
how to handle function arguments correctly. We first tried to avoid renaming function arguments at all but found 
this prevented us from fully reaching SSA form if the function argument variable name was reused as a dest in the 
function body. Instead we copy the function argument into a renamed version at the beginning of the function. 
However we found a nasty bug with this approach that caused our SSA conversion of the core/orders.bril benchmark to 
enter an infinite loop because the function argument variable names were being written to but then control flow 
would pass back to the entry block and we would incorrectly copy the original function arguments back into the 
variable. To fix this we needed to add a dummy entry block for the function argument copies. To test our conversion 
to SSA we use turnt to convert to SSA and then evaluate correctness of execution and whether the converted programs 
are actually in SSA. We ran these checks on both handpicked test cases based on bugs we observed and all of the bril 
benchmarks, all of which pass.







