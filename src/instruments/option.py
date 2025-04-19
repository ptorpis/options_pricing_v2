import QuantLib as ql

from src.utils.config_loader import load_config


class OptionInstrument:
    def __init__(
            self,
            option_type: str,
            strike: float,
            expiry: ql.Date,
            style: str
        ):
        
        self.option_type = option_type
        self.strike = strike
        self.expiry = expiry
        self.style = style


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
    

if __name__ == "__main__":
    cfg = load_config()
    ql.Settings.instance().evaluationDate = ql.DateParser.parseISO(cfg.market_env.pricing_date)

    option_cfg = cfg.option_instrument
    option = OptionInstrument.from_config(option_cfg)
    ql_option = option.build_option()

    print(ql_option)