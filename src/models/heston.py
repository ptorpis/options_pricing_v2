import QuantLib as ql
from src.models.base import AbstractModel

class HestonModel(AbstractModel):
    def __init__(
            self,
            spot: float,
            risk_free_curve: ql.YieldTermStructure,
            dividend_curve: ql.YieldTermStructure,
            heston_params # from config
        ):
        
        self.spot = spot
        self.risk_free_curve = risk_free_curve
        self.dividend_curve = dividend_curve
        self.params = heston_params

    def build(self):
        # Return the process, not the model
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
