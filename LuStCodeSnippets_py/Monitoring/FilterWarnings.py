#%%imports
import warnings

#%%definitions
def set_filter():
    """
        - function to filter out some commonly appearing, non-critical warnings

        Parameters
        ----------

        Raises
        ------

        Returns
        -------

        Dependencies
        ------------

        Comments
        --------
            - executed upon import
    """
    warnings.filterwarnings("ignore", message="set_ticklabels()")   #source: matplotlib; trigger: using `ax.set_ticklabels()` without a fixed number of ticks

    return

set_filter()