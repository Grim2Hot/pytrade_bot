from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
import pandas as pd
import numpy as np


class ARIMAEGARCHModel:
    """
    ARIMA-EGARCH model for time series analysis.
    This model combines ARIMA for trend modeling and EGARCH for volatility modeling.
    The expected return is modeled using ARIMA, and the residuals of the prediction are fed into the EGARCH model to assess volatility, or risk.
    p, o, q are required orders for the ARIMA model.
    vol & vol_params are required for the variation of ARCH model used.

    @param p: The order of the Symmetric innovation. The number of GARCH terms (lags of the conditional variance). These terms capture how past volatility (or variance) affects current volatility.

    @param o: The order of the Asymmeteric innovation. The number of leverage terms, or asymmetric terms. These capture how negative and positive shocks affect volatility differently (e.g., bad news having a larger impact than good news). This is a key feature of EGARCH, distinguishing it from standard GARCH.
    
    @param q: The order of the lagged (transformed) conditional variance.
    the number of ARCH terms (lags of the standardized residuals). 
    These terms model how past shocks (squared returns, typically) impact current volatility.

    @param vol: The type of volatility model to use. Default is 'EGARCH'. For long-term volatility, use 'FIGARCH'.

    @param vol_params: Parameters for the volatility model. If a diverent volatility model is used, ensure to set the parameters accordingly.
    Reference arch documentation for more details on the parameters.
    """
    def __init__(self, p=1, o=0, q=1, vol='EGARCH', vol_params=(1, 1, 1)):
        self.p = p
        self.o = o
        self.q = q
        self.vol = vol
        self.vol_params = vol_params
        self.arima_model = None
        self.garch_model = None
        self.fitted_arima = None
        self.fitted_garch = None

    def fit(self, series: pd.Series):
        """
        Fit the ARIMA-EGARCH model to the given time series data.
        """
        log_returns = np.log(series).diff().dropna()
        self.arima_model = ARIMA(log_returns, order=(self.p, self.o, self.q))
        self.fitted_arima = self.arima_model.fit()
        residuals = self.fitted_arima.resid

        self.garch_model = arch_model(residuals, vol=self.vol, p=self.vol_params[0], o=self.vol_params[1], q=self.vol_params[2])
        self.fitted_garch = self.garch_model.fit(disp="off")

        return self

    def forecast_volatility(self, steps=1):
        """
        Forecast future volatility using the fitted GARCH model.
        """
        if self.fitted_garch is None:
            raise ValueError("Model must be fit before forecasting.")
        return self.fitted_garch.forecast(horizon=steps).variance.iloc[-1].values

    def get_residuals(self):
        return self.fitted_arima.resid if self.fitted_arima else None

    def get_volatility_series(self):
        return self.fitted_garch.conditional_volatility if self.fitted_garch else None