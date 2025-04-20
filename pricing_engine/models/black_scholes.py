import QuantLib as ql

from pricing_engine.models.base import AbstractModel

class BlackScholesModel(AbstractModel):
    """
    Black-Scholes-Merton model implementation for option pricing.

    This class wraps the construction of a QuantLib Black-Scholes-Merton process
    using the provided market inputs.

    Attributes:
        spot (float): Current spot price of the underlying asset.
        dividend_curve (ql.YieldTermStructure): Term structure of dividends.
        risk_free_curve (ql.YieldTermStructure): Risk-free interest rate curve.
        vol_surface (ql.BlackVolTermStructure): Volatility surface (must be BlackVolTermStructure).
    """


    def __init__(
            self,
            spot: float,
            dividend_curve: ql.YieldTermStructure,
            risk_free_curve: ql.YieldTermStructure,
            vol_surface # ql.VolatilitySurface depending on regime
        ):
        """
        Initialize the Black-Scholes-Merton model.

        Args:
            spot (float): Spot price of the underlying.
            dividend_curve (ql.YieldTermStructure): Dividend yield curve.
            risk_free_curve (ql.YieldTermStructure): Risk-free rate curve.
            vol_surface (ql.BlackVolTermStructure): Volatility surface.
        """

        super().__init__()

        self.spot = spot
        self.dividend_curve = dividend_curve
        self.risk_free_curve = risk_free_curve
        self.vol_surface = vol_surface


    def build(self):
        """
        Build and return the QuantLib Black-Scholes-Merton process.

        Returns:
            ql.BlackScholesMertonProcess: The process object for use in pricing engines.

        Raises:
            TypeError: If vol_surface is not an instance of ql.BlackVolTermStructure.
        """
        
        if not isinstance(self.vol_surface, ql.BlackVolTermStructure):
            raise TypeError("vol_surface must be a QuantLib BlackVolTermStructure")

        return ql.BlackScholesMertonProcess(
            ql.QuoteHandle(ql.SimpleQuote(self.spot)),
            ql.YieldTermStructureHandle(self.dividend_curve),
            ql.YieldTermStructureHandle(self.risk_free_curve),
            ql.BlackVolTermStructureHandle(self.vol_surface)
        )