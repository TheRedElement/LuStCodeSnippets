
#%%imports
import pytest
from lust_codesnippets_py.sklearn_extension import decision_tree_convenience

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

#%%tests
class Test_get_nodes:
    
    @pytest.fixture(
        params=[
            (0, 0, 3, [0,1,2,3,4,5,6,7,8]),
            (0, 0, 2, [0,1,2,3,6]),
            (1, 0, 2, [1]),
            (2, 0, 2, [2,3,4,5,6,7,8]),
            (2, 1, 2, [2,3,6]),
        ]
    )
    def action(self, request):
        #arrange
        ##load data
        data = load_iris()
        X, y = data["data"], data["target"]
        features = data["feature_names"]
        
        ##train classifier
        DTC = DecisionTreeClassifier(max_depth=3)
        DTC.fit(X, y)

        #act
        node, depth, max_depth, nodes_true  = request.param
        nodes_pred = decision_tree_convenience.get_nodes(DTC.tree_, node, depth, max_depth)

        return nodes_pred, nodes_true

    #assert
    def test_absmag(self, action):
        assert action[0] == action[1]
