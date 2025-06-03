# LuStCodeSnippets

repository of some useful code snippets in various programming languages.

If you want to use the code simply clone the repo:

```shell
git clone https://github.com/TheRedElement/LuStCodeSnippets.git
```

In case you want use the repo inside your own git repo, it is recommended to create a submodule:

```shell
git submodule add https://github.com/TheRedElement/LuStCodeSnippets.git
```

This allows you to keep your commits separate from this repo.
You can, of course, `git pull` in the submodule to get the latest changes.
To do so, navigate inside the directory of where you cloned this submodule to and run `git pull` from there.

> [!IMPORTANT]
> If you find this repo useful in your work, a brief acknowledgement would be appreciated.

## Installation

### Julia
To install the julia package use the following from within `Pkg`:

```shell
add https://github.com/TheRedElement/LuStCodeSnippets.git#main:LuStCodeSnippets_jl
```

### Python
To install the python package use the following:

```shell
pip3 install git+https://github.com/TheRedElement/LuStCodeSnippets.git
```

## Dependencies

### Julia
Julia will take care of all dependencies automatically.
They will be stored in:
* [./LuStCodeSnippets_jl/Project.toml](./LuStCodeSnippets_jl/Project.toml) for the package
* [./Project.toml](./Project.toml) for the testing environment

### Python
To keep track of dependencies in a clean manner it is recommended to use [pipreqs](https://pypi.org/project/pipreqs/).
To do so run the following at the root of your project (`--force` overwrites any existing requirements.txt file):

```shell
pip3 install pipreqs
pipreqs . --force
```

## Development
To install the package while still enabling development (iteratively changing things, editable mode) use the following:

### Julia

```shell
dev ./LuStCodeSnippets_jl
```

### Python

```shell
pip3 install --editable .
```

## Testing

### Julia
To run tests for the julia module use the following command in the root directory:

```shell
julia --project=. -e "using Pkg; Pkg.instantiate(); Pkg.status()"
julia --project=. -e 'include("LuStCodeSnippets_jl_tests/runtests.jl")'
```

### Python
Given you have some form of the package installed (i.e. in editable mode - [Development](#development)) use the following command in the root directory to run unit tests:

```shell
pytest LuStCodeSnippets_py_tests/
```

## Compiling the Package

### Julia
Run the following command from the root directory to compile the package:
```bash
julia --project=./LuStCodeSnippets_jl -e "using Pkg; Pkg.instantiate(); Pkg.status()"
julia --project=./LuStCodeSnippets_jl ./compile_module.jl
```
This will update [./LuStCodeSnippets_jl/Project.toml](./LuStCodeSnippets_jl/Project.toml) with the latest information about the module.

### Python
Run the following command from the root directory to compile the package:
```bash
source venv/bin/activate
python3 compile_module.py
```

## Comments