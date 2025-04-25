Group (@ngernest, @katherinewu312, @samuelbreckenridge)

[Code](https://github.com/katherinewu312/cs6120-tasks/tree/main/l12)                

Our modified reference interpreter records traces from the beginning of the main function for a configurable number 
of dynamic instructions. Using the resulting trace as output our optimizer parses the trace to identify the sequence 
of instructions between two backedges that occurs the most frequently in the main function and chooses this as the 
"hot path" to optimize for. We kept our analysis intraprocedural and just bailed out of tracking paths on function 
calls. Once the hot path is identified we prepend a speculation block to the original sequence of instructions that 
eliminates 
jumps and converts branches to guard conditions that if failed will cause execution to jump to a hotpathfailed label 
where the instructions will execute normally not on the "fast path". At the end of the speculation block we 
commit and jump to a hotpathsuccess block. The most difficult part of this implementation was probably determining 
what information needed to be recorded by the trace versus could be inferred by the optimizer. We settled on a 
relatively "dumb" interpreter and did most of the work of identifying hot paths and constructing the new program in 
the optimizer, but had to iterate a bit to find what worked.












