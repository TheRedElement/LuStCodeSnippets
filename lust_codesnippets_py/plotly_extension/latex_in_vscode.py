
def latex_in_vscode():
    """
        - function to enable rendering of latex equations and symbols in VSCode
        -  wokraround from [tomas mazak](https://github.com/microsoft/vscode-jupyter/issues/8131#issuecomment-1589961116)

        Parameters
        ----------

        Raises
        ------
        
        Returns
        -------

        Dependencies
        ------------
            - `plotly`
            - `IPython`

        Comments
        -------- 
    """
    import plotly
    from IPython.display import display, HTML
    plotly.offline.init_notebook_mode()
    display(HTML(
        '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
    ))
    
    return