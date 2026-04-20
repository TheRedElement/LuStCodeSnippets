"""routines for table rading and creation

Exceptions

Classes

Functions
    - `prepend()` -- prepends some string to a file

Other Objects
"""
#%%imports

#%%definitions
def prepend(filename:str, s:str):
    """prepends `s` to `filename`

    - WARNING: will override the content of current version of `filename`

    Parameters
        - `filename`
            - `str`
            - path to the file to prepend
        - `s`
            - `str`
            - string to prepend to the file

    Raises

    Returns

    Dependencies
    """
    with open(filename, "r") as f:
        text = f.read()

    with open(filename, "w") as f:
        text = s + text
        f.write(text)
    return