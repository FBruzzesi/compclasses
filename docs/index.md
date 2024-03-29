<img src="img/compclass-logo.svg" width=180 height=180 align="right">

# Compclasses

![Licence](https://img.shields.io/github/license/FBruzzesi/compclasses)
<img src ="img/interrogate-shield.svg">
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<img src ="img/coverage.svg">
<img src="https://img.shields.io/pypi/pyversions/compclasses">

Like *dataclasses*, but for composition.

!!! quote "Favor object composition over class inheritance"

    As the Gang of Four (probably) said.

However when we use composition in Python, we cannot access methods directly from the composed class, and we either re-define these methods from scratch, or access them using chaining.

**Compclasses** enables composition and delegation of methods, making it easier to work with complex object structures.

---

[**Documentation**](https://fbruzzesi.github.io/compclasses/) | [**Source Code**](https://github.com/fbruzzesi/compclasses)

---

## Alpha Notice

This codebase is experimental and is working for my use cases. It is very probable that there are cases not covered and for which everything breaks. If you find them, please feel free to open an issue in the [issue page](https://github.com/FBruzzesi/compclasses/issues) of the repo.

## Installation

The library is dependency-free, it only uses built-in modules from the [Python Standard Library](https://docs.python.org/3/library/).

**compclasses** is published as a Python package on [pypi](https://pypi.org/), and it can be installed with pip, ideally by using a virtual environment (suggested option), or directly from source using git, or with a local clone:

=== "pip (pypi)"

    ```bash
    python -m pip install compclasses
    ```

=== "source/git"

    ```bash
    python -m pip install git+https://github.com/FBruzzesi/compclasses.git
    ```

=== "local clone"

    ```bash
    git clone https://github.com/FBruzzesi/compclasses.git
    cd compclasses
    python -m pip install .
    ```

## License

The project has a [MIT Licence](https://github.com/FBruzzesi/compclasses/blob/main/LICENSE)
