# LuStCodeSnippets

repository of some useful code snippets in various programming languages.

Demos on how to use the different snippets and routines can be found in
* [LuStCodeSnippets_jl_demos](./LuStCodeSnippets_jl_demos/) for Julia
* [lust_codesnippets_py_demos](./lust_codesnippets_py_demos) for Python

If you want to use the code simply clone the repo:

```bash
git clone https://github.com/TheRedElement/LuStCodeSnippets.git
```

In case you want use the repo inside your own git repo, it is recommended to create a submodule:

```bash
git submodule add https://github.com/TheRedElement/LuStCodeSnippets.git
```

This allows you to keep your commits separate from this repo.
You can, of course, `git pull` in the submodule to get the latest changes.
To do so, navigate inside the directory of where you cloned this submodule to and run `git pull` from there.

> [!IMPORTANT]
> If you find this repo useful in your work, a brief acknowledgement would be appreciated.

## TODO
- [LuStCodeSnippets_sh](./LuStCodeSnippets_sh/)
    - [ ] update docstrings to enable calling `--help` 

## Installation

### Julia
To install the julia package use the following from within `Pkg`:

```bash
add https://github.com/TheRedElement/LuStCodeSnippets.git#main:LuStCodeSnippets_jl
```

### Python
To install the python package with [uv](https://docs.astral.sh/uv/) (recommended) use the following:

```bash
uv add git+https://github.com/TheRedElement/LuStCodeSnippets.git
```

To install the python package with [pip](https://pypi.org/project/pip/) use the following:
```bash
pip3 install git+https://github.com/TheRedElement/LuStCodeSnippets.git
```

### Bash
To install simply clone the repo and call the following from the repository root:

```bash
source LuStCodeSnippets_sh/*
```

## Dependencies

### Julia
Julia will take care of all dependencies automatically.
They will be stored in:
* [./LuStCodeSnippets_jl/Project.toml](./LuStCodeSnippets_jl/Project.toml) for the package
* [./Project.toml](./Project.toml) for the testing environment

### Python
To keep track of dependencies in a clean manner it is recommended to use [uv](https://docs.astral.sh/uv/).
All the relevant files for [uv](https://docs.astral.sh/uv/) to know what to do are already present in the root directory.
This way, all the dependencties are manged for you.

#### Not Using [uv](https://docs.astral.sh/uv/)?
It is recommended to use [pipreqs](https://pypi.org/project/pipreqs/).
To do so run the following at the root of your project (`--force` overwrites any existing requirements.txt file):

```bash
pip3 install pipreqs
pipreqs . --force
```

## Development
To install the package while still enabling development (iteratively changing things, editable mode) use the following:

### Julia

```bash
dev ./LuStCodeSnippets_jl
```

### Python
In case you use [uv](https://docs.astral.sh/uv/) there's no need to install the package separately, as [uv](https://docs.astral.sh/uv/) will take care of that when executing scripts (automatic choice of correct environment)

#### Not Using [uv](https://docs.astral.sh/uv/)?
Call the following:
```bash
pip3 install --editable .
```

## Testing

### Julia
To run tests for the julia module use the following command in the root directory:

```bash
julia --project=. -e "using Pkg; Pkg.instantiate(); Pkg.status()"
julia --project=. -e 'include("LuStCodeSnippets_jl_tests/runtests.jl")'
```

### Python
When using [uv](https://docs.astral.sh/uv/) testing is as straightforward as calling the following (`uv run` to make sure the correct environment gets used):
```bash
uv run pytest lust_codesnippets_py_tests/
```

#### Not Using [uv](https://docs.astral.sh/uv/)?
Given you have some form of the package installed (i.e. in editable mode - [Development](#development)) use the following command in the root directory to run unit tests:

```bash
pytest lust_codesnippets_py_tests/
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
In principle, [uv](https://docs.astral.sh/uv/) will take care of the proper formatting of [pyproject.toml](./pyproject.toml) for you.
You might need to make some minor adjustments though.

### Styles
The `TheRedElement` style can be found in [./styles/](./styles/).
Using the style can be done as follows:
* $\LaTeX$
    * copy [TRE.sty](./styles/TRE.sty) in your $\LaTeX$ document and import it via `\usepackage[<dark|light>]{TRE}`
* html
    * copy [tre_dark.css](./styles/tre_dark.css) and/or [tre_light.css](./styles/tre_light.css) into your project
    * import by calling `<link rel="stylesheet" href=path2tre_dark.css>` and `<link rel="stylesheet" href=path2tre_light.css>`

## Comments