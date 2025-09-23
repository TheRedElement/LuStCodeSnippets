
#%%imports
from astropy.cosmology import Cosmology, FlatLambdaCDM, z_at_value
import astropy.units as u

#%%definitions
def observation_limit(
    M_obj:u.Quantity, m_lim:u.Quantity,
    cosmo:Cosmology=FlatLambdaCDM(H0=70, Om0=0.3),
    zmin:float=1e-8, zmax:float=1000, ztol:float=1e-8,
    ) -> u.Quantity:
    """
        - function to determine up to which redshift an object with absolute magnitude `M_obj` is observable given a survey with limiting magnitude `m_lim` is used

        Parameters
        ----------
            - `M_obj`
                - `Quantity`
                - absolute magnitude of the object to be observed
            - `m_lim`
                - `Quantity`
                - limiting magnitude of the survey in use
            - `cosmo`
                - `Cosmology`, optional
                - cosmology to be used for the computation
                - the default is `FlatLambdaCDM(H0=70, Om0=0.3, Tcmb0=2.725)`
            - `zmin`
                - `float`, optional
                - minimum of search range for `z`
                - see [`astropy.cosmology.z_at_value()`](https://docs.astropy.org/en/stable/api/astropy.cosmology.z_at_value.html#astropy.cosmology.z_at_value) docs for details
                - the default is `1e-8`
            - `zmax`
                - `float`, optional
                - maximum of search range for `z`
                - see [`astropy.cosmology.z_at_value()`](https://docs.astropy.org/en/stable/api/astropy.cosmology.z_at_value.html#astropy.cosmology.z_at_value) docs for details
                - the default is `1000`
            - `ztol`
                - `float`, optional
                - error in `z` acceptable for convergence
                - see [`astropy.cosmology.z_at_value()`](https://docs.astropy.org/en/stable/api/astropy.cosmology.z_at_value.html#astropy.cosmology.z_at_value) docs for details
                - the default is `1e-8`
            
        Raises
        ------
            - `AssertionError`
                - if input types are not correct

        Returns
        -------
            - `z`
                - `Quantity`
                - redshift up to which the object is observable
        
        Dependencies
        ------------
            - `astropy`

        Comments
        --------
    """
    
    #checks
    assert isinstance(M_obj, u.Quantity)
    assert isinstance(m_lim, u.Quantity)

    #computation
    mu = m_lim - M_obj
    z = z_at_value(cosmo.distmod, mu, zmin=zmin, zmax=zmax, ztol=ztol)
    return z