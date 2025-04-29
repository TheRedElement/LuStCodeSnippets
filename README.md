# code_snippets

repository of some useful code snippets in various programming languages.

If you want to use the code simply clone the repo:

```shell
    git clone https://github.com/TheRedElement/code_snippets.git
```

In case you want use the repo inside your own git repo, it is recommended to create a submodule:

```shell
    git submodule add https://github.com/TheRedElement/code_snippets.git
```

This allows you to keep your commits separate from this repo.
You can, of course, `git pull` in the submodule to get the latest changes.
To do so, navigate inside the directory of where you cloned this submodule to and run `git pull` from there.

> [!IMPORTANT]
> If you find this repo useful in your work, a brief acknowledgement would be appreciated.

## Installation

### Python
To install the python package use the following:

```shell
    pip3 install git+https://github.com/TheRedElement/code_snippets.git
```

### Julia


## Development
To install the package while still enabling development (iteratively changing things, editable mode) use the following:

### Julia

<!-- ```shell
    dev .
``` -->

### Python

```shell
    pip3 install --editable .
```

## Testing

### Julia
To run tests for the julia module use the following command in the root directory:

```shell
    julia --project=. -e 'include("src_jl_tests/runtests.jl")'
```

### Python
Given you have some form of the package installed (i.e. in editable mode - [Development](#development)) use the following command in the root directory to run unit tests:

```shell
    pytest CodeSnippets_py_tests/
```