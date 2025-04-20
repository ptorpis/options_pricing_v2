import QuantLib as ql

from pricing_engine.utils.config_loader import load_config, FullConfig
from pricing_engine.environment.market_env import MarketEnvironment
from pricing_engine.models.factory import ModelFactory, EngineFactory
from pricing_engine.instruments.option import OptionInstrument


class PricingInterface:
    """
    The main interface class to configure and price an option instrument.

    This class loads the entire environment and pricing stack from configuration:
    - Market data (volatility, curves, etc.)
    - Pricing model (e.g., Black-Scholes, Heston)
    - Engine (e.g., analytic, binomial, etc.)
    - Option instrument (call/put, European/American)
    """

    
    def __init__(self):
        """
        Initialize the pricing interface by loading config and constructing
        all components (market environment, model, engine, and instrument).
        """

        self.cfg: FullConfig = load_config()

        self.expiry_date = ql.DateParser.parseISO(self.cfg.option_instrument.expiry)

        self.market_env = MarketEnvironment.from_config(self.cfg)
        self._model = ModelFactory.create_model(
            self.cfg.pricer.model,
            self.market_env.underlying.spot,
            self.market_env.dividend_curve,
            self.market_env.risk_free_curve,
            self.market_env.vol_surface,
            self.cfg.pricer.heston_params
        )
        self._engine = EngineFactory.create_engine(
            self._model,
            self.cfg.pricer.engine,
            steps=100
        )
        self.option = OptionInstrument(
            self.cfg.option_instrument.option_type,
            self.cfg.option_instrument.strike,
            self.expiry_date,
            self.cfg.option_instrument.style,
            self._engine,
            self.cfg.pricer.bid_ask_spread
        )

    
    def price(self) -> dict:
        """
        Price the configured option instrument.

        Returns:
            dict: A dictionary with mid, bid, and ask prices.
        """

        return self.option.price()
