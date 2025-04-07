
#%%imports
import astropy as ap
import csv
import numpy as np
from typing import Union

#%%definitions
@np.vectorize
def absmag(
    m:float, z:float,
    cosmo:ap.cosmology.Cosmology,
    dm:float=0.0, dz:float=0.0,
    pb:str=None,
    fn_confstats:Union[str,bool]=False,
    ):
    """
        - function to convert apparent magnitudes to absolute magnitudes given some redshift
        - considers cosmology to do so

        Parameters
        ----------
            - `m`
                - `float`
                - apparent magnitude
            - `z`
                - `float`
                - redshift
            - `cosmo`
                - `astropy.cosmology.Cosmology`
                - cosmological model to consider for the conversion of `z` to a luminosity distance
            - `pb`
                - str, optional
                - passband to use for the confidence estimate
                - has to be present in the `"passband"` column of `fn_confstats`
                    - will return `np.nan` for `offset` and `std`
                - the default is `None`
                    - no confidence estimate made
            - `fn_confstats`
                - `str`, `bool`, optional
                - path to a lookup table containing confidence estimates for
                    - specific mission
                    - specific astrophysical object
                - has to contain the following columns
                    - `"passband"`
                        - specifies the passband
                    - `"z_bin"`
                        - specifies upper bonud of the redshift bin
                    - `"std"`
                        - specifies standard deviation (dispersion) in some (`"passband", "z_bin"`) combination
                    - `"offset"`
                        - specifies offset from literature value in some (`"passband", "z_bin"`) combination                   

        Raises
        ------

        Returns
        -------
            - `M`
                - `float`
                - computed absolute magnitude
            - `std`
                - `float`
                - `"std"`/dispersion of `M` at given `z`
                - if available
            - `offset`
                - `float`
                - offset  of `M` at given `z` from literature value
                - if available

        Dependencies
        ------------
            - `astropy`
            - `csv`
            - `numpy`
            - `typing`

        Comments
        --------

    """

    #init
    offset = np.nan
    std = np.nan
    
    #get confidence estimates
    if isinstance(fn_confstats, str):
        with open(fn_confstats) as f:   #load lookup table
            pb_errs = [
                {k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)
            ]
        pb_err = [d for d in pb_errs if (d["passband"]==pb)]    #filter for relevant entry in LUT
        if len(pb_err) > 0: #if passband present in LUT
            pb_err = min(pb_err, key=lambda d: abs(float(d["z_bin"]) - z)) #get correct redshift bin
            offset  = float(pb_err["offset"])
            std      = float(pb_err["std"])

    #compute absolute magnitude by using distance module
    mu = cosmo.distmod(z).value
    M = m - mu

    return M, std, offset

