import QuantLib as ql

from src.models.base import AbstractModel

class BlackScholesModel(AbstractModel):
    def __init__(
            self,
            spot,
            dividend_curve,
            risk_free_curve,
            vol_surface
        ):
        super().__init__()

        self.spot = spot
        self.dividend_curve = dividend_curve
        self.risk_free_curve = risk_free_curve
        self.vol_surface = vol_surface


    def build(self):
        if not isinstance(self.vol_surface, ql.BlackVolTermStructure):
            raise TypeError("vol_surface must be a QuantLib BlackVolTermStructure")

        return ql.BlackScholesMertonProcess(
            ql.QuoteHandle(ql.SimpleQuote(self.spot)),
            ql.YieldTermStructureHandle(self.dividend_curve),
            ql.YieldTermStructureHandle(self.risk_free_curve),
            ql.BlackVolTermStructureHandle(self.vol_surface)
        )