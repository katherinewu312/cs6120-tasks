Group (@ngernest, @katherinewu312, @samuelbreckenridge)

[Code](https://github.com/katherinewu312/cs6120-tasks/tree/main/l4)
(Katherine: generic solver, Sam: live variables, Ernest: constant propagation)

As a first step we implemented a data flow analysis to identify live variables. Setting up a skeleton of the solver 
was pretty straightforward, although we did have to be a bit careful about setting things up consistently to run 
backwards instead of forwards. The trickiest part of the live variables analysis was probably finding the appropriate 
transfer function, it was helpful to switch to thinking about the set operations as per instruction rather than per 
basic block as discussed in class. To test our implementation we chose a selection of Bril tests and benchmarks and 
compared the output of our data analysis to a manual tracking of live variables. This certainly revealed bugs that 
we were able to fix (e.g. Python sets not getting updated because the union method is not in place) but overall it 
was quite tricky to determine live variables manually, especially for complex control flows. This somewhat limits 
our ability to gain confidence in our implementation from these more complex tests so we are more reliant on simple 
unit tests that can be manually verified.

For constant propagation, the trickiest part was getting the merge function right.
From our discussion in class, we know that the merge function for constant propagation
should take the "union" of all dictionaries within a list of dicts (where each dict maps a variable name to its constant value, or `None` if it is unknown). Initially, we tried using 
Python's default dictionary union operator `d1 | d2`. However, we found out this doesn't
work when the same key `var` is defined in both dicts and `d1[var] != d2[var]`, 
since the Python operator automatically picks `d2[var]` due to how it is defined.
As a result, we had to hand-roll our own dictionary union function so that 
`var` is always mapped to `None` in the case above. To gain confidence in our constant propagation implementation, we used property-based random testing (using Python's [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) library) to check that our implementaiton satisfies various equational properties (e.g. the output dict from the merge function should preserve all keys from the argument dicts). We also set up separate Turnt environments for our different analyses and manually compared our results to [the example dataflow tests in the Bril repo](https://github.com/sampsyo/bril/tree/main/examples/test/df) to make sure our analysis works for a selection of Bril programs. 

We also decided to implement a generic solver that supports multiple analyses. Our code follows the high-level 
pseudocode that was mentioned in the lesson. We tried to think of a way to write both the forward and backward data 
flow passes as one piece of code, instead of having them as two separate problems. Doing so allowed us to reuse 
several variables, making our code less verbose, but this did mean that we were using block_in to represent 
block_out and vice versa for the backward pass. Although this did not introduce any technical problems, it did lead 
to some confusion in reading the code itself at times. Additionally, we made sure to define a dataclass called 
Analysis to distinguish between forward/backward passes, initial values, merge functions, and transfer functions. 
Thus, specifying a new data flow analysis simply amounted to assigning values to these variables forward, init, 
merge, and transfer. We tested our generic solver using turnt, using the bril examples located in the test directory.
We tested the generic solver by setting up turnt environments that ran the generic solver configured for live 
variables / constant propagation and checking that these runs matched the outputs of the respective standalone 
implementations. We think we deserve a Michelin star because we implemented multiple data flow analyses and tested 
these thoroughly using turnt before abstracting both implementations into a generic solver while verifying that 
correctness was maintained.