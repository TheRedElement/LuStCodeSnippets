#%%imports
import json
import matplotlib.colors as mcolors
import pathlib
import plotly.graph_objects as go
import plotly.io as pio
import re
from typing import Literal

#%%definitions
def tre(theme:Literal["dark","light"]="dark"):
    """
        - function defining the `tre` style
        - will
            - load the style from the respective json style sheet
            - create a plotly template
            - register the plotly template as f"tre_{theme}"
            - set the template as the default

        Parameters
        ----------
            - `theme`
                - `Literal`, optional
                - the theme to use
                - currently supported are
                    - `"dark"`
                    - `"light"`
                - the default is `"dark"`
        
        Raises
        ------

        Returns
        -------

        Dependencies
        ------------
            - `json`
            - `matplotlib`
            - `numpy`
            - `plotly`
            - `re`
            - `typing`
    """

    #to load file at runtime
    jsonfile = pathlib.Path(__file__).parent / f"../_data/tre_plotly_{theme}.json"

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

    #register template
    pio.templates[f"tre_{theme}"] = go.layout.Template(
          **style
    )
    pio.templates.default = f"tre_{theme}"
    return
