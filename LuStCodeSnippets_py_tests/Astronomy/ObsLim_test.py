
#%%imports
import pytest
from LuStCodeSnippets_py.Astronomy import ObsLim

from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import numpy as np

#%%tests
class Test_observation_limit:
    
    @pytest.fixture(
        params=[
            (-16.0*u.mag, 23.5*u.mag, 0.1654772*u.mag),
            (-19.5*u.mag, 23.5*u.mag, 0.66229162*u.mag),
            (-16.0*u.mag, 24.5*u.mag, 0.24978182*u.mag),
            (-19.5*u.mag, 24.5*u.mag, 0.96333899*u.mag),
            (-19.3*u.mag, 23.5*u.mag, 0.61404295*u.mag),
            (-19.3*u.mag, 24.5*u.mag, 0.89409072*u.mag),
        ]
    )
    def action(self, request):
        #arrange
        cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

        #act
        M_obj, m_lim, z_true = request.param

        z_pred = ObsLim.observation_limit(M_obj, m_lim, cosmo=cosmo)
        return z_pred, z_true

    #assert
    def test_outtypes(self, action):
        z_pred, z_true = action
        assert isinstance(z_pred, u.Quantity)

    def test_observation_limit(self, action):
        assert action[0].value == pytest.approx(action[1].value, rel=1e-4)
