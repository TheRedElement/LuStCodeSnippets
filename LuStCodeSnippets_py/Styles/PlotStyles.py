
#%%imports
from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np

#%%global setup
def layout_specs():
    """
        - function to set layout specifications that apply to all styles

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
            - `mono_colors`
                - `np.ndarray`
                - colors used in monochromatic styles
            - `mono_ls`
                - `np.ndarray`
                - linestyles used in monochromatic styles
            - `mono_markers`
                - `np.ndarray`
                - markes used in monochromatic styles
            - `mono_hatches`
                - `np.ndarray`
                - hatches used in monochromatic styles

        Dependencies
        ------------
            - `matplotlib`
            - `numpy`

        Comments
        -------- 
    """
    
    # for k, v in plt.rcParams.items(): print(k, v)
    #text
    plt.rcParams["text.usetex"]             = True

    #fontsizes
    plt.rcParams["font.size"]               = 16
    plt.rcParams["figure.titlesize"]        = "large"
    plt.rcParams["axes.titlesize"]          = "large"
    plt.rcParams["axes.labelsize"]          = "medium"
    plt.rcParams["xtick.labelsize"]         = "medium"
    plt.rcParams["ytick.labelsize"]         = "medium"
    plt.rcParams["legend.title_fontsize"]   = "small"
    plt.rcParams["legend.fontsize"]         = "small"

    #frame layout
    plt.rcParams["figure.figsize"]          = (9.0,5.0)
    plt.rcParams["figure.dpi"]              = 180

    #grid layout
    plt.rcParams["axes.grid"]               = True
    plt.rcParams["axes.grid.which"]         = "major"
    plt.rcParams["grid.alpha"]              = 0.3

    #marker and line defaults
    plt.rcParams["lines.linewidth"]         = 2
    plt.rcParams["lines.linewidth"]         = 2
    plt.rcParams["lines.linestyle"]         = "-"
    plt.rcParams["lines.markersize"]        = 4
    plt.rcParams["scatter.marker"]          = "o"

    #legend
    plt.rcParams["legend.framealpha"]       = 0.2                   #:fglegend, :legendbackgroundcolor

    #python specific
    plt.rcParams["errorbar.capsize"]        = 3
    plt.rcParams["savefig.transparent"]     = False
    plt.rcParams["savefig.bbox"]            = "tight"
    plt.rcParams["savefig.dpi"]             = 180
    plt.rcParams["xtick.direction"]         = "in" 
    plt.rcParams["ytick.direction"]         = "in" 
    plt.rcParams["xtick.minor.visible"]     = True
    plt.rcParams["ytick.minor.visible"]     = True
    plt.rcParams["axes.spines.top"]         = False
    plt.rcParams["axes.spines.right"]       = False


    #options for monochrome plots
    """
        - has presets for `ncolors_mono*nlinestyles_mono` lines
        - has presets for `ncolors_mono*nmarkers_mono` markers
        - `mono_ls` contains `ncolors_mono*nlinestyles_mono` linestyles.
            - Each ls gets repeated `ncolors_mono` times
            - Then the next color is applied
        - `mono_markers` contains `ncolors_mono*nmarkers_mono` markers.
            - Each marker gets repeated `ncolors_mono` times
            - Then the next color is applied
        - The idea here is that each `mono_ls`/`mono_markers` will be plotted in each color, then plot the proceed to the next  in the next `mono_ls`/`mono_markers` etc.
            - This way, the lines/scatters will always be distinguishable
    """

    ncolors_mono        = 3

    mono_colors_base = plt.get_cmap("gray")(np.linspace(0,1,ncolors_mono+2))[1:-1]
    mono_ls_base        = ["-", "--", ":", "-."]              #linestyles to cycle through when plotting
    mono_markers_base   = ["o", "^", "v", "d", "x"]
    mono_hatches_base   = ["/","\\","o","*", "|"]

    nlinestyles_mono    = len(mono_ls_base)                         #number of defined linestyles
    nmarkers_mono       = len(mono_markers_base)                    #number of defined linestyles

    mono_colors         = np.repeat(mono_colors_base[np.newaxis,:,:], nlinestyles_mono, axis=0).reshape(-1,4)
    mono_ls             = np.repeat(mono_ls_base, ncolors_mono, axis=0)
    mono_markers        = np.repeat(mono_markers_base, ncolors_mono, axis=0)
    mono_hatches        = np.repeat(mono_hatches_base, ncolors_mono, axis=0)

    return mono_colors, mono_ls, mono_markers, mono_hatches

