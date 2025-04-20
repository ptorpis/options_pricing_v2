import QuantLib as ql

from pricing_engine.environment.conventions import Conventions
from pricing_engine.environment.underlying import Underlying
from pricing_engine.environment.volatility import VolatilitySurfaceFactory
from pricing_engine.environment.yield_curves import YieldCurveBuilder


class MarketEnvironment:
    """
    A class that encapsulates all market-related data required for option pricing.

    This class holds all the necessary market data such as pricing date, calendar,
    day count convention, underlying asset, volatility surface, risk-free curve,
    and dividend curve. It also provides a method to build these data structures
    from a configuration.

    Attributes:
        pricing_date (ql.Date): The pricing date used for building curves and volatilities.
        calendar (ql.Calendar): The calendar used for date adjustments.
        day_count (ql.DayCounter): The day count convention used for interest rate calculations.
        underlying (Underlying): An object representing the underlying asset (e.g., stock).
        vol_surface (ql.BlackVolTermStructure): The volatility surface used in option pricing.
        risk_free_curve (ql.YieldTermStructure): The risk-free yield curve.
        dividend_curve (ql.YieldTermStructure): The dividend yield curve.

    Methods:
        from_config(cfg): 
            Creates a MarketEnvironment instance from the provided configuration.

        __repr__(): 
            Returns a string representation of the MarketEnvironment object, including key market details.
    """


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
        """
        Initialize the MarketEnvironment instance with the given market data.

        Args:
            pricing_date (ql.Date): The pricing date used for constructing the curves.
            calendar (ql.Calendar): The calendar used for date adjustments.
            day_count (ql.DayCounter): The day count convention used for curve calculations.
            underlying (Underlying): The underlying asset.
            vol_surface (ql.BlackVolTermStructure): The volatility surface to be used.
            risk_free_curve (ql.YieldTermStructure): The risk-free yield curve.
            dividend_curve (ql.YieldTermStructure): The dividend yield curve.
        """

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
        """
        Create a MarketEnvironment instance from the given configuration.

        This class method reads the configuration and constructs the market environment
        by initializing the necessary data structures like the volatility surface, 
        risk-free curve, and dividend curve based on the configuration.

        Args:
            cfg (pydantic config object): The configuration dictionary containing market parameters.

        Returns:
            MarketEnvironment: An instance of the MarketEnvironment class.
        """

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


