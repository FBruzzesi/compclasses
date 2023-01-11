# Contributing

## Guidelines

We welcome contributions to the library! If you have a bug fix or new feature that you would like to contribute, please follow the steps below:

1. Fork the repository on GitHub.
2. Clone the repository to your local machine.
3. Create a new branch for your bug fix or feature.
4. Make your changes and test them thoroughly, making sure that it passes all current tests (see more below)
5. Commit your changes and push the branch to your fork.
6. Open a pull request on the main repository.

Code of Conduct
All contributors are expected to follow the project's code of conduct, which is based on the Contributor Covenant.

### Reporting Bugs
If you find a bug in the library, please report it by opening an [issue on GitHub](https://github.com/FBruzzesi/compclasses/issues). Be sure to include the version of the library you're using, as well as any error messages or tracebacks and a reproducible example.

### Requesting Features
If you have a suggestion for a new feature, please open an [issue on GitHub](https://github.com/FBruzzesi/compclasses/issues). Be sure to explain the problem that you're trying to solve and how you think the feature would solve it.

### Submitting Pull Requests
When submitting a pull request, please make sure that you've followed the steps above and that your code has been thoroughly tested. Also, be sure to include a brief summary of the changes you've made and a reference to any issues that your pull request resolves.

### Code formatting

Compclasses uses [black](https://black.readthedocs.io/en/stable/index.html) and [isort](https://pycqa.github.io/isort/) with default parameters for code formatting.

As part of the checks on pull requests, it is checked whether the code follows those standards. To ensure that the standard is met, it is recommanded to install [pre-commit hooks](https://pre-commit.com/):

```bash
python -m pip install pre-commit
pre-commit install
```

or by taking advantage of the Makefile it is enough to run:

```
make init-dev
```

## Developing

## Docs

## Tests
