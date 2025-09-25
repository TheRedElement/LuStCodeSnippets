
#%%imports
from astropy.cosmology import Cosmology, FlatLambdaCDM
import astropy.units as u
import logging
import numpy as np

logger = logging.getLogger(__name__)

#%%definitions
def number_from_rate(
    rate:u.Quantity, z:float,
    dt_eff:u.Quantity, fov_eff:u.Quantity,
    z_min=0.0,
    cosmo:Cosmology=FlatLambdaCDM(H0=70, Om0=0.3),
    ) -> u.Quantity:
    """
        - function to estimate number of objects that can be observed with some survey

        Parameters
        ----------
            - `rate`
                - `u.Quantity`
                - rate at which a specific object is observed
                - has to have units of `1/(Volume * Time)`
                    - typically `1/(u.Mpc**3 * u.yr)`
            - `z`
                - `float`
                - maximum redshift `rate` is valid up to
            - `dt_eff`
                - `u.Quantity`
                - effective observing baseline of the survey
                - has to have units of `Time`
                - consider typical timescales of your object and adjust `dt_eff` accordingly
            - `fov_eff`
                - `u.Quantity`
                - effective field of view of the survey
                - has to have units
                    - `u.deg**2`
                        - recommended
                        - effective area on the celestial sphere covered by the survey
                    - `u.deg`
                        - angular field of view of the telescope
                        - requires use of an approximation for computation of the output
            - `z_min`
                - `float`, optional
                - minimum redshift `rate` is valid in
                - the default is `0.0`
            - `cosmo`
                - `Cosmology`, optional
                - cosmology to be used for the computation
                - the default is `FlatLambdaCDM(H0=70, Om0=0.3)`

        Raises
        ------
            - `ValueError`
                - if wrong `fov_eff` has wrong units

        Returns
        -------
            - `nobj`
                - `float`
                - number of objects observed, given `rate` and the survey specification

        Dependencies
        ------------
            - `astropy`
            - `logging`
            - `numpy`

        Comments
        --------
            - in case you have a survey with `N` fields of `fov=d*u.deg`
                - pass `fov_eff=np.sqrt(N)*fov` to compensate for area computation
            - if your results are by a factor of about `3` to high compared to observations
                - make sure you multiplied your `rate` with `cosmo.h**3`
            - if your results are by a factor of about `10` to high compared to actual observations
                - check if you accidentally divided your `rate` by `cosmo.h**3`
    """

    #checks
    assert (fov_eff.unit == u.deg**2), "`fov_eff` has to have one of the following units: `u.deg**2`"
    
    
    #cosmological quantities
    V_com_min = cosmo.comoving_volume(z_min)    #observed volume
    V_com_max = cosmo.comoving_volume(z)        #observed volume
    
    #fraction of comoving volume
    A_sky = 4*np.pi * (180/np.pi)**2 * u.deg**2         #area of entire night-sky (~41253 *u.deg**2)
    V_com = fov_eff/A_sky * (V_com_max - V_com_min)     #fraction of the sky actually observed (i.e., Strolger2015)

    """ #alternative: explicit computation of observed volume (equivalent to the above)
    d_com_min = cosmo.comoving_distance(z_min)  #observed distance
    d_com_max = cosmo.comoving_distance(z)      #observed distance
    
    #computation of observed volume from comoving distance
    V_com = fov_eff * (np.pi/(180*u.deg))**2 * (d_com_max**3 - d_com_min**3)/3
    """
    
    #compute number of objects that are observed
    nobj = (rate * V_com * dt_eff).value

    return nobj