#%%style definitions
def tre_light():
    """
        - function defining a monochrome style that contains one red element

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
            - `tre_light_palette`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `tre_light_ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `tre_light_markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `tre_light_cmap`
                - `string`
                - colormap used in the style
            - `tre_light_hatches`
                - `np.ndarray`
                - hatches used in style

        Dependencies
        ------------
            - `cycler`
            - `matplotlib` 
            - `numpy`

        Comments
        --------
    """

    mono_colors, mono_ls, mono_markers, mono_hatches = layout_specs()

    tre_light_markers   = ["o", *mono_markers]
    tre_light_ls        = ["-", *mono_ls]
    tre_light_palette   = [(161/255,0,0,1), *mono_colors]
    tre_light_hatches   = mono_hatches

    prop_cycle = (
        cycler(linestyle=tre_light_ls) +
        cycler(color=tre_light_palette)
    )

    tre_light_cmap = "gray_r"

    tre_light_bg = "FFFFFF"

    #color scheme                                               #julia equivalent
    plt.rcParams["figure.facecolor"]        = tre_light_bg      #:bg
    # plt.rcParams["figure.edgecolor"]      = (0,0,0,1)     
    plt.rcParams["axes.facecolor"]          = "FFFFFF"          #:bginside
    plt.rcParams["text.color"]              = (0,0,0,1)         #:fgtext, :legendfontcolor, :legendtitlefontcolor, :titlefontcolor
    plt.rcParams["xtick.color"]             = (0,0,0,1)         #:fgtext
    plt.rcParams["ytick.color"]             = (0,0,0,1)         #:fgtext
    plt.rcParams["axes.labelcolor"]         = (0,0,0,1)         #:fgtext
    plt.rcParams["axes.edgecolor"]          = (0,0,0,1)         #:fgguide
    plt.rcParams["legend.facecolor"]        = "inherit"         #:fglegend, :legendbackgroundcolor
    plt.rcParams["legend.edgecolor"]        = "inherit"               #
    plt.rcParams["axes.prop_cycle"]         = prop_cycle        #:palette, cycling through :ls
    plt.rcParams["image.cmap"]              = tre_light_cmap    #:colorgradient
    plt.rcParams["axes3d.xaxis.panecolor"]  = (1,1,1,.9)        #
    plt.rcParams["axes3d.yaxis.panecolor"]  = (1,1,1,.9)        #
    plt.rcParams["axes3d.zaxis.panecolor"]  = (1,1,1,.9)        #

    return tre_light_palette, tre_light_ls, tre_light_markers, tre_light_cmap, tre_light_hatches

def tre_dark():
    """
        - function defining a monochrome style that contains one red element

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
            - `tre_dark_palette`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `tre_dark_ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `tre_dark_markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `tre_dark_cmap`
                - `string`
                - colormap used in the style
            - `tre_dark_hatches`
                - `np.ndarray`
                - hatches used in style

        Dependencies
        ------------
            - `cycler`
            - `matplotlib` 
            - `numpy`

        Comments
        --------
    """

    mono_colors, mono_ls, mono_markers, mono_hatches = layout_specs()

    tre_dark_markers   = ["o", *mono_markers]
    tre_dark_ls        = ["-", *mono_ls]
    tre_dark_palette   = [(161/255,0,0,1), *mono_colors[::-1]]
    tre_dark_hatches   = mono_hatches

    prop_cycle = (
        cycler(linestyle=tre_dark_ls) +
        cycler(color=tre_dark_palette)
    )

    tre_dark_cmap = "gray"

    tre_dark_bg = "000000"

    #color scheme                                                   #julia equivalent
    plt.rcParams["figure.facecolor"]        = tre_dark_bg           #:bg
    # plt.rcParams["figure.edgecolor"]        = (1,1,1,1)     
    plt.rcParams["axes.facecolor"]          = "000000"              #:bginside
    plt.rcParams["text.color"]              = (0.75,0.75,0.75,1)    #:fgtext, :legendfontcolor, :legendtitlefontcolor, :titlefontcolor
    plt.rcParams["xtick.color"]             = (0.75,0.75,0.75,1)    #:fgtext
    plt.rcParams["ytick.color"]             = (0.75,0.75,0.75,1)    #:fgtext
    plt.rcParams["axes.labelcolor"]         = (0.75,0.75,0.75,1)    #:fgtext
    plt.rcParams["axes.edgecolor"]          = (0.75,0.75,0.75,1)    #:fgguide
    plt.rcParams["legend.facecolor"]        = "inherit"         #:fglegend, :legendbackgroundcolor
    plt.rcParams["legend.edgecolor"]        = "inherit"               #
    plt.rcParams["axes.prop_cycle"]         = prop_cycle            #:palette, cycling through :ls
    plt.rcParams["image.cmap"]              = tre_dark_cmap         #:colorgradient
    plt.rcParams["axes3d.xaxis.panecolor"]  = (1,1,1,.1)            #
    plt.rcParams["axes3d.yaxis.panecolor"]  = (1,1,1,.1)            #
    plt.rcParams["axes3d.zaxis.panecolor"]  = (1,1,1,.1)            #


    return tre_dark_palette, tre_dark_ls, tre_dark_markers, tre_dark_cmap, tre_dark_hatches

