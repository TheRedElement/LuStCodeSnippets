
#%%imports
import pytest
from src_py.astronomy import absmag

from astropy.cosmology import FlatLambdaCDM
import numpy as np

#%%tests
class Test_absmag:
    
    @pytest.fixture(
            params=[
            (22.6803, 0.36966, "g", 41.3716),
            (21.333, 0.29686, "Y", 40.8982),
            (24.031, 0.89888, "z", 43.6493),
            (22.5743, 0.48813, "Y", 42.1856),
            (21.7198, 0.26775, "z", 40.9014),
            (22.7008, 0.4351, "g", 42.123),
            (22.7698, 0.43774, "Y", 41.9706),
            (20.9328, 0.26628, "r", 40.5791),
            (22.0543, 0.35791, "Y", 41.4181),
            (23.3303, 0.6291, "g", 42.8509),
            (23.7241, 0.76584, "Y", 43.3872),
            (22.9417, 0.45394, "r", 42.1279),
            (22.5284, 0.49743, "z", 41.9505),
            (23.2806, 0.38809, "z", 41.819),
            (23.1372, 0.63681, "Y", 42.7893),
            (22.8268, 0.53112, "Y", 42.3827),
            (23.3801, 0.65992, "r", 43.0052),
            (22.0423, 0.32988, "Y", 41.0865),
            (22.7398, 0.50394, "g", 42.1735),
            (22.6445, 0.49611, "g", 42.0243),
        ]
    )
    def action(self, request):
        #arrange
        cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

        #act
        m  = request.param[0]
        z  = request.param[1]
        pb = request.param[2]
        mu = request.param[3]
        M, std, offset = absmag.absmag(m, z, cosmo, pb, "./data/lut_snana_snia.csv")

        mu_pred = m - M
        return mu_pred, std, offset, mu

    #assert
    def test_outtypes(self, action):
        mu_pred, std, offset, mu = action
        assert isinstance(mu_pred, (float, int))
        assert isinstance(std, (float, int, np.ndarray)) or np.isnan(std)
        assert isinstance(offset, (float, int, np.ndarray)) or np.isnan(offset)

    def test_absmag(self, action):
        assert action[0] == pytest.approx(action[3], rel=1e-2)
