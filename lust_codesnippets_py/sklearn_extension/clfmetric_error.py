#%%imports
import numpy as np

#%%constants

#%%definitions
def clfmetric_error(
    quantities:np.ndarray, quantities_e:np.ndarray,
    numerator_indices:np.ndarray[int],
    ) -> float:
    """
        - function to compute the error for expressions of the following form:
        $$
            \\begin{align}
            f(x_1,\\dots,x_N)
                &= \\frac{\\sum_{k=1}^K x_k}{\\sum_{n=1}^{N} x_n},
                    & K \\le N 
                .
            \\end{align}
        $$
        - computes error estimate following gaussian error propagation

        Parameters
        ----------
            - `quantities`
                - `np.ndarry`
                - all arguments of the function $f$
                - the denominator of $f$ is computed as `np.sum(quantities)`
            - `quantities_e`
                - `np.ndarray`
                - error estimates for `quantites`
            - `numerator_indices`
                - `np.ndarray[int]
                - indices pointing to subset of `quantities` that appears in the numerator
                - the numerator of $f$ is computed as `np.sum(quantities[numerator_indices])`
        Raises
        ------
            - `AssertionError`
                - if not enough quantities or quantity uncertainties are passed
        
        Returns
        -------
            - `clfmetric_e`
                - `float`
                - propagated uncertainty of $f$

        Dependencies
        ------------
            - `numpy`
        
        Comments
        --------
            - example for accuracy ((TP+TN)/(TP+TN+FP+FN)): `clfmetric_error([<TP>,<TN>,<FP>,<FN>], [<TP_e>,<TN_e>,<FP_e>,<FN_e>], [0,1])`
                - expressions in `<>` are substituted by the respective value
    """
    assert len(quantities) == len(quantities_e), f"`len(quantities)` has to be equal to `len(quantities_e)` but got {len(quantities)} and {len(quantities_e)} (every quantity needs an error)"

    #type conversions
    quantities = np.array(quantities)
    quantities_e = np.array(quantities_e)
    numerator_indices = np.array(numerator_indices)

    #get equation parts
    denominator = np.sum(quantities)
    numerator = np.sum(quantities[numerator_indices])
    numerator_e = np.sum(quantities_e[numerator_indices])
    denominator_e = np.sum(quantities_e)

    #compute
    f1 = 1/denominator**4
    t1 = (denominator - numerator)**2 * (numerator_e)
    t2 = numerator**2 * (denominator_e - numerator_e)

    clfmetric_e = f1 * (t1 + t2)

    return clfmetric_e