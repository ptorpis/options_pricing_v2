import QuantLib as ql

from src.models.black_scholes import BlackScholesModel
from src.models.heston import HestonModel
from src.engine.engines import BinomialEngine, AnalyticEuropeanEngine, HestonEngine


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

   