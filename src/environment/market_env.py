import QuantLib as ql

from src.environment.conventions import Conventions
from src.environment.underlying import Underlying
from src.environment.volatility import VolatilitySurfaceFactory
from src.environment.yield_curves import YieldCurveBuilder


class MarketEnvironment:
    def __init__(
        self,
        pricing_date: ql.Date,
        calendar: ql.Calendar,
        day_count: ql.DayCounter,
        underlying: Underlying,
        vol_surface: ql.BlackVolTermStructure,
        risk_free_curve: ql.YieldTermStructure,
        dividend_curve: ql.YieldTermStructure
    ):
        self.pricing_date = pricing_date
        self.calendar = calendar
        self.day_count = day_count
        self.underlying = underlying
        self.vol_surface = vol_surface
        self.risk_free_curve = risk_free_curve
        self.dividend_curve = dividend_curve

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

        curve_builder = YieldCurveBuilder(cfg.curves, pricing_date, calendar, day_count)
        risk_free_curve, dividend_curve = curve_builder.build_all()

        return cls(
            pricing_date=pricing_date,
            calendar=calendar,
            day_count=day_count,
            underlying=underlying,
            vol_surface=vol_surface,
            risk_free_curve=risk_free_curve,
            dividend_curve=dividend_curve
        )

    def __repr__(self):
        return (f"MarketEnvironment("
                f"name={self.underlying.name}, "
                f"pricing_date={self.pricing_date}, "
                f"spot={self.underlying.spot}, "
                f"rfr={self.risk_free_curve.zeroRate(1.0, ql.Continuous).rate():.4f}, "
                f"div={self.dividend_curve.zeroRate(1.0, ql.Continuous).rate():.4f}, "
                f"day_count={self.day_count.name()}, "
                f"calendar={self.calendar}, "
                f"vol={self.vol_surface.blackVol(1.0, ql.Continuous)})"
            )


