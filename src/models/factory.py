import QuantLib as ql

from src.models.black_scholes import BlackScholesModel
from src.models.heston import HestonModel
from src.engine.engines import BinomialEngine, AnalyticEuropeanEngine, HestonEngine


class ModelFactory:
    """
    Factory for creating model instances for pricing options.

    Provides a static method to instantiate either a Black-Scholes or Heston model
    based on configuration and market data.
    """


    @staticmethod
    def create_model(
        model_type: str,
        spot: float,
        dividend_curve: ql.YieldTermStructure,
        risk_free_curve: ql.YieldTermStructure,
        vol_surface=None, # ql.VolSurface, depending on the regime
        heston_params=None # HestonParams from config
    ):
        """
        Create an instance of a pricing model based on the specified type.

        Args:
            model_type (str): Type of model ('bsm' or 'heston').
            spot (float): Current spot price of the underlying asset.
            dividend_curve (ql.YieldTermStructure): Dividend yield curve.
            risk_free_curve (ql.YieldTermStructure): Risk-free yield curve.
            vol_surface: Black volatility surface for Black-Scholes model.
            heston_params: Heston model parameters from configuration.

        Returns:
            BlackScholesModel or HestonModel: Instantiated model object.

        Raises:
            ValueError: If an unknown model type is provided.
        """
        
        if model_type == "bsm":
            return BlackScholesModel(spot, dividend_curve, risk_free_curve, vol_surface)
        elif model_type == "heston":
            return HestonModel(spot, risk_free_curve, dividend_curve, heston_params)
        else:
            raise ValueError(f"Unknown model type: {model_type}")


class EngineFactory:
    """
    Factory for creating QuantLib-compatible pricing engines.

    Provides a static method to build a pricing engine for a given model
    and selected numerical method (e.g., analytic, binomial, Heston).
    """


    @staticmethod
    def create_engine(
        model, # ql.BlackScholesModel or ql.HestonModel
        engine_type, # From config
        steps=100
    ):
        """
        Create a pricing engine for the specified model and engine type.

        Args:
            model: A Black-Scholes or Heston model instance.
            engine_type (str): Type of engine ('binomial', 'analytic', 'heston').
            steps (int, optional): Number of steps for binomial tree engines.

        Returns:
            ql.PricingEngine: A configured QuantLib pricing engine.

        Raises:
            ValueError: If the engine type is unsupported for the given model.
        """

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

   