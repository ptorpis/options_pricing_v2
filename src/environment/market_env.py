import QuantLib as ql

from src.environment.conventions import Conventions
from src.environment.underlying import Underlying
from src.environment.volatility import VolatilitySurfaceFactory

from src.utils.config_loader import load_config

class MarketEnvironment:
    def __init__(
        self,
        pricing_date: ql.Date,
        calendar: ql.Calendar,
        day_count: ql.DayCounter,
        underlying: Underlying,
        vol_surface: ql.BlackVolTermStructure,
        # yield_curves: ...
    ):
        self.pricing_date = pricing_date
        self.calendar = calendar
        self.day_count = day_count
        self.underlying = underlying
        self.vol_surface = vol_surface
        # self.yield_curves = yield_curves

        ql.Settings.instance().evaluationDate = self.pricing_date


    @classmethod
    def from_config(cls, cfg):
        pricing_date = ql.DateParser.parseISO(cfg.market_env.pricing_date)

        conventions = Conventions.from_config(cfg.market_env)
        calendar, day_count = conventions.build()

        underlying = Underlying.from_config(cfg.underlying)

        vol_regime = cfg.market_env.volatility_regime
        vol_config = cfg.volatility_surfaces[vol_regime]

        vol_surface = VolatilitySurfaceFactory.from_config(vol_config).build(
            pricing_date=pricing_date,
            calendar=calendar,
            day_count=day_count
        )

        # TODO: Yield Curves
        

        return cls(
            pricing_date=pricing_date,
            calendar=calendar,
            day_count=day_count,
            underlying=underlying,
            vol_surface=vol_surface
        )


if __name__ == "__main__":
    cfg = load_config()
    market_env = MarketEnvironment.from_config(cfg)
    print("Spot:", market_env.underlying.spot)
    print("Vol Surface:", market_env.vol_surface)