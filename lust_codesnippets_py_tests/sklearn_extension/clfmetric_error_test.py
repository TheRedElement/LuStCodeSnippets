
#%%imports
import pytest
from lust_codesnippets_py.sklearn_extension import clfmetric_error as clfe

import numpy as np
#%%tests
class Test_clfmetric_error:
    
    @pytest.fixture(
        params=[
            ([5,5,5,5], [1/np.sqrt(5),1/np.sqrt(5),1/np.sqrt(5),1/np.sqrt(5)],[0,1], 0.0011),   #acc
            ([5,5], [1/np.sqrt(5),1/np.sqrt(5),],[0], 0.0022),   #contamination
        ]
    )
    def action(self, request):
        #arrange

        #act
        quantities, quantities_e, numerator_indices, err  = request.param

        err_pred = clfe.clfmetric_error(quantities, quantities_e, numerator_indices)        

        return err_pred, err

    #assert
    def test_result(self, action):
        err_pred, err = action
        assert err == pytest.approx(np.round(err_pred, 4), rel=1e-4)
    
    def test_outtypes(self, action):
        err_pred, err = action
        assert isinstance(err_pred, float)
    
    def test_input(self):
        with pytest.raises(AssertionError):
            clfe.clfmetric_error([5,5],[5],[0])        
        with pytest.raises(IndexError):
            clfe.clfmetric_error([5,5],[5,5],[3])        

        