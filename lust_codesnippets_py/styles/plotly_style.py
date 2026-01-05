#%%imports
import json
import matplotlib.colors as mcolors
import pathlib
import plotly.graph_objects as go
import plotly.io as pio
import re
from typing import List, Literal

#%%definitions
def tre(theme:Literal["dark","light"]="dark", cycle:Literal["cycle","batch"]="cycle",
    colorway_override:List[str]=None, cmap_override:str=None,
    themename_override:str=None,
    ):
    """
        - function applying the RedElement base style
        - will
            - load the style from the respective json style sheet
            - create a plotly template
            - register the plotly template as f"tre_{theme}"
            - set the template as the default
        - used as template for other style variations
        - draws from `/lust_code_snippets_py/_data/tre_plotly_*.json` which is defined via `/styles/tre.json`

        Parameters
        ----------
            - `theme`
                - `Literal`, optional
                - the theme to use
                - options are
                    - `"dark"`
                    - `"light"`
                - the default is `"dark"`
            - `cycle`
                - `Literal`, optional
                - mode to use for cycling through linestyles, markers, hatches, etc.
                - options are
                    - `"cycle"`
                        - will cycle through the linestyles 
                        - every line consecutive line, marker, hatch, etc. will have a unique style
                    - `"batch"`
                        - will batch similar linestyles together
                        - consecutive lines, markes, hatches, etc. will have the same style
            - `colorway_override`
                - `List[str]`, optional
                - override of the default tre colorway (colorway = palette)
                - elements have to be some valid form of plotly color definition
                    - I recommend hex representation
                - used to make quick customization to the coloration of a plot
                - used in downstream style variations (i.e., `lust()`)
                - the default is `None`
                    - will use the standard tre colorway
            - `cmap_override`
                - `List[str]`, optional
                - override of the default tre cmap (cmap = colorscale)
                - used to make quick customization to the coloration of a plot
                - used in downstream style variations (i.e., `lust()`)
                - the default is `None`
                    - will use the standard tre cmap
            - `themename_override`
                - `str`, optional
                - override of the default theme name when registering to plotly's interface
                - the default is `None`
                    - will use `f"tre_{theme}_{cycle}"`

        Raises
        ------
            - `AssertionError`
                - if some arguments don't comply with supported options 

        Returns
        -------
            - `colorway`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `cmap`
                - `string`
                - colormap used in the style
            - `hatches`
                - `np.ndarray`
                - contains hatches used to cycle through when plotting

        Dependencies
        ------------
            - `json`
            - `matplotlib`
            - `pathlib`
            - `plotly`
            - `re`
            - `typing`

        Comments
        --------
    """

    #preliminary checks
    assert theme in ["dark","light"], f"`theme` has to be one of `'dark'`, `'light'` but got {theme}" 
    assert cycle in ["cycle","batch"], f"`cycle` has to be one of `'cycle'`, `'batch'` but got {cycle}" 

    #to load file at runtime
    jsonfile = pathlib.Path(__file__).parent / f"../_data/tre_plotly_{theme}_{cycle}.json"

    #load style from json
    with open(jsonfile, "r", encoding='utf-8') as file:
            
            #read plain text for replacements
            style = file.read()

            #deal with colors (plotly doesn't like hex with alpha)
            hexcolors = set(re.findall(r"#[\w\d]{8}", style))
            replacement = {hc:mcolors.to_rgba(hc) for hc in hexcolors}
            for (h, rgba) in replacement.items():
                style = style.replace(h, f"rgba({int(rgba[0]*255)},{int(rgba[1]*255)},{int(rgba[2]*255)},{rgba[3]})")

            #parse json to dict
            style = json.loads(style)

    #overrides for variations
    if colorway_override is not None: style["layout"]["colorway"] = colorway_override
    if cmap_override is not None: style["layout"]["colorscale"]["sequential"] = cmap_override
    themename = f"tre_{theme}_{cycle}" if themename_override is None else themename_override

    #returned values
    cmap    = style["layout"]["colorscale"]["sequential"]
    hatches = [e["marker"]["pattern"]["shape"] for e in style["data"]["histogram"]]
    ls      = [e["line"]["dash"] for e in style["data"]["scatter"]]
    markers = [e["marker"]["symbol"] for e in style["data"]["scatter"]]
    colorway = style["layout"]["colorway"]

    #register template
    pio.templates[themename] = go.layout.Template(
          **style
    )
    #set as default
    pio.templates.default = themename
    return colorway, ls, markers, cmap, hatches

