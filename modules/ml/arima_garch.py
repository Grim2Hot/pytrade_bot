from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
import pandas as pd
import numpy as np


class ARIMAEGARCHModel:
    def __init__(self, p=1, d=0, q=1, vol='EGARCH', vol_params=(1, 1, 1)):
        self.p = p
        self.d = d
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
        self.arima_model = ARIMA(log_returns, order=(self.p, self.d, self.q))
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