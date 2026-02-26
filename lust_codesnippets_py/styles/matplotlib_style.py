
#%%imports
from cycler import cycler
import json
import logging
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pathlib
from typing import List, Literal

logger = logging.getLogger(__name__)
#%%custom registered mpl elements
#tre colormap
jsonfile = pathlib.Path(__file__).parent / f"../_data/tre_matplotlib.json"  #to load file at runtime
with open(jsonfile, "r", encoding='utf-8') as file:
        
        #read plain text for replacements
        style = file.read()

        #parse json to dict
        style = json.loads(style)

        cmap   = mcolors.LinearSegmentedColormap.from_list(name="tre", colors=style["colors"]["c_plot_cmap"]["dark"])
        cmap_r = cmap.reversed()
        mpl.colormaps.register(cmap, force=True)
        mpl.colormaps.register(cmap_r, force=True)        
        cmap   = mcolors.LinearSegmentedColormap.from_list(name="tre_light", colors=style["colors"]["c_plot_cmap"]["light"])
        cmap_r = cmap.reversed()
        mpl.colormaps.register(cmap, force=True)
        mpl.colormaps.register(cmap_r, force=True)        

#fink colormap
if "fink" in plt.colormaps:
    logger.info("colormap `fink` was already registered ... overwriting existing")

fink_colors = [
    [0.0, "#15284F"],
    # [0.5, "#3C8DFF"],
    [0.5, "#D5D5D3"],
    [1.0, "#F5622E"],
]
cmap   = mcolors.LinearSegmentedColormap.from_list(name="fink", colors=fink_colors)
cmap_r = cmap.reversed()
mpl.colormaps.register(cmap, force=True)
mpl.colormaps.register(cmap_r, force=True)

