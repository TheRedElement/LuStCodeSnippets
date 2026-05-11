"""predictor for fitting a model based on [Bazin2011](http://ui.adsabs.harvard.edu/abs/2011A&A...534A..43B/abstract)

- provides
    - the plain model
    - a predictor following scikit learn implementation

Exceptions

Classes
    - `Bazin2011` -- basic model for forward computations
    - `BazinModel` -- predictor to fit Bazin2011 model

Functions

Other Objects
"""

#%%imports
import numpy as np
from scipy import optimize as spo
from typing import Any, List, Tuple

#%%imports
class Bazin2011:
    """implements a model based on Bazin2011

    Attributes
        - `c`
            - `float`
            - constant flux offset
            - see `__init__()` for details
        - `a`
            - `float`
            - amplitude
            - see `__init__()` for details
        - `tau_fall`
            - `float`
            - time constant for decay
            - see `__init__()` for details
        - `tau_rise`
            - `float`
            - time constant for rise
            - see `__init__()` for details
        - `t0`
            - `float`
            - reference time
            - related to `t_peak`
                - see Bazin2011
            - see `__init__()` for details
        - `t_peak`
            - `float`
            - peak time
            - overrides the use of `t0`
            - see `__init__()` for details

    Inferred Attributes

    Methods
        - `bazin_t0()` -- computes `t0` from `t_peak`
        - `bazin_t_peak()` -- computes `t_peak` from `t0`
        - `predict()` -- return flux values for Bazin2011 model

    Dependencies
        - `numpy`
        - `typing`
    """

    def __init__(self,
        c:float, a:float,
        tau_fall:float, tau_rise:float,
        t0:float, t_peak:float=None,
        ):
        """instantiates the model

        Parameters
            - `c`
                - `float`
                - constant flux offset
                - essentially reference flux
            - `a`
                - `float`
                - amplitude
            - `tau_fall`
                - `float`
                - time constant for decay
            - `tau_rise`
                - `float`
                - time constant for rise
            - `t0`
                - `float`
                - reference time
                - related to `t_peak`
                    - see Bazin2011
            - `t_peak`
                - `float`, optional
                - peak time
                - overrides the use of `t0`
                - the default is `None`
                    - uses `t0` instead

        Raises

        Returns
        """

        self.c = c
        self.a = a
        self.tau_fall = tau_fall
        self.tau_rise = tau_rise
        self.t0 = t0
        self.t_peak = t_peak

        #inference
        if t_peak is not None:
            self.t0 = self.bazin_t0(self.t_peak, self.tau_fall, self.tau_rise)
        else:
            self.t_peak = self.bazin_t_peak(self.t0, self.tau_fall, self.tau_rise)
        pass

    def bazin_t0(self,
        t_peak:float,
        tau_fall:float, tau_rise:float,
        ) -> float:
        """returns `t0` from `t_peak` based on the relation provided in Bazin2011

        - `t_peak` is referring to `t_max` in Bazin2011
        - will be `np.nan` if `tau_fall` < `tau_rise`
            - no peak

        Parameters
            - `t_peak`
                - `float`
                - peak time
            - `tau_fall`
                - `float`
                - time constant for decay
            - `tau_rise`
                - `float`
                - time constant for rise
        Raises

        Returns
            - `t0`
                - `float`
                - reference time
                - related to `t_peak`
                    - see Bazin2011
        """

        if np.isclose(tau_fall/tau_rise, 1):
            return np.nan

        t0 = t_peak - tau_rise*np.log(tau_fall/tau_rise - 1)

        return t0
    
    def bazin_t_peak(self,
        t0:float,
        tau_fall:float, tau_rise:float,
        ) -> float:
        """returns `t_peak` from `t0` based on the relation provided in Bazin2011

        - `t_peak` is referring to `t_max` in Bazin2011
        - will be `np.nan` if `tau_fall` < `tau_rise`
            - no peak

        Parameters
            - `t0`
                - `float`
                - reference time
            - `tau_fall`
                - `float`
                - time constant for decay
            - `tau_rise`
                - `float`
                - time constant for rise

        Raises

        Returns
            - `t_peak`
                - `float`
                - time of maximum
        """

        if np.isclose(tau_fall/tau_rise, 1):
            return np.nan

        t_peak = t0 + tau_rise*np.log(tau_fall/tau_rise - 1)

        return t_peak                 

    def predict(self,
        t:float,
        ) -> float:
        """returns flux based on Bazin2011 model

        Parameters
            - `t`
                - `float`
                - time

        Raises

        Returns
            - `flux`
                - `float`
                - computed flux
        """

        #computations
        rise = 1 + np.exp(-(t-self.t0)/self.tau_rise)
        fall = np.exp(-(t-self.t0)/self.tau_fall)

        flux = self.a * fall/rise + self.c
        return flux

