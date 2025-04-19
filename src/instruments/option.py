import QuantLib as ql

from src.utils.config_loader import load_config

from src.models.factory import ModelFactory, EngineFactory
from src.environment.conventions import Conventions
from src.environment.yield_curves import YieldCurveBuilder
from src.environment.volatility import VolatilitySurfaceFactory

class OptionInstrument:
    def __init__(
            self,
            option_type: str,
            strike: float,
            expiry: ql.Date,
            style: str,
            engine: ql.PricingEngine,
            bid_ask_spread: float
        ):
        
        self.option_type = option_type
        self.strike = strike
        self.expiry = expiry
        self.style = style
        self.engine = engine
        self.bid_ask_spread = bid_ask_spread


    @staticmethod
    def from_config(cfg) -> "OptionInstrument":
        expiry_date = ql.DateParser.parseISO(cfg.expiry)
        return OptionInstrument(
            option_type=cfg.option_type,
            strike=cfg.strike,
            expiry=expiry_date,
            style=cfg.style
        )
    

    def payoff(self) -> ql.Payoff:
        if self.option_type == "call":
            return ql.PlainVanillaPayoff(ql.Option.Call, self.strike)
        elif self.option_type == "put":
            return ql.PlainVanillaPayoff(ql.Option.put, self.strike)
        else:
            raise ValueError(f'Unknown option type: {self.option_type}')
        

    def exercise(self) -> ql.Exercise:
        if self.style == "european":
            return ql.EuropeanExercise(self.expiry)
        elif self.style == "american":
            today = ql.Settings.instance().evaluationDate
            return ql.AmericanExercise(today, self.expiry)
        else:
            raise ValueError(f"Unknown option style: {self.style}")
        
    
    def build_option(self) -> ql.VanillaOption:
        return ql.VanillaOption(self.payoff(), self.exercise())
    
    def price(self) -> dict:
        option = self.build_option()

        if not self.engine:
            raise ValueError(
                "No pricing engine set. Pass it during init or set `self.engine` before calling price()."
            )

        option.setPricingEngine(self.engine)

        mid = option.NPV()
        if self.bid_ask_spread > 0.0:
            bid = mid - self.bid_ask_spread / 2
            ask = mid + self.bid_ask_spread / 2
        else:
            bid = ask = mid

        return {
            "mid": mid,
            "bid": bid,
            "ask": ask
        }
    

if __name__ == "__main__":
    cfg = load_config()
    #ql.Settings.instance().evaluationDate = ql.DateParser.parseISO(cfg.market_env.pricing_date)
    model_type = cfg.pricer.model
    spot = cfg.underlying.spot
    pricing_date = ql.DateParser.parseISO(cfg.market_env.pricing_date)
    calendar, day_count = Conventions.from_config(cfg.market_env).build()

    curves_builder = YieldCurveBuilder(cfg.curves, pricing_date, calendar, day_count)

    risk_free_curve, dividend_curve = curves_builder.build_all()
    vol_regime = cfg.market_env.volatility_regime
    vol_surface_config = cfg.volatility_surfaces[vol_regime]

    vol_surface = VolatilitySurfaceFactory.from_config(vol_surface_config)

    ql_vol = vol_surface.build(
        pricing_date=pricing_date,
        calendar=calendar,
        day_count=day_count
    )
    engine_type = cfg.pricer.engine
    model = ModelFactory.create_model(model_type, spot, dividend_curve, risk_free_curve, ql_vol)
    engine = EngineFactory.create_engine(model, engine_type, steps=100)
    
    expiry_date = ql.DateParser.parseISO(cfg.option_instrument.expiry)
    
    option_cfg = cfg.option_instrument
    option = OptionInstrument(
        option_type=option_cfg.option_type,
        strike=option_cfg.strike,
        expiry=expiry_date,
        style=option_cfg.style,
        engine=engine,                   # ⬅ Inject the pricing engine
        bid_ask_spread=0.1              # ⬅ Optional spread
    )
    ql_option = option.build_option()
    price = option.price()
    print(price)
    