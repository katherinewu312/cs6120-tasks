Group (@ngernest, @katherinewu312, @samuelbreckenridge)

As a first step we implemented a data flow analysis to identify live variables. Setting up a skeleton of the solver 
was pretty straightforward, although we did have to be a bit careful about setting things up consistently to run 
backwards instead of forwards. The trickiest part of the live variables analysis was probably finding the appropriate 
transfer function, it was helpful to switch to thinking about the set operations as per instruction rather than per 
basic block as discussed in class. To test our implementation we chose a selection of bril tests and benchmarks and 
compared the output of our data analysis to a manual tracking of live variables. This certainly revealed bugs that 
we were able to fix (e.g. Python sets not getting updated because the union method is not in place) but overall it 
was quite tricky to determine live variables manually, especially for complex control flows. This somewhat limits 
our ability to gain confidence in our implementation from these more complex tests so we are more reliant on simple 
unit tests that can be manually verified.