def lust_light():
    """
        - function defining a light style

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
            - `lust_light_palette`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `lust_light_ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `lust_light_markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `lust_light_cmap`
                - `string`
                - colormap used in the style
            - `lust_light_hatches`
                - `np.ndarray`
                - hatches used in style

        Dependencies
        ------------
            - `cycler`
            - `matplotlib` 
            - `numpy`

        Comments
        --------
    """

    mono_colors, mono_ls, mono_markers, mono_hatches = layout_specs()

    lust_light_markers   = [*mono_markers]
    lust_light_ls        = [*mono_ls]
    lust_light_palette   = ["#A10000", "#FF7B00", "#51BFFF", "#CFC100", "#B500BB", "#009E69"]*2
    lust_light_hatches   = mono_hatches

    prop_cycle = (
        cycler(linestyle=lust_light_ls) +
        cycler(color=lust_light_palette)
    )

    lust_light_cmap = "hot"

    lust_light_bg = "FFFFFF"

    #color scheme                                               #julia equivalent
    plt.rcParams["figure.facecolor"]        = lust_light_bg      #:bg
    # plt.rcParams["figure.edgecolor"]      = (0,0,0,1)     
    plt.rcParams["axes.facecolor"]          = "FFFFFF"          #:bginside
    plt.rcParams["text.color"]              = (0,0,0,1)         #:fgtext, :legendfontcolor, :legendtitlefontcolor, :titlefontcolor
    plt.rcParams["xtick.color"]             = (0,0,0,1)         #:fgtext
    plt.rcParams["ytick.color"]             = (0,0,0,1)         #:fgtext
    plt.rcParams["axes.labelcolor"]         = (0,0,0,1)         #:fgtext
    plt.rcParams["axes.edgecolor"]          = (0,0,0,1)         #:fgguide
    plt.rcParams["legend.facecolor"]        = "inherit"         #:fglegend, :legendbackgroundcolor
    plt.rcParams["legend.edgecolor"]        = "inherit"               #
    plt.rcParams["axes.prop_cycle"]         = prop_cycle        #:palette, cycling through :ls
    plt.rcParams["image.cmap"]              = lust_light_cmap    #:colorgradient
    plt.rcParams["axes3d.xaxis.panecolor"]  = (1,1,1,.9)        #
    plt.rcParams["axes3d.yaxis.panecolor"]  = (1,1,1,.9)        #
    plt.rcParams["axes3d.zaxis.panecolor"]  = (1,1,1,.9)        #

    return lust_light_palette, lust_light_ls, lust_light_markers, lust_light_cmap, lust_light_hatches

def lust_dark():
    """
        - function defining a dark style

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
            - `lust_dark_palette`
                - `np.ndarray`
                - contains color palette used to cycle through when plotting
            - `lust_dark_ls`
                - `np.ndarray`
                - contains linestyles used to cycle through when plotting
            - `lust_dark_markers`
                - `np.ndarray`
                - contains markers used to cycle through when plotting
            - `lust_dark_cmap`
                - `string`
                - colormap used in the style
            - `lust_dark_hatches`
                - `np.ndarray`
                - hatches used in style

        Dependencies
        ------------
            - `cycler`
            - `matplotlib` 
            - `numpy`

        Comments
        --------
    """

    mono_colors, mono_ls, mono_markers, mono_hatches = layout_specs()

    lust_dark_markers   = [*mono_markers]
    lust_dark_ls        = [*mono_ls]
    lust_dark_palette   = ["#A10000", "#FF7B00", "#51BFFF", "#FFEE00", "#FA62FF", "#70FFF8"]*2
    lust_dark_hatches   = mono_hatches

    prop_cycle = (
        cycler(linestyle=lust_dark_ls) +
        cycler(color=lust_dark_palette)
    )

    lust_dark_cmap = "hot"

    lust_dark_bg = "000000"

    #color scheme                                                   #julia equivalent
    plt.rcParams["figure.facecolor"]        = lust_dark_bg           #:bg
    # plt.rcParams["figure.edgecolor"]        = (1,1,1,1)     
    plt.rcParams["axes.facecolor"]          = "000000"              #:bginside
    plt.rcParams["text.color"]              = (0.75,0.75,0.75,1)    #:fgtext, :legendfontcolor, :legendtitlefontcolor, :titlefontcolor
    plt.rcParams["xtick.color"]             = (0.75,0.75,0.75,1)    #:fgtext
    plt.rcParams["ytick.color"]             = (0.75,0.75,0.75,1)    #:fgtext
    plt.rcParams["axes.labelcolor"]         = (0.75,0.75,0.75,1)    #:fgtext
    plt.rcParams["axes.edgecolor"]          = (0.75,0.75,0.75,1)    #:fgguide
    plt.rcParams["legend.facecolor"]        = "inherit"         #:fglegend, :legendbackgroundcolor
    plt.rcParams["legend.edgecolor"]        = "inherit"               #
    plt.rcParams["axes.prop_cycle"]         = prop_cycle            #:palette, cycling through :ls
    plt.rcParams["image.cmap"]              = lust_dark_cmap         #:colorgradient
    plt.rcParams["axes3d.xaxis.panecolor"]  = (1,1,1,.1)            #
    plt.rcParams["axes3d.yaxis.panecolor"]  = (1,1,1,.1)            #
    plt.rcParams["axes3d.zaxis.panecolor"]  = (1,1,1,.1)            #


    return lust_dark_palette, lust_dark_ls, lust_dark_markers, lust_dark_cmap, lust_dark_hatches

