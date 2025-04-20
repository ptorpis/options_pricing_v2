import QuantLib as ql

from src.utils.config_loader import load_config
from src.environment.market_env import MarketEnvironment
from src.models.factory import ModelFactory, EngineFactory
from src.instruments.option import OptionInstrument


class PricingInterface:
    def __init__(self):
        self.cfg = load_config()

        self.expiry_date = ql.DateParser.parseISO(self.cfg.option_instrument.expiry)

        self._market_env = MarketEnvironment.from_config(self.cfg)
        self._model = ModelFactory.create_model(
            self.cfg.pricer.model,
            self._market_env.underlying.spot,
            self._market_env.dividend_curve,
            self._market_env.risk_free_curve,
            self._market_env.vol_surface,
            self.cfg.pricer.heston_params
        )
        self._engine = EngineFactory.create_engine(
            self._model,
            self.cfg.pricer.engine,
            steps=100
        )
        self._option = OptionInstrument(
            self.cfg.option_instrument.option_type,
            self.cfg.option_instrument.strike,
            self.expiry_date,
            self.cfg.option_instrument.style,
            self._engine,
            self.cfg.pricer.bid_ask_spread
        )

    
    def price(self):
        return self._option.price()
    


if __name__ == "__main__":
    interface = PricingInterface()
    print(interface.price())