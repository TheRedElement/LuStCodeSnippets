
#%%imports
import LuStCodeSnippets_py
import toml


#%%main
#get dependencies
with open("requirements.txt", "r") as f:
    deps = [l.rstrip("\n") for l in f.readlines()]

#load existing pyproject.toml
data = toml.load("pyproject.toml")

#update pyproject.toml
data["build-system"]["requires"] = ["hatchling >= 1.26"]
data["build-system"]["build-backend"] = "hatchling.build"

data["project"]["name"] = LuStCodeSnippets_py.__modulename__
data["project"]["version"] = LuStCodeSnippets_py.__version__
data["project"]["description"] = "repository of some useful code snippets in various programming languages."
data["project"]["readme"] = "README.md"
data["project"]["requires-python"] = ">=3.10"
data["project"]["classifiers"] = ["Programming Language :: Python :: 3", "Operating System :: OS Independent",]
data["project"]["license"] = "MIT"
data["project"]["license-files"] = ["LICEN[CS]E*",]
data["project"]["dependencies"] = deps
data["project"]["authors"] = [{"name":LuStCodeSnippets_py.__author__, "email":LuStCodeSnippets_py.__author_email__},]
data["project"]["maintaners"] = [{"name":LuStCodeSnippets_py.__maintainer__, "email":LuStCodeSnippets_py.__maintainer_email__},]
data["project"]["urls"] = {"Homepage":LuStCodeSnippets_py.__url__, "Issues":LuStCodeSnippets_py.__url__+"/issues"}

data["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"] = [LuStCodeSnippets_py.__modulename__]

#save updated version
with open("pyproject.toml", "w") as f:
    toml.dump(data, f)
