import QuantLib as ql

from src.utils.config_loader import load_config, FullConfig
from src.environment.market_env import MarketEnvironment
from src.models.factory import ModelFactory, EngineFactory
from src.instruments.option import OptionInstrument


class PricingInterface:
    def __init__(self):
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

    
    def price(self):
        return self.option.price()
