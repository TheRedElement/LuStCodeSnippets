"""utilities for debugging

- specifically targeted at Pdb (PythonDebugger)

Exceptions

Classes

Functions
    - `state()` -- print current state to debugger console

Other Objects
"""
#%%imports
import inspect

#%%definitions
def state(
    fstring:str="%-30s, %15i, %s",
    show_globals:bool=True,
    show_locals:bool=True,
    filter_dunder:bool=True
    ) -> None:
    """displays the current state

    - ONLY TO BE USED FROM WITHIN Pdb (PythonDebugger)!
    - displays
        - locals of current frame
        - globals of current frame
        - additional information for each

    Parameters
        - `fstring`
            - `str`, optional
            - some `%` format-string with 3 fields
                - `variable name`
                - `variable id`
                - `variable repr`
            - to format the output
            - the default is `"%-30s, %15i, %s"`
        - `show_globals`
            - `bool`, optional
            - whether to show global variables
            - the default is `True`
        - `show_locals`
            - `bool`, optional
            - whether to show local variables
            - the default is `True`
        - `filter_dunder`
            - `bool`, optional
            - whether to remove python dunder (`__<name>__`) variables
            - the default is `True`

    Raises

    Returns

    Dependencies
        - `inspect`

    """

    #get previous frame (`state()` creates a new frame)
    frame = inspect.currentframe().f_back

    if show_globals:
        print("GLOBALS:")
        print("--------")
        for k, v in frame.f_globals.items():
            if k.startswith("__") and k.endswith("__") and filter_dunder:
                continue
            print(fstring%(k, id(v), repr(v)))

    print("\n")
    if show_locals:
        print("LOCALS:")
        print("-------")
        for k, v in frame.f_locals.items():
            if k.startswith("__") and k.endswith("__") and filter_dunder:
                continue
            print(fstring%(k, id(v), repr(v)))
    return

