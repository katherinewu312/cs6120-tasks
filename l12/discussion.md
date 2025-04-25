Group (@ngernest, @katherinewu312, @samuelbreckenridge)

[Code](https://github.com/katherinewu312/cs6120-tasks/tree/main/l12)                

Our modified reference interpreter records traces from the beginning of the `main` function for a configurable number 
of dynamic instructions (currently 1000). Using the resulting trace as output, our optimizer (a separate Python script) parses the trace to identify the sequence 
of instructions between two backedges that occurs the most frequently in the `main` function and chooses this as the 
"hot path" to optimize for. We kept our analysis intraprocedural and just bailed out of tracking paths on function 
calls / effect operations e.g. `print`. Once the hot path is identified, we prepend a speculation block to the original sequence of instructions that 
eliminates jumps and converts branches to guard conditions that if failed will cause execution to jump to a `hotpathfailed` label 
where the instructions will execute normally not on the "fast path". At the end of the speculation block we 
commit and jump to a `hotpathsuccess` block. The most difficult part of this implementation was probably determining 
what information needed to be recorded by the trace versus could be inferred by the optimizer. Initially, we thought we could do all the work in the TypeScript
interpreter, but we quickly realized this was not going to be the best design since we want to enforce some separation of concerns between actually interpreting
instructions and emitting the modified trace. We settled on a relatively "dumb" interpreter and did most of the work of identifying hot paths and constructing the new program in the optimizer, but we had to iterate a bit to find what worked.

Here is essentially a high-level overview of how we stitch the trace back into the program:

```bash
@main(num: int) {
    # code 1...
    # hottest trace...
    # code 2...
}
@main(num: int) {
    # code 1...
    speculate;
    # hottest trace...
    # something about branching to .hotpathfail
    commit;
    jmp .hotpathsuccess;
    .hotpathfail:
    # hottest trace...
    .hotpathsuccess:
    # code 2...
}
```

We tested our implemention on several core bril benchmarks. Specifically, we tested on `br.bril`, `factors.bril`, `perfect.bril`, and `while.bril`, all of which but one contained loops. First, we used brench to test correctness on one input, i.e. when the default input and the input to reduce overfitting matched. Despite an increase in dynamic instruction count between the baseline and speculative optimization pipelines, the tests all pass. We then tested on multiple inputs, using one input to generate the trace and optimize the program and the other to check correctness. We used 3 as our default input for all benchmarks. Specifically, here are our results (left is input value, right is total dynamic instruction count):

`factors.bril`:
(default total_dyn_inst: 24)
input 10: total_dyn_inst 64
input 15: total_dyn_inst 64
input 20: total_dyn_inst 74

`perfect.bril`:
(default total_dyn_inst: 13)
input 10: total_dyn_inst 46
input 15: total_dyn_inst 46
input 20: total_dyn_inst 58

`while.bril`:
(default total_dyn_inst: 22)
input 10: total_dyn_inst 119
input 15: total_dyn_inst 174
input 20: total_dyn_inst 229

















