import QuantLib as ql
from src.models.base import AbstractModel

class HestonModel(AbstractModel):
    """
    Heston stochastic volatility model for option pricing.

    This class encapsulates the setup of the Heston model in QuantLib using 
    configuration parameters for volatility dynamics.

    Attributes:
        spot (float): Current spot price of the underlying asset.
        risk_free_curve (ql.YieldTermStructure): Risk-free interest rate curve.
        dividend_curve (ql.YieldTermStructure): Term structure of dividends.
        params: Configuration object containing Heston model parameters:
            - v0: Initial variance
            - kappa: Mean reversion speed
            - theta: Long-term variance
            - sigma: Volatility of variance (vol-of-vol)
            - rho: Correlation between asset and volatility
    """


    def __init__(
            self,
            spot: float,
            risk_free_curve: ql.YieldTermStructure,
            dividend_curve: ql.YieldTermStructure,
            heston_params # from config
        ):
        """
        Initialize the HestonModel with market inputs and Heston parameters.

        Args:
            spot (float): Spot price of the underlying.
            risk_free_curve (ql.YieldTermStructure): Risk-free discount curve.
            dividend_curve (ql.YieldTermStructure): Dividend yield curve.
            heston_params: Object or namespace with Heston model parameters.
        """
        
        self.spot = spot
        self.risk_free_curve = risk_free_curve
        self.dividend_curve = dividend_curve
        self.params = heston_params


    def build(self):
        """
        Build and return the QuantLib Heston model.

        Returns:
            ql.HestonModel: A calibrated Heston model based on the input parameters.
        """

        process = ql.HestonProcess(
            ql.YieldTermStructureHandle(self.risk_free_curve),
            ql.YieldTermStructureHandle(self.dividend_curve),
            ql.QuoteHandle(ql.SimpleQuote(self.spot)),
            self.params.v0,
            self.params.kappa,
            self.params.theta,
            self.params.sigma,
            self.params.rho
        )
        return ql.HestonModel(process)
