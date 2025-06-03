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

## Dependencies

### Python
To keep track of dependencies in a clean manner it is recommended to use [pipreqs](https://pypi.org/project/pipreqs/).
To do so run the following at the root of your project (`--force` overwrites any existing requirements.txt file):

```shell
    pip3 install pipreqs
    pipreqs . --force
```

### Julia
Julia will take care of all dependencies automatically.
They will be stored in `Project.toml`.

## Installation

### Python
To install the python package use the following:

```shell
    pip3 install git+https://github.com/TheRedElement/code_snippets.git
```

### Julia
To install the julia package use the following from within `Pkg`:

```shell
    add git+https://github.com/TheRedElement/code_snippets.git
```


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
    julia --project=. -e 'include("CodeSnippets_jl_tests/runtests.jl")'
```

### Python
Given you have some form of the package installed (i.e. in editable mode - [Development](#development)) use the following command in the root directory to run unit tests:

```shell
    pytest CodeSnippets_py_tests/
```

## Comments
* The [src/CodenSnippets.jl](./src/CodeSnippets.jl) file and directory are necessary for julia to know that the repo is a package.