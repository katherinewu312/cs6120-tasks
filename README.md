# CS 6120 Tasks

## Repo overview
- [Lesson 2: Representing Programs](./l2)
- [Lesson 3: Local Analysis & Optimization](./l3)
- [Lesson 4: Data Flow](./l4)
- [Lesson 5: Global Analysis](./l5)
- [Lesson 6: Static Single Assignment](./l6)
- [Lesson 7: LLVM](./l7)
- [Lesson 8: Loop Optimization](./l8)
- [Lesson 12: Dynamic Compilers](./l12)

## Setting up a TypeScript environment (for L12)
Install the TypeScript compiler globally (`-g`) on your machine by doing:
```bash
$ npm install -g typescript
```
Check whether TypeScript is installed by doing:
```bash
$ tsc --version
```
(Also make sure the JS runtime [Deno](https://docs.deno.com/runtime/) is installed -- this should already be done already.)

To compile / run a TypeScript file, just do:
```bash
$ deno <.ts file>
```

## Setting up a Python virtual environment using uv

First, install uv following the instructions [here](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

To create a virtualenv using [uv](https://docs.astral.sh/uv/), run the following in the 
top-level directory. (Note that Python 3.12 or newer is required.)
```bash
$ uv venv cs6120 --python 3.12
```
(this creates a virtualenv called `cs6120`).

To activate your local virtual environment, run:
```bash
$ source cs6120/bin/activate
```

To install Python packages in the new virtual environment (eg `matplotlib`), run:
```bash
$ uv pip install matplotlib
```

To deactivate your virtualenv, run `deactivate`.

 
