
#%%imports
import astroLuSt.physics.photometry as alphphp
import astropy as ap
import numpy as np
from typings import Union, Literal

#%%definitions
@np.vectorize
def absmag(
    m:float, z:float,
    cosmo:ap.cosmology.Cosmology,
    dm:float=0.0, dz:float=0.0,
    pb:Literal["g","r","i","z"]=None,
    fn_confstats:Union[str,bool]=False,
    ):
    """
        #TODO: error propagation for z?
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
            - `dm`
                - `float`, optional
                - uncertainty of `m`
                - the default is `0.0`
            - `dz`
                - `float`, optional
                - uncertainty of `z`
                - the default is `0.0`
            - `pb`
                - Literal["g","r","i","z"], optional
                - passband to use for the confidence estimate
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
            - `dM`
                - `float`
                - uncertainty estimate of `M`
                - computed by
                    - propagating uncertainties
                    - adding `"std"`/dispersion (if available)
            - `offset`
                - `float`
                - offset from literature value

        Dependencies
        ------------
            - `astroLuSt`
            - `astropy`
            - `csv`
            - `numpy`
            - `typing`

        Comments
        --------
            - confidence estimate
                - will be added to `dM` if available

    """

    if isinstance(fn_confstats, str):
        with open(fn_confstats) as f:
            pb_errs = [
                {k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)
            ]
    else:
        pb_errs = None

    #compute luminosity distance from redshift
    d_lum = cosmo.luminosity_distance(z).to("pc").value
    
    #compute absolute magnitude by using distance module
    DM = alphph.DistanceModule(m=m, d=d_lum, dm=dm)
    M       = DM.M

    #get error for current input (adapt depending on passed value for `fn_confstats`)
    if pb_errs is not None:
        pb_err = [d for d in pb_errs if (d["passband"]==pb)]
        if len(pb_err) > 0:
            pb_err = min(pb_err, key=lambda d: abs(float(d["z_bin"]) - z)) #get correct redshift bin
            offset  = float(pb_err["offset"])
            dM      = DM.dM + float(pb_err["std"])
        else:
            offset  = np.nan
            dM      = DM.dM
    else:
        offset = np.nan
        dM      = DM.dM
    
    return M, dM, offset