class BazinModel:
    """fits Bazin2011 models to the supernnova predictions to filter for noise and nonsensical LCs

    - details in [Bazin2011](https://ui.adsabs.harvard.edu/abs/2011A%26A...534A..43B/abstract)

    Attributes

    Inferred Attributes
        - `chi2_min`
            - `float`
            - minimum chi2 value
        - `p_fit`
            - `Tuple[float]`
            - parameters that minimize chi2

    Methods
        - `bazin_chi2()` -- chi2 of the Bazin2011 model
        - `fit()` -- fits Bazin2011 model to data
        - `predict()` -- predicts new datapoints using fitted Bazin2011 model

    Dependencies
        - `numpy`
        - `scipy`
        - `typing`

    """

    def __init__(self,
        ):
        """constructor for redback model fitter

        Parameters

        Raises

        Returns
        
        """
        
        pass

    def bazin_chi2(self, 
        params:Tuple[float],
        t:float,
        f:float, f_e:float,
        ) -> float:
        """returns chi2 error for the Bazin2011 model

        Parameters
            - params
                - `Tuple[float]`
                - parameters passed to `self.bazin_model()`
            - `t`
                - `float`
                - time
        """
        BM = Bazin2011(*params)
        f_pred = BM.predict(t)          #prediction
        chi2_e = np.nansum(((f - f_pred) / f_e)**2)    #error
        return chi2_e
    
    def fit(self,
        x:np.ndarray, y:np.ndarray,
        y_e:np.ndarray,
        x0:Tuple[Any]=None,
        bounds:List[Tuple]=None,
        ):
        """fits Bazin2011 model to a single object

        - will assign inferred attributes
            - `chi2_min`
            - `p_fit`

        Parameters
            - `x`
                - `np.ndarray`
                - x-values
                - usually time
            - `y`
                - `np.ndarray`
                - y-values
                - usually flux
            - `y_e`
                - `np.ndarray`
                - errors associated with `y`
            - `x0`
                - `Tuple[Any]`
                - initial guess for the parameters of `Bazin2011`
                - entries re `(c, A, tau_fall, tau_rise, t0)`
                - the default is `(1, 1, 10, 30, 15)`
            - `bounds`
                - `List[Tuple]`, optional
                - bounds to use when fitting for correct parameters
                - will be passed to `scipy.optimize.minimize()`
                - the default is `[(-10,100),(1,100),(1,100),(1,100),(0,100)]`
            - `plot_result`
                - `bool`, optional
                - whether to plot the fit result
        
        Raises

        Returns
        """

        #default parameters
        if x0 is None:
            x0 = (1, 1, 10, 30, 15)
        if bounds is None:
            bounds = [(-10,100),(1,100),(1,100),(1,100),(0,100)]

        #chi2 fit
        bounds = [(-10,100),(1,100),(1,100),(1,100),(0,100)]
        res = spo.minimize(self.bazin_chi2,
            x0=x0,
            args=(x, y, y_e),
            bounds=bounds,
        )
        self.p_fit = res["x"]                    #optimum parameters
        self.chi2_min = res["fun"]               #optimum chi2 value

        return

    def predict(self,
        x:np.ndarray
        ) -> np.ndarray:
        """returns prediction made with fitted Bazin2011 model

        Parameters
            - `x`
                - `np.ndarray`
                - x-values
                - usually time

        Raises

        Returns
            - `y_pred`
                - `np.ndarray`
                - prediction
                - usually flux
        """

        BM = Bazin2011(*self.p_fit)
        y_pred = BM.predict(x)
        return y_pred
