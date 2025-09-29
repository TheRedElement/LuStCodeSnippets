#%%imports
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from typing import Union, List

#%%definitions
def get_nodes(
    tree:Union[DecisionTreeClassifier,DecisionTreeRegressor],
    node:int=0,
    depth:int=0, max_depth:int=2
    ) -> List[int]:
    """
        - recursive function to obtain all nodes until a depth `max_depth` in a `DecisionTreeClassifier`

        Parameters
        ----------
            - `tree`
                - `DecisionTreeClassifier`
                - tree to extract nodes from
            - `node`
                - `int`, optional
                - id of the node to initialize the search from
                - the default is `0`
                    - root node
            - `depth`
                - `int`, optional
                - current depth of the tree
                - the default is `0`
                    - will serch for `max_depth` levels starting from `node`
            - `max_depth`
                - `int`, optional
                - maximum depth to search relative to `depth`
                - the default is `2`
                    - will search up to 2 levels below `depth`

        Raises
        ------

        Returns
        -------
            - `nodes`
                - `List[int]`
                - list of node ids that got selected

        Dependencies
        ------------
            - `sklearn`
        
        Comments
        --------
    """
    
    #exit conditions
    if node is None:        #no node
        return []
    elif node == -1:        #leaf node
        return []
    elif depth > max_depth: #maximum search depth
        return []
    
    #init output
    nodes = [node]

    #recursion if below depth
    for child in [tree.children_left[node], tree.children_right[node]]:
        nodes.extend(get_nodes(tree, child, depth+1, max_depth))

    return nodes

