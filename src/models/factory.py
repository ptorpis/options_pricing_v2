import QuantLib as ql

from src.models.black_scholes import BlackScholesModel
from src.models.heston import HestonModel
from src.engine.engines import BinomialEngine, AnalyticEuropeanEngine, HestonEngine

from src.utils.config_loader import load_config

from src.environment.conventions import Conventions
from src.environment.yield_curves import YieldCurveBuilder
from src.environment.volatility import VolatilitySurfaceFactory


class ModelFactory:
    @staticmethod
    def create_model(
        model_type: str,
        spot: float,
        dividend_curve: ql.YieldTermStructure,
        risk_free_curve: ql.YieldTermStructure,
        vol_surface=None, # ql.VolSurface, depending on the regime
        heston_params=None # HestonParams from config
    ):
        
        if model_type == "bsm":
            return BlackScholesModel(spot, dividend_curve, risk_free_curve, vol_surface)
        elif model_type == "heston":
            return HestonModel(spot, risk_free_curve, dividend_curve, heston_params)
        else:
            raise ValueError(f"Unknown model type: {model_type}")


class EngineFactory:
    @staticmethod
    def create_engine(
        model, # ql.BlackScholesModel or ql.HestonModel
        engine_type, # From config
        steps=100
    ):
        # Create the corresponding pricing engine based on model type
        if isinstance(model, BlackScholesModel):
            if engine_type == "binomial":
                engine = BinomialEngine(model.build(), steps)
            elif engine_type == "analytic":
                engine =  AnalyticEuropeanEngine(model.build())
            else:
                raise ValueError(f"Unknown engine type for Black-Scholes: {engine_type}")
        
        elif isinstance(model, HestonModel):
            if engine_type == "heston":
                engine = HestonEngine(model.build())
            else:
                raise ValueError(f"Unknown engine type for Heston model: {engine_type}")
        
        else:
            raise ValueError("Engine not supported for this model type.")
        
        return engine.build()


if __name__ == "__main__":
    cfg = load_config()
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

    heston_params = cfg.pricer.heston_params

    model = ModelFactory.create_model(model_type, spot, dividend_curve, risk_free_curve, ql_vol, heston_params)
    # Create Engine
    engine = EngineFactory.create_engine(model, cfg.pricer.engine, steps=100)

    # Use the engine for pricing
    pricing_results = engine.price()
    print(pricing_results)
   