#%%style definitions
def tre(
    theme:Literal["dark","light"]="dark", cycle:Literal["cycle","batch"]="cycle",
    colorway_override:List[str]=None, cmap_override:str=None,
    ):
    """
        - function applying the RedElement base style
        - used as template for other style variations
        - draws from `/lust_code_snippets_py/_data/tre_matplotlib.json` which is defined via `/styles/tre.json`

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
                - the default is `"cycle"`
            - `colorway_override`
                - `List[str]`, optional
                - override of the default tre colorway (colorway = palette)
                - elements have to be some valid form of matplotlib color definition
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
            - `cycler`
            - `json`
            - `matplotlib` 
            - `pathlib`
            - `typing`

        Comments
        --------
    """

    #preliminary checks
    assert theme in ["dark","light"], f"`theme` has to be one of `'dark'`, `'light'` but got {theme}" 
    assert cycle in ["cycle","batch"], f"`cycle` has to be one of `'cycle'`, `'batch'` but got {cycle}" 

    #load style from json
    jsonfile = pathlib.Path(__file__).parent / f"../_data/tre_matplotlib.json"  #to load file at runtime
    with open(jsonfile, "r", encoding='utf-8') as file:
            
            #read plain text for replacements
            style = file.read()

            #parse json to dict
            style = json.loads(style)

    #returned values
    cmap     = "tre" if cmap_override is None else cmap_override
    colorway = style["colors"]["c_plot_colorway"][theme] if colorway_override is None else colorway_override
    hatches  = style["hatches"][cycle]
    ls       = style["line"]["dash"][cycle][:len(colorway)]
    markers  = style["marker"]["symbol"][cycle]

    #create prop cycle
    prop_cycle = (
        cycler(linestyle=ls) +
        cycler(color=colorway)
    )


    ##############
    #adjust theme#
    ##############
    # for k, v in plt.rcParams.items(): print(k, v)
    #layout related
    ##text
    plt.rcParams["text.usetex"]             = True

    ##fontsizes
    plt.rcParams["font.size"]               = style["fontsizes"]["fs_plot_body"]["value"]
    plt.rcParams["figure.titlesize"]        = "large"
    plt.rcParams["axes.titlesize"]          = "large"
    plt.rcParams["axes.labelsize"]          = "medium"
    plt.rcParams["xtick.labelsize"]         = "medium"
    plt.rcParams["ytick.labelsize"]         = "medium"
    plt.rcParams["legend.title_fontsize"]   = "small"
    plt.rcParams["legend.fontsize"]         = "small"

    ##frame layout
    plt.rcParams["figure.figsize"]          = (style["figure"]["width"]/100, style["figure"]["height"]/100)
    plt.rcParams["figure.dpi"]              = 180

    ##grid layout
    plt.rcParams["axes.grid"]               = style["axes"]["xaxis"]["showgrid"] | style["axes"]["yaxis"]["showgrid"]
    plt.rcParams["axes.grid.which"]         = "major"
    spines = ["top","bottom","left","right"]
    for spine in spines:
        if spine in style["axes"]["xaxis"]["spines"]+style["axes"]["yaxis"]["spines"]:
            plt.rcParams[f"axes.spines.{spine}"]   = True 
        else:
            plt.rcParams[f"axes.spines.{spine}"]   = False
    
    plt.rcParams["grid.alpha"]              = mcolors.to_rgba(style["colors"]["c_plot_grid"][theme])[-1]
    plt.rcParams["grid.color"]              = style["colors"]["c_plot_grid"][theme]
    plt.rcParams["xtick.direction"]         = style["axes"]["xaxis"]["ticks"].replace("side", "")
    plt.rcParams["xtick.minor.visible"]     = "minor" in style["axes"]["xaxis"].keys()
    plt.rcParams["ytick.direction"]         = style["axes"]["yaxis"]["ticks"].replace("side", "")
    plt.rcParams["ytick.minor.visible"]     = "minor" in style["axes"]["xaxis"].keys()

    ##marker and line defaults
    plt.rcParams["errorbar.capsize"]        = max(style["errorbars"]["error_x"]["width"], style["errorbars"]["error_y"]["width"])
    plt.rcParams["lines.linewidth"]         = style["line"]["width"]
    plt.rcParams["lines.linestyle"]         = style["line"]["dash"][cycle][0]
    plt.rcParams["lines.markersize"]        = style["marker"]["size"]
    plt.rcParams["patch.linewidth"]         = style["line"]["width"]
    plt.rcParams["scatter.marker"]          = style["marker"]["symbol"][cycle][0]

    ##legend
    plt.rcParams["legend.framealpha"]       = mcolors.to_rgba(style["colors"]["c_plot_legendbg"][theme])[-1]

    ##saving
    plt.rcParams["savefig.transparent"]     = False
    plt.rcParams["savefig.bbox"]            = "tight"
    plt.rcParams["savefig.dpi"]             = 180

    ##colors
    plt.rcParams["figure.facecolor"]        = style["colors"]["c_bg"][theme]
    plt.rcParams["axes.facecolor"]          = style["colors"]["c_plot_pane"][theme]
    plt.rcParams["text.color"]              = style["colors"]["c_body_text"][theme]
    plt.rcParams["xtick.color"]             = style["colors"]["c_body_text"][theme]
    plt.rcParams["ytick.color"]             = style["colors"]["c_body_text"][theme]
    plt.rcParams["axes.labelcolor"]         = style["colors"]["c_body_text"][theme]
    plt.rcParams["axes.edgecolor"]          = style["colors"]["c_body_text"][theme]
    plt.rcParams["legend.facecolor"]        = style["colors"]["c_plot_legendbg"][theme]
    plt.rcParams["legend.edgecolor"]        = style["colors"]["c_plot_legendborder"][theme]
    plt.rcParams["axes.prop_cycle"]         = prop_cycle
    plt.rcParams["image.cmap"]              = cmap
    plt.rcParams["axes3d.xaxis.panecolor"]  = style["colors"]["c_plot_pane"][theme]
    plt.rcParams["axes3d.yaxis.panecolor"]  = style["colors"]["c_plot_pane"][theme]
    plt.rcParams["axes3d.zaxis.panecolor"]  = style["colors"]["c_plot_pane"][theme]

    return colorway, ls, markers, cmap, hatches

def lust(theme:Literal["dark","light"]="dark", cycle:Literal["cycle","batch"]="cycle"):
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
                - the default is `"cycle"`

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
    
    
    #use `tre` as template but override some settings
    colorway, ls, markers, cmap, hatches = tre(theme, cycle, colorway_override=colorway, cmap_override=cmap)

    return colorway, ls, markers, cmap, hatches

def fink(theme:Literal["dark","light"]="dark", cycle:Literal["cycle","batch"]="cycle"):
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
                - the default is `"cycle"`

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
        cmap        = "fink_r"
        colorway    = ["#15284F", "#3C8DFF", "#D5D5D3", "#F5622E"][1:][::-1]*2
    elif theme == "light":
        cmap        = "fink"
        colorway    = ["#15284F", "#3C8DFF", "#D5D5D3", "#F5622E"]*2
    else:
        raise ValueError("invalid `theme`")

    #use `tre` as template but override some settings
    colorway, ls, markers, cmap, hatches = tre(theme, cycle, colorway_override=colorway, cmap_override=cmap)

    return colorway, ls, markers, cmap, hatches
