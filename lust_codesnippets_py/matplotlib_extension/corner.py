"""defines a custom corner plot interface for matplotlib

- provides utilities to generate
    - sequences of colors
    - colormaps

Exceptions

Classes
    - `CornerPlot` -- api for corner plot creation using matplotlib

Functions

Other Objects
"""
#%%imports
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.figure import Figure
import numpy as np
from scipy import stats
from typing import Tuple, Union

#%%definitions
class CornerPlot:
    """api for corner plot generation

    - class to generate a corner plot given some data and potentially labels

    Attributes

    Methods
        - `__2standardnormal()`
        - `__2d_distributions()`
        - `__1d_distributions()`
        - `plot()`

    Dependencies
        - `matplotlib`
        - `numpy`
        - `scipy`
        - `typing`

    Comments
    """

    def __init__(self) -> None:
        return
    
    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(\n'
            f')'
        )

    def __dict__(self) -> dict:
        return eval(str(self).replace(self.__class__.__name__, 'dict'))

    def __2standardnormal(self,
        d1:np.ndarray, mu1:float, sigma1:float,
        d2:np.ndarray, mu2:float, sigma2:float,
        ) -> Tuple[np.ndarray,float,float,np.ndarray,float,float]:
        """converts input to standard normal distribution

        - private method to convert the input to a standard normal distribution
            - zero mean
            - unit variance
        
        Parameters
            - `d1`
                - `np.ndarray`
                - data of the first coordinate to plot
            - `mu1`
                - `np.ndarray`
                - mean of the first coordinate
            - `sigma1`
                - `np.ndarray`
                - standard deviation of the first coordinate
            - `d2`
                - `np.ndarray`
                - data of the second coordinate to plot
            - `mu2`
                - `np.ndarray`
                - mean of the second coordinate
            - `sigma2`
                - `np.ndarray`
                - standard deviation of the second coordinate

        Raises

        Returns
            - `d1`
                - `np.ndarray`
                - normalized input `d1`
            - `mu1`
                - `float`
                - mean of `d1`
            - `sigma1`
                - `float`
                - standard deviation of `d1`
            - `d2`
                - `np.ndarray`
                - normalized input `d2`
            - `mu2`
                - `float`
                - mean of `d2`
            - `sigma2`
                - `float`
                - standard deviation of `d2`
        """

        d1 = (d1-mu1)/sigma1
        d2 = (d2-mu2)/sigma2
        mu1, mu2 = 0, 0
        sigma1, sigma2 = 1, 1

        return (
            d1, mu1, sigma1,
            d2, mu2, sigma2,       
        )
    
    def __2d_distributions(self,
        idx1:int, idx2:int, idx:int,
        d1:np.ndarray, mu1:float, sigma1:float, l1:str,
        d2:np.ndarray, mu2:float, sigma2:float, l2:str,
        corrmat:np.ndarray,
        y:np.ndarray,
        cmap:Union[str,mcolors.Colormap],
        xvals:np.ndarray, yvals:np.ndarray,
        fig:Figure, nrowscols:int,
        sctr_kwargs:dict=None,
        contour_kwargs:dict=None,
        axvline_kwargs:dict=None,
        ) -> plt.Axes:
        """generates off-diagonal distributions

        - method to generate the (off-diagonal) 2d distributions

        Parameters
            - `idx1`
                - `int`
                - index of y coordinate in use
            - `idx2`
                - `int`
                - index of x coordinate in use
            - `idx`
                - `int`
                - current subplot index
            - `d1`
                - `np.ndarray`
                - data of the first coordinate to plot
            - `mu1`
                - `np.ndarray`
                - mean of the first coordinate
            - `sigma1`
                - `np.ndarray`
                - standard deviation of the first coordinate
            - `l1`
                - `str`
                - label to apply to y coordinate in use
            - `d2`
                - `np.ndarray`
                - data of the second coordinate to plot
            - `mu2`
                - `np.ndarray`
                - mean of the second coordinate
            - `sigma2`
                - `np.ndarray`
                - standard deviation of the second coordinate
            - `l2`
                - `str`
                - label to apply to x coordinate in use
            - `corrmat`
                - `np.ndarray`
                - correlation matrix for all passed coordinates
            - `y`
                - `np.ndarray`
                - labels for each sample
            - `cmap`
                - `str`, `Colormap`
                - name of colormap or `Colormap` instance to color the datapoints
            - `xvals`
                - `np.ndarray`
                - x-values to use for plotting
                - used for generating the normal distribution estimate
                - used for defining x-axis limits
            - `yvals`
                - `np.ndarray`
                - y-values to use for plotting
                - used for generating the normal distribution estimate
                - used for defining y-axis limits
            - `fig`
                - `Figure`
                - figure to plot into
            - `nrowscols`
                - `int`
                - number of rows and columns of the corner-plot
            - `sctr_kwargs`
                - `dict`, optional
                - kwargs to pass to `ax.scatter()`
                - the default is `None`
                    - will be set to `dict(s=1, alpha=0.5, zorder=2)`
            - `countour_kwargs`
                - `dict`, optional
                - kwargs to pass to `ax.contour()`
                - the default is `None`
                    - will be set to `dict(cmap=cur_cmap)`
                    - default cmap

        Raises

        Returns
            - `ax`
                - `plt.Axes`
                - created axes
        """

        cur_cmap = plt.rcParams["image.cmap"]


        #default values
        if sctr_kwargs is None:
            sctr_kwargs = dict(s=1, alpha=0.5, zorder=2)
        if 's' not in sctr_kwargs.keys():       sctr_kwargs['s']        = 1
        if 'alpha' not in sctr_kwargs.keys():   sctr_kwargs['alpha']    = 0.5
        if 'zorder' not in sctr_kwargs.keys():  sctr_kwargs['zorder']   = 2
        if contour_kwargs is None:              contour_kwargs          = dict(cmap=cur_cmap)
        if 'cmap' not in contour_kwargs.keys(): contour_kwargs['cmap']  = cur_cmap
        if axvline_kwargs is None:                  axvline_kwargs              = dict(color='C0', linestyle='--')
        if 'color' not in axvline_kwargs.keys():    axvline_kwargs['color']     = 'C0'
        if 'linestyle' not in axvline_kwargs.keys():axvline_kwargs['linestyle'] = '--'
        
        #add new panel
        ax = fig.add_subplot(nrowscols, nrowscols, idx)
        
        #lines for means
        if mu1 is not None: ax.axhline(mu1, **axvline_kwargs)
        if mu2 is not None: ax.axvline(mu2, **axvline_kwargs)

        #data
        sctr = ax.scatter(
            d2, d1,
            c=y,
            cmap=cmap,
            **sctr_kwargs,
        )
             
        if mu1 is not None and sigma1 is not None:
            
            covmat = np.cov(np.array([d1,d2]))

            xx, yy = np.meshgrid(xvals, yvals)
            mesh = np.dstack((xx, yy))
            
            norm = stats.multivariate_normal(
                mean=np.array([mu1, mu2]),
                cov=covmat,
                allow_singular=True
            )
            cont = ax.contour(yy, xx, norm.pdf(mesh), zorder=1, **contour_kwargs)
        

        #labelling
        if idx1 == nrowscols-1:
            ax.set_xlabel(l2)
        else:
            ax.set_xticklabels([])
        if idx2 == 0:
            ax.set_ylabel(l1)
        else:
            ax.set_yticklabels([])
        ax.tick_params()

        ax.set_xlim(np.nanmin(xvals), np.nanmax(xvals))
        ax.set_ylim(np.nanmin(yvals), np.nanmax(yvals))

        ax.margins(x=0,y=0)

        #add corrcoeff in legend
        ax.errorbar(np.nan, np.nan, color="none", label=r"$r_\mathrm{P}=%.4f$"%(corrmat[idx1, idx2]))
        ax.legend()


        return ax

    def __1d_distributions(self,
        idx:int,
        d1:np.ndarray, mu1:float, sigma1:float,
        y:np.ndarray,
        cmap:Union[str,mcolors.Colormap],
        bins:np.ndarray,
        fig:Figure, nrowscols:int,
        hist_kwargs:dict=None,
        sctr_kwargs:dict=None,
        plot_kwargs:dict=None,
        axvline_kwargs:dict=None,
        ) -> plt.Axes:
        """
            - method to generate (on-diagonal) 1d distributions (i.e. histograms)

            Parameters
            ----------
                - `idx`
                    - `int`
                    - current subplot index
                - `d1`
                    - `np.ndarray`
                    - data of the first coordinate to plot
                - `mu1`
                    - `np.ndarray`
                    - mean of the first coordinate
                - `sigma1`
                    - `np.ndarray`
                    - standard deviation of the first coordinate
                - `y`
                    - `np.ndarray`
                    - labels for each sample
                - `cmap`
                    - `str`, `Colormap`
                    - name of colormap or `Colormap` instance to color the datapoints
                - `bins`
                    - `np.ndarray`
                    - bins to use in the histogram
                - `fig`
                    - `Figure`
                    - figure to plot into
                - `nrowscols`
                    - `int`
                    - number of rows and columns of the corner-plot
                - `hist_kwargs`
                    - `dict`, optional
                    - kwargs to pass to `ax.hist()`
                - `sctr_kwargs`
                    - `dict`, optional
                    - kwargs to pass to `ax.scatter()`
                    - will use only part of the information to format 1d-histograms similarly to the scatters
                - `plot_kwargs`
                    - ``dict`` optional
                    - kwargs to pass to `ax.plot()`
                    - the default is `None`
                        - will be set to `dict(color='C2')`
                - `axvline_kwargs`
                    - `dict` optional
                    - kwargs to pass to `ax.axvline()`
                    - the default is `None`
                        - will be set to `dict(color='C0', linestyle='--')`
                    
            Raises
            ------

            Returns
            -------
                - `ax`
                    - `plt.Axes`
                    - created axes

            Comments
            --------

        """

        #default parameters
        if hist_kwargs is None:                     hist_kwargs                 = dict(density=True, alpha=0.5, zorder=2)
        if 'density' not in hist_kwargs.keys():     hist_kwargs['density']      = True
        if 'alpha' not in hist_kwargs.keys():       hist_kwargs['alpha']        = 0.5
        if 'zorder' not in hist_kwargs.keys():      hist_kwargs['zorder']       = 2
        if sctr_kwargs is None:                     sctr_kwargs                 = dict(s=1, alpha=0.5, zorder=2)
        if 's' not in sctr_kwargs.keys():           sctr_kwargs['s']            = 1
        if 'alpha' not in sctr_kwargs.keys():       sctr_kwargs['alpha']        = 0.5
        if 'zorder' not in sctr_kwargs.keys():      sctr_kwargs['zorder']       = 2        
        if plot_kwargs is None:                     plot_kwargs                 = dict(color='C2')
        if 'color' not in plot_kwargs.keys():       plot_kwargs['color']        = 'C2'
        if axvline_kwargs is None:                  axvline_kwargs              = dict(color='C0', linestyle='--')
        if 'color' not in axvline_kwargs.keys():    axvline_kwargs['color']     = 'C0'
        if 'linestyle' not in axvline_kwargs.keys():axvline_kwargs['linestyle'] = '--'
        
        
        if 'vmin' in sctr_kwargs.keys(): vmin = sctr_kwargs['vmin']
        else:                            vmin = None
        if 'vmax' in sctr_kwargs.keys(): vmax = sctr_kwargs['vmax']
        else:                            vmax = None

        #get colors for distributions
        if isinstance(cmap, str): cmap = plt.get_cmap(cmap)
        if isinstance(y, str):  colors = [y]    ##if no classes got passed
        else:
            ##generate colormap if classes are passed
            colors = cmap(mcolors.Normalize(vmin=vmin, vmax=vmax)(np.unique(y).astype(np.float64)))

        #add panel
        ax = fig.add_subplot(nrowscols, nrowscols, idx)

        #plot histograms
        if 'density' in hist_kwargs.keys():
            if hist_kwargs['density']:  countlab = 'Normalized Counts'
            else:                       countlab = 'Counts'
        else:
            countlab = 'Counts'


        if idx != 1:
            orientation = 'horizontal'
            ax.tick_params(bottom=False, top=True, labelbottom=False, labeltop=True)
            ax.xaxis.set_label_position('top')
            ax.set_xlabel(countlab)
            ax.set_yticklabels(ax.get_yticklabels(), visible=False)
            ax.set_ymargin(0)
        else:
            orientation = 'vertical'
            ax.set_ylabel(countlab)
            ax.set_xticklabels(ax.get_xticklabels(), visible=False)
            ax.set_xmargin(0)

        #plot histograms (color each class in y)
        for yu, c in zip(np.unique(y), colors):
            ax.hist(
                d1[(y==yu)].flatten(),
                orientation=orientation,
                color=c,
                bins=bins,
                **hist_kwargs
            )


        #normal distribution estimate
        if mu1 is not None and sigma1 is not None:
            normal = stats.norm.pdf(bins, mu1, sigma1)
            
            if orientation == 'horizontal':
                ax.plot(normal, bins, **plot_kwargs)
                ax.axhline(mu1, label=r'$\mu=%.2f$'%(mu1), **axvline_kwargs)
            
            elif orientation == 'vertical':
                ax.plot(bins, normal, **plot_kwargs)
                ax.axvline(mu1, label=r'$\mu=%.2f$'%(mu1), **axvline_kwargs)
        
            ax.errorbar(np.nan, np.nan, color='none', label=r'$\sigma=%.2f$'%(sigma1))
            ax.legend()

        return ax
   
    def plot(self,
        X:np.ndarray, y:Union[np.ndarray,str]=None, featurenames:np.ndarray=None,
        mus:np.ndarray=None, sigmas:np.ndarray=None, corrmat:np.ndarray=None,
        bins:Union[int,np.ndarray]=100,
        cmap:Union[str,mcolors.Colormap]=None,
        asstandardnormal:bool=False,
        fig:Figure=None,
        sctr_kwargs:dict=None,
        contour_kwargs:dict=None,
        hist_kwargs:dict=None,
        plot_kwargs:dict=None,
        axvline_kwargs:dict=None,
        ) -> Tuple[Figure,plt.Axes]:
        """creates the corner-plot

        - method to create the corner-plot

        Parameters
            - `X`
                - `np.ndarray`
                - contains samples as rows
                - contains features as columns
            - `y`
                - `np.ndarray`, `str`, optional
                - contains labels corresponding to `X`
                - if a `np.ndarray` is passed
                    - will be used as the colormap
                - if a string is passed
                    - will be interpreted as the actual color
                - the default is `None`
                    - will default to `'C0'`
            - `featurenames`
                - `np.ndarray`, optional
                - names to give to the features present in `X`
                - the default is `None`
                    - will initialize with `'Feature i'`, where `i` is the index at which the feature appears in `X`
            - `mus`
                - `np.ndarray`, optional
                - contains the mean value estimates corresponding to `X`
                - the default is `None`
                    - will be ignored
            - `sigmas`
                - `np.ndarray`, optional
                - contains the standard deviation estimates corresponding to `X`
                - the default is `None`
                    - will be ignored
            - `corrmat`
                - `np.ndarray`, optional
                - correlation matrix for `X`
                - has to have shape `(X.shape[1],X.shape[1])`
                - the default is `None`
                    - will infer the correlation coefficients
            - `bins`
                - `int`, `np.ndarray`, optional
                - number of bins to use in
                    - `ax.histogram()`
                    - `np.meshgrid()` in `self.__2d_distributions()`
                - will be passed to 
                    - `self.__2d_distributions()`
                    - `hist_kwargs`
                        - if not overwritten
                - if `np.ndarray`
                    - will be used as axis limits for ALL axis as well
                    - will use those exact bins for ALL uninque values in `y`
                - if `int`
                    - will automatically calculate the bins
                    - will use the calculated bins for ALL uninque values in `y`
                - to enforce equal ranges for all panels use `bins=np.array(X.min(), X.max(), 100)`
                - the default is `100`
            - `cmap`
                - `str`, `mcolors.Colormap`
                - name of the colormap to use or `Colormap` instance
                - used to color the 1d and 2d distributions according to `y`
                - the default is `None`
                    - will use current default `cmap`
            - `asstandardnormal`
                - `bool`, optional
                - whether to plot the data rescaled to zero mean and unit variance
                - the default is `False`
            - `fig`
                - `Figure`, optional
                - figure to plot into
                - the default is `None`
                    - will create a new figure
            - `sctr_kwargs`
                - `dict`, optional
                - kwargs to pass to `ax.scatter()`
                - the default is `None`
                    - will be set to `dict(s=1, alpha=0.5, zorder=2)`
            - `countour_kwargs`
                - `dict`, optional
                - kwargs to pass to `ax.contour()`
                - the default is `None`
                    - will be set to `dict(cmap=cur_cmap)`                        
                    - will use current default `cmap`
            - `hist_kwargs`
                - `dict`, optional
                - kwargs to pass to `ax.hist()`
                - the default is `None`
                    - will be set to `dict(bins=bins, density=True, alpha=0.5, zorder=2)`
            - `plot_kwargs`
                - `dict` optional
                - kwargs to pass to `ax.plot()`
                - the default is `None`
                    - will be set to `dict(color='C2')`
            - `axvline_kwargs`
                - `dict` optional
                - kwargs to pass to `ax.axvline()`
                - the default is `None`
                    - will be set to `dict(color='C0', linestyle='--')`                        

        Raises

        Returns
            - `fig`
                - 'Figure'
                - the created matplotlib figure
            - `axs`
                - `plt.Axes`
                - axes corresponding to `fig`
        """

        cur_cmap = plt.rcParams["image.cmap"]

        #default parameters
        if y is None: y = 'C1'
        if featurenames is None: featurenames = [f'Feature {i}' for i in np.arange(X.shape[1])]

        if mus is None:
            mus = [None]*len(X)
        if sigmas is None:
            sigmas = [None]*len(X)
        if corrmat is None:
            corrmat = np.corrcoef(X.T)
        if cmap is None: cmap = cur_cmap
        if sctr_kwargs is None:
            sctr_kwargs = dict(s=1, alpha=0.5, zorder=2)
        if 's' not in sctr_kwargs.keys():       sctr_kwargs['s']        = 1
        if 'alpha' not in sctr_kwargs.keys():   sctr_kwargs['alpha']    = 0.5
        if 'zorder' not in sctr_kwargs.keys():  sctr_kwargs['zorder']   = 2
        if contour_kwargs is None:              contour_kwargs          = dict(cmap=cur_cmap)
        if 'cmap' not in contour_kwargs.keys(): contour_kwargs['cmap']  = cur_cmap
        if hist_kwargs is None:
            hist_kwargs = dict(density=True, alpha=0.5, zorder=2)
        if 'density' not in hist_kwargs.keys(): hist_kwargs['density']  = True
        if 'alpha' not in hist_kwargs.keys():   hist_kwargs['alpha']    = 0.5
        if 'zorder' not in hist_kwargs.keys():  hist_kwargs['zorder']   = 2
        if plot_kwargs is None:                     plot_kwargs                 = dict(color='C2')
        if 'color' not in plot_kwargs.keys():       plot_kwargs['color']        = 'C2'
        if axvline_kwargs is None:                  axvline_kwargs              = dict(color='C0', linestyle='--')
        if 'color' not in axvline_kwargs.keys():    axvline_kwargs['color']     = "C0"
        if 'linestyle' not in axvline_kwargs.keys():axvline_kwargs['linestyle'] = '--'
        
        if fig is None: fig = plt.figure()
        nrowscols = X.shape[1]


        idx = 0
        for idx1, (d1, l1, mu1, sigma1) in enumerate(zip(X.T, featurenames, mus, sigmas)):
            for idx2, (d2, l2, mu2, sigma2) in enumerate(zip(X.T, featurenames, mus, sigmas)):
                idx += 1

                if asstandardnormal and mu1 is not None and sigma1 is not None:
                    d1, mu1, sigma1, \
                    d2, mu2, sigma2, =\
                        self.__2standardnormal(
                            d1, mu1, sigma1,
                            d2, mu2, sigma2,
                        )

                #get x and y values (serve as bins as well)
                if isinstance(bins, int):
                        xvals = np.linspace(np.nanmin(d2), np.nanmax(d2), bins)
                        yvals = np.linspace(np.nanmin(d1), np.nanmax(d1), bins)
                else:
                    xvals = bins.copy()
                    yvals = bins.copy() 

                #plotting 2D distributions
                if idx1 > idx2:
                    
                    ax1 = self.__2d_distributions(
                        idx1=idx1, idx2=idx2, idx=idx,
                        d1=d1, mu1=mu1, sigma1=sigma1, l1=l1,
                        d2=d2, mu2=mu2, sigma2=sigma2, l2=l2,
                        corrmat=corrmat,
                        y=y,
                        cmap=cmap,
                        xvals=xvals, yvals=yvals,
                        fig=fig, nrowscols=nrowscols,
                        sctr_kwargs=sctr_kwargs,                        
                        axvline_kwargs=axvline_kwargs,
                    )

                #plotting 1d histograms
                elif idx1 == idx2:

                    axhist = self.__1d_distributions(
                        idx=idx,
                        d1=d1, mu1=mu1, sigma1=sigma1,
                        y=y,
                        cmap=cmap,
                        bins=xvals,
                        fig=fig, nrowscols=nrowscols,
                        hist_kwargs=hist_kwargs,
                        sctr_kwargs=sctr_kwargs,
                        plot_kwargs=plot_kwargs,
                        axvline_kwargs=axvline_kwargs,
                    )            

        #get axes
        axs = fig.axes

        return fig, axs
    