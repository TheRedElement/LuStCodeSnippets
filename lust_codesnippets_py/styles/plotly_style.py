#%%imports
import json
import matplotlib.colors as mcolors
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

    #load style from json
    with open(f"../../styles/tre_{theme}_plotly.json", "r", encoding='utf-8') as file:
            
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

#%%
import plotly.graph_objects as go
import numpy as np

def style_testplot(palette=None, ls=None, markers=None, cmap=None):
    """
        - function defining a testplot to compare different styles with each other
    """

    layout = go.Layout(**{
        "legend": {
             "title": {
                  "text": "LEGTITLE",
             }
        },
        "xaxis": {
            "domain": [0, 0.45],
            "anchor": "y1",
            "title": {
                "text": "x"
            },
        },
        "yaxis": {
            "domain": [0.7, 1.0],
            "anchor": "x1",
            "title": {
                "text": "y"
            },
        },
        "xaxis2": {
            "domain": [0.55, 1.0],
            "anchor": "y2",
            "title": {
                "text": "x"
            }
        },
        "yaxis2": {
            "domain": [0.7, 1.0],
            "anchor": "x2",
            "title": {
                "text": "y"
            },                    
        },
        "xaxis3": {
            "domain": [0.0, 0.45],
            "anchor": "y3",
            "title": {
                "text": "x"
            }                    
        },
        "yaxis3": {
            "domain": [0.3, 0.6],
            "anchor": "x3",
            "title": {
                "text": "y"
            },
        },
        "xaxis5": {
            "domain": [0.0, 1.0],
            "anchor": "y5",
            "title": {
                "text": "x"
            }                    
        },
        "yaxis5": {
            "domain": [0.0, 0.2],
            "anchor": "x5",
            "title": {
                "text": "Counts"
            },
        },
        "scene1": {
            "xaxis": {
                "title": {
                    "text": "X"
                }
            },
            "yaxis": {
                "title": {
                    "text": "Y"
                }
            },
            "zaxis": {
                "title": {
                    "text": "Z"
                }
            },
            "domain": {
                "x": [0.55, 1.0],
                "y": [0.3, 0.6],
            },
        }         
    })
    traces = [
        *[go.Scatter(
            x=np.arange(-1,1,0.05),
            y=np.arange(-1,1,0.05)+i,
            mode="lines",
            type="scatter",
            xaxis="x1",
            yaxis="y1",
            name="(1,1)"
        ) for i in range(5)],
        *[go.Scatter(
            x=np.random.rand(20),
            y=np.random.rand(20),
            mode="markers",
            type="scatter",
            xaxis="x2",
            yaxis="y2",
            name="(1,2)"
        ) for i in range(5)],
        go.Heatmap(
            z=np.random.rand(50*50).reshape(50,50),
            type="heatmap",
            xaxis="x3",
            yaxis="y3",
            name="(2,1)",
            colorbar=dict(
                len=0.3,
                x=0.45
            )
        ),
        go.Surface(
            z=np.random.rand(50*50).reshape(50,50),
            type="surface",
            scene="scene1",
            name="(2,2)",
            showscale=False,
        ),
        go.Histogram(
            x=np.random.rand(500),
            type="histogram",
            xaxis="x5",
            yaxis="y5",
            name="(3,1),(3,2)",             
        ),
        go.Histogram(
            x=np.random.rand(100),
            type="histogram",
            xaxis="x5",
            yaxis="y5",
            name="(3,1),(3,2)",             
        ),
    ]

    fig = go.Figure(layout=layout, data=traces)

    fig.show()

    return



tre("dark")
# tre("light")
print(pio.templates)
style_testplot()
