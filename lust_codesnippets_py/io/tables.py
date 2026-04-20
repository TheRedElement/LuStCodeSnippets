"""routines for table reading and creation

Exceptions

Classes

Functions
    - `make_header()` -- generates a custom header describing some table

Other Objects
"""

#%%imports
import json
from typing import Dict, List, Union

#%%definitions
def make_header(
    schema:List[Dict[str,str]],
    description:str,
    as_string:bool=True,
    comment_prefix="#",
    dumps_kwargs:dict=None,
    ) -> Union[dict,str]:
    """generates a header for tables

    - will generate a json string that can be used as header in tables

    Parameters
        - `schema`
            - `List[Dict[str,str]]`
            - schema of the table
            - each list item describes a column
            - required entries in the schema
                - `name`
                - `type`
                    - preferably shorthand form of a datatype
                        - i.e., f64 instead of float64, str instead of string
                - `description`
                - `missing`
                    - describes how missing values are denoted
        - `description`
            - `str`
            - description of the table
        - `as_string`
            - `bool`, optional
            - whether to return the result as a string
            - the default is `True`
        - `comment_prefix`
            - `str`, optional
            - prefix denoting a comment
            - only relevant when `as_string==True`
            - important for i.e., prepending the header to a `csv` file
            - the default is `#`
        - `dumps_kwargs`
            - `dict`, optional
            - kwargs to pass to `json.dumps()`
            - the default is `None`
                - set to `dict()`

    Raises
        - `AssertionError`
            - if required fields are missing in the schema
    
    Returns
        - `header`
            - `dict`, `str`
            - the generated header
    
    Dependencies
        - `json`
        - `typing`
    
    """

    #default parameters
    if dumps_kwargs is None: dumps_kwargs = dict()
    required = ["name", "type", "description", "missing"]
    
    #checks
    for r in required:
        for col in schema:
            assert r in col.keys(), f"{r} is required in the schema but got {col.keys()}"

    header = {
        "description": [d.strip() for d in description.split("\n")],
        "$schema": schema
    }

    if as_string:
        header = json.dumps(header, **dumps_kwargs)
        header = header.replace("\n", "\n"+comment_prefix)
        header = comment_prefix + header

    return header