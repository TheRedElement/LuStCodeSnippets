"""routines for interactions with `hdf5` files

Exceptions

Classes

Functions
    - `tree()` -- prints `hdf5` file structure in tree-format 

Other Objects
"""
#%%imports
import h5py
from typing import Union

#%%definitions
def tree(f:Union[h5py.File,str]):
    """prints structure of `f` in tree-format

    - function to print the tree of a hdf5 file
    - can only deal with hdf5 files of following structure
        - file[groups][datasets]

    Parameters
        - `f`
            - `h5py.File`, `str`
            - file to show the tree of
            - if `h5py.File`
                will use that file
            - if `str`
                - will attempt to open the file, display the tree and close the file
    
    Raises

    Returns

    Dependencies
        - `h5py`

    """
    #open file if necessary
    if isinstance(f, str): f = h5py.File(f, "r")

    #generate tree
    print(f"tree: {f}")
    for gidx, grp in enumerate(f.keys()):
        grp_connector = "|" if gidx != len(f.keys())-1 else "`"
        grp_attrs = ", ".join([f"{k}:{v}" for k,v in f[grp].attrs.items()])
        
        #pretty print
        pad = " "   #padding to ensure tabular layout
        print(f"{grp_connector}--{grp:15s} ({pad:28s} {grp_attrs})")
        for didx, dataset in enumerate(f[grp].keys()):
            #adjust connectors
            grp_connector = " " if gidx == len(f.keys())-1 else grp_connector
            ds_connector = "|" if didx != len(f[grp].keys())-1 else "`"
            #get specifications
            shape = f[grp][dataset].shape
            dtype = f[grp][dataset].dtype
            ds_attrs = ", ".join([f"{k}:{v}" for k,v in f[grp][dataset].attrs.items()])
            
            #pretty pring
            print(f"{grp_connector}  {ds_connector}--{dataset:12s} ({str(shape):15s}, {str(dtype):10s}, {ds_attrs})")
    
    #cleanup
    if isinstance(f, str): f.close()
    
    return
