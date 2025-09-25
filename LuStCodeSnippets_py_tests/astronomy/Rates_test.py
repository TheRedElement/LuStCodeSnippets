
#%%imports
import pytest
from LuStCodeSnippets_py.Astronomy import Rates

from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import numpy as np

#%%tests
class Test_number_from_rate:

    @pytest.fixture(
        params=[#rate, zmin, zmax, dt_eff, fov_eff, n_true
            (7.0e-5   * 1/(u.Mpc**3 * u.yr), 0.045, 0.25, (5.5/12 * 5*u.yr), 23.0*u.deg**2, 50+69),                                                         #source (rates): Pessi2025, Dahlen2012", source(numbers): Grayling2023, object: sncc
            (1.266e-5 * 1/(u.Mpc**3 * u.yr), 0.045, 0.25, (5.5/12 * 5*u.yr), 23.0*u.deg**2, 50),                                                            #source (rates): Pessi2025", source(numbers): Grayling2023, object: snibc
            (4.3e-5   * 1/(u.Mpc**3 * u.yr), 0.045, 0.25, (5.5/12 * 5*u.yr), 23.0*u.deg**2, 69),                                                            #source (rates): Pessi2025", source(numbers): Grayling2023, object: snii
            (2.43e-5  * 1/(u.Mpc**3 * u.yr), 0.07,  1.14, (5.5/12 * 5*u.yr), 23.0*u.deg**2, 2298),                                                          #source (rates): Frohmaier2019", source(numbers): Moeller2024, object: snia
            # (7.0e-5   * 1/(u.Mpc**3 * u.yr), 0.001, 0.02, ((2018-2014.5) *u.yr), (4*np.pi * (180/np.pi)**2 * u.deg**2 *1/(1-np.sin(15*np.pi/180))), 173),   #source (rates): Pessi2025", source(numbers): Pessi2025, object: sncc
            (0.033e-5 * 1/(u.Mpc**3 * u.yr), 0.001, 0.02, ((2018-2014.5) *u.yr), (4*np.pi * (180/np.pi)**2 * u.deg**2 *1/(1-np.sin(15*np.pi/180))), 2),     #source (rates): Pessi2025", source(numbers): Pessi2025, object: snibc
            # (4.3e-5   * 1/(u.Mpc**3 * u.yr), 0.001, 0.02, ((2018-2014.5) *u.yr), (4*np.pi * (180/np.pi)**2 * u.deg**2 *1/(1-np.sin(15*np.pi/180))), 104),   #source (rates): Pessi2025", source(numbers): Pessi2025, object: snii
            ((np.array([2.1,3.0,3.5,3.6,4.8,5.5,5.9]) * 1e-5).mean() * 1/(u.Mpc**3 * u.yr), 0.07,  0.9, (5.5/12 * 5*u.yr), 23.0*u.deg**2, 2298),            #source(rates): Perrett2012, source(numbers): Moeller2024, object: snia
        ]
    )
    def action(self, request):
        #arrange
        cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

        #act
        rate, zmin, zmax, dt_eff, fov_eff, n_true = request.param
        rate *= cosmo.h

        n_pred = Rates.number_from_rate(rate, zmax, dt_eff, fov_eff, zmin, cosmo)
        return n_pred, n_true

    #assert
    def test_outtypes(self, action):
        n_pred, n_true = action
        assert isinstance(n_pred, float)

    def test_result(self, action):
        print(action[0], action[1])
        True
        assert action[0] == pytest.approx(action[1], rel=0.7)
