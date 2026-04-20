
#%%imports
from matplotlib import colors as mcolors
import pytest
from lust_codesnippets_py.colors import color_generation

import numpy as np

#%%tests
class Test_generate_categorical_cmap:
    
    @pytest.fixture(
        params=[
            (["r","g","b"], 5, np.array([[1. , 0. , 0. , 1. ],
                [0. , 0.5, 0. , 1. ],
                [0. , 0. , 1. , 1. ],
                [0. , 0. , 1. , 1. ],
                [0. , 0. , 1. , 1. ]])
            ),
            ([[0,0,0,1],[0.3,0.3,0.3,1],[.63,0,0,1]], 10, np.array([[0.  , 0.  , 0.  , 1.  ],
                [0.  , 0.  , 0.  , 1.  ],
                [0.  , 0.  , 0.  , 1.  ],
                [0.3 , 0.3 , 0.3 , 1.  ],
                [0.3 , 0.3 , 0.3 , 1.  ],
                [0.3 , 0.3 , 0.3 , 1.  ],
                [0.63, 0.  , 0.  , 1.  ],
                [0.63, 0.  , 0.  , 1.  ],
                [0.63, 0.  , 0.  , 1.  ],
                [0.63, 0.  , 0.  , 1.  ]])
            ),
        ]
    )
    def action(self, request):
        #arrange

        #act
        colors, res, cmap_true = request.param
        cmap = color_generation.generate_categorical_cmap(colors, res)
        return cmap, cmap_true

    #assert
    def test_output(self, action):
        cmap, cmap_true = action
        assert np.all(cmap.colors == cmap_true)

    def test_outtypes(self, action):
        cmap, cmap_true = action
        assert isinstance(cmap, (mcolors.ListedColormap))


class Test_generate_colors:
    
    @pytest.fixture(
        params=[
            ([0,1,2,3,4], None, None, None, "plasma", ['#0d0887', '#7e03a8', '#cc4778', '#f89540', '#f0f921']),
            ([0,0,1,3,3], 1, 5, 2, "plasma", ['#0d0887', '#0d0887', '#cc4778']),
            (4, None, None, None, "plasma", ['#0d0887', '#0d0887', '#0d0887', '#0d0887']),
        ]
    )
    def action(self, request):
        #arrange

        #act
        classes, vmin, vmax, vcenter,  cmap, colors_true = request.param
        colors = color_generation.generate_colors(classes, vmin, vmax, vcenter, cmap)
        return colors, colors_true

    #assert
    def test_output(self, action):
        colors, colors_true = action
        assert colors == colors_true

    def test_outshape(self, action):
        colors, colors_true = action
        assert np.all(isinstance(c, str) for c in colors)

    def test_outtypes(self, action):
        colors, colors_true = action
        assert isinstance(colors, (list))

