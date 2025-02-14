# Lesson 4: Dataflow Analyses

## Testing using Turnt

To confirm (using Turnt) that our standalone implementation of live variables & constant propagation
behave the same as the generic solver instantiated with these analyses, `cd` into the `test` subdirectory and run the following:
```bash 
turnt *.bril --env live_vars
turnt *.bril --env generic_live_vars

turnt *.bril --env const_prop
turnt *.bril --env generic_const_prop
```
