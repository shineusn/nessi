# Contributing to NeSSI

This document aims to give an overview of how to contribute to NeSSI.

## Getting started

To contribute, you must have:
* a __GitHub__ account
* __git__ installed on your system ([download and install](https://git-scm.com/downloads))

More informations on how to use __git__ are available on the [git official documentation](https://git-scm.com/doc) and the [GitHub cheat sheet](https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf)

## Submitting an Issue

Before submitting an issue, please search through [existing issues](https://github.com/PageotD/nessi/issues) to avoid duplicates.

If you want to post a problem/bug, to help us understand and resolve your issue please check that you have provided essential informations:

* __problem/bug description:__ A clear and concise description of what the bug is.
* __to reproduce:__ A small piece of code which reproduces the issue (with as few as possible external dependencies).
* __NeSSI version__, __python version__
* __platform__ OS+version (Debian 9, Ubuntu 16.10, ...)
* __virtual environement__ yes/no; if yes, which one.

## Submitting a Pull Request

Before submitting a pull request:
* be sure that the feature/hotfix that you want to add does not already exist.
* NeSSI follows a simple branching model, please read [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) before starting.

1. Fork the repository.
2. Make a new branch. For feature additions/changes base your new branch at `develop`, for pure bugfixes base your new branch at `master` .
3. Add a test for your change. Only refactoring and documentation changes require no new tests. If you are adding functionality or fixing a bug, we need a test!
4. Make the test pass.
5. Push to your fork and submit a pull request.
  - for feature branches set base branch to `nessi:develop`
  - for bugfix branches set base branch to the latests maintenance branch, e.g. `nessi:master`
6. Wait for our review. We may suggest some changes or improvements or alternatives. Keep in mind that PR checklist items can be met after the pull request has been opened by adding more commits to the branch.

All the submitted pieces including potential data must be compatible with the LGPLv3 license and will be LGPLv3 licensed as soon as they are part of NeSSI. Sending a pull request implies that you agree with this.

Additionally take care to not add big files. Even for tests we generally only accept files that are very small and at max on the order of a few kilobytes.
