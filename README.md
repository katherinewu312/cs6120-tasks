# cs6120-tasks


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

 
