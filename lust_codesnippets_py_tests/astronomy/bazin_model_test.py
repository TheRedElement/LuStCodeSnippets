
#%%imports
import pytest
from lust_codesnippets_py.astronomy import bazin_model

import numpy as np

#%%tests
class Test_Bazin2011:

    @pytest.fixture(
        params=[
            (40, 0, 1, 50, 10, None, 20, 0.4914),
            (40, 0, 1, 50, 10, None, 40, 0.6062),
            (-1, 0, 1, 50, 10, 10, None, 0.3112),
        ]
    )
    def action(self, request):        
        #arrange

        #act
        t, c, A, tau_fall, tau_rise, t0, t_peak, y_true = request.param

        B2011 = bazin_model.Bazin2011(c, A, tau_fall, tau_rise, t0, t_peak)
        y_pred = B2011.predict(t)
        
        return y_pred, y_true

    #assert
    def test_outtypes(self, action):
        y_pred, y_true = action
        assert isinstance(y_pred, float)

    def test_result(self, action):
        y_pred, y_true = action
        assert y_pred == pytest.approx(y_true, rel=0.7)

class Test_BazinModel:

    @pytest.fixture(
        params=[
            (0, 1, 50, 10, None, 20),
            (0, 1, 50, 10, 10, None),
        ]
    )
    def action(self, request):        
        #arrange
        np.random.seed(0)

        #act
        c, A, tau_fall, tau_rise, t0, t_peak = request.param


        #ground truth
        B2011 = bazin_model.Bazin2011(c, A, tau_fall, tau_rise, t0, t_peak)
        p_true = np.array((B2011.c, B2011.a, B2011.tau_fall, B2011.tau_rise, B2011.t0, B2011.t_peak))
        x_true = np.linspace(0,100,100)
        y_true = B2011.predict(x_true)
        y_true /= y_true.max()

        #simulate observations
        ridxs = np.random.permutation(np.arange(len(x_true)))[:80]  #random subset of observations
        x = x_true[ridxs]
        y = y_true[ridxs]
        y_e = 1e-6*np.abs(np.random.normal(size=x.shape))    #no noise (ensure recovery of original params)
        y +=  y_e/y_true.max()
        y /= y.max()

        #fitting a predictor
        x_pred = np.linspace(0,100,100)
        BM = bazin_model.BazinModel()
        BM.fit(x, y, y_e)
        y_pred = BM.predict(x_pred)

        #predicted params
        B2011_pred = bazin_model.Bazin2011(*BM.p_fit)
        p_pred = np.array((B2011_pred.c, B2011_pred.a, B2011_pred.tau_fall, B2011_pred.tau_rise, B2011_pred.t0, B2011_pred.t_peak))

        # #plotting result
        # fig, axs = plt.subplots(1,1, subplot_kw=dict(xlabel="Time [d]", ylabel="Normalized Flux"))
        # axs.errorbar(x, y, yerr=y_e, ls="", marker=".", label="Data")
        # axs.plot(x_pred, y_pred, label="Prediction")
        # axs.plot(x_true, y_true, label="Truth")
        # axs.legend()
        # plt.show()        
        
        return p_pred, p_true

    #assert
    @pytest.mark.filterwarnings("ignore:invalid value encountered in log")
    def test_result(self, action):
        p_pred, p_true = action
        assert p_pred == pytest.approx(p_true, abs=7e-1, nan_ok=True)