def lust(theme:Literal["dark","light"]="dark", cycle:Literal["cycle","batch"]="cycle",):
    """
        - function defining a colorful variation of `tre()`

        Parameters
        ----------
            - `theme`
                - `Literal`, optional
                - the theme to use
                - options are
                    - `"dark"`
                    - `"light"`
                - the default is `"dark"`
            - `cycle`
                - `Literal`, optional
                - mode to use for cycling through linestyles, markers, hatches, etc.
                - options are
                    - `"cycle"`
                        - will cycle through the linestyles 
                        - every line consecutive line, marker, hatch, etc. will have a unique style
                    - `"batch"`
                        - will batch similar linestyles together
                        - consecutive lines, markes, hatches, etc. will have the same style

        Raises
        ------

        Returns
        -------
            - `colorway`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `cmap`
                - `string`
                - colormap used in the style
            - `hatches`
                - `np.ndarray`
                - contains hatches used to cycle through when plotting

        Dependencies
        ------------

        Comments
        --------    
    """
    #override some colors
    if theme == "dark":
        cmap        = "hot_r"
        colorway    = ["#A10000", "#FF7B00", "#51BFFF", "#CFC100", "#B500BB", "#009E69"]*2
    elif theme == "light":
        cmap        = "hot"
        colorway    = ["#A10000", "#FF7B00", "#51BFFF", "#CFC100", "#B500BB", "#009E69"]*2
    else:
        raise ValueError("invalid `theme`")
         
    colorway, ls, markers, cmap, hatches = tre(theme, cycle, colorway_override=colorway, cmap_override=cmap, themename_override=f"lust_{theme}_{cycle}")

    return colorway, ls, markers, cmap, hatches

def fink(theme:Literal["dark","light"]="dark", cycle:Literal["cycle","batch"]="cycle",):
    """
        - function defining a style in the corporate colors of the [FINK](https://fink-broker.org/) collaboration
        - does so by overriding `tre()`

        Parameters
        ----------
            - `theme`
                - `Literal`, optional
                - the theme to use
                - options are
                    - `"dark"`
                    - `"light"`
                - the default is `"dark"`
            - `cycle`
                - `Literal`, optional
                - mode to use for cycling through linestyles, markers, hatches, etc.
                - options are
                    - `"cycle"`
                        - will cycle through the linestyles 
                        - every line consecutive line, marker, hatch, etc. will have a unique style
                    - `"batch"`
                        - will batch similar linestyles together
                        - consecutive lines, markes, hatches, etc. will have the same style

        Raises
        ------

        Returns
        -------
            - `colorway`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `cmap`
                - `string`
                - colormap used in the style
            - `hatches`
                - `np.ndarray`
                - contains hatches used to cycle through when plotting

        Dependencies
        ------------

        Comments
        --------
    """    
    #override some colors
    if theme == "dark":
        cmap        = [
            [0.0, "#15284F"],
            # [0.5, "#3C8DFF"],
            [0.5, "#D5D5D3"],
            [1.0, "#F5622E"],
        ][::-1]
        colorway    = ["#15284F", "#3C8DFF", "#D5D5D3", "#F5622E"][1:][::-1]*2
    elif theme == "light":
        cmap        = [
            [0.0, "#15284F"],
            # [0.5, "#3C8DFF"],
            [0.5, "#D5D5D3"],
            [1.0, "#F5622E"],
        ]
        colorway    = ["#15284F", "#3C8DFF", "#D5D5D3", "#F5622E"]*2
    else:
        raise ValueError("invalid `theme`")
         
    colorway, ls, markers, cmap, hatches = tre(theme, cycle, colorway_override=colorway, cmap_override=cmap, themename_override=f"fink_{theme}_{cycle}")

    return colorway, ls, markers, cmap, hatches
