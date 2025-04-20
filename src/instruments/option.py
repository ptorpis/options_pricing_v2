import QuantLib as ql


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
    

    def _payoff(self) -> ql.Payoff:
        if self.option_type == "call":
            return ql.PlainVanillaPayoff(ql.Option.Call, self.strike)
        elif self.option_type == "put":
            return ql.PlainVanillaPayoff(ql.Option.Put, self.strike)
        else:
            raise ValueError(f'Unknown option type: {self.option_type}')
        

    def _exercise(self) -> ql.Exercise:
        if self.style == "european":
            return ql.EuropeanExercise(self.expiry)
        elif self.style == "american":
            today = ql.Settings.instance().evaluationDate
            return ql.AmericanExercise(today, self.expiry)
        else:
            raise ValueError(f"Unknown option style: {self.style}")
        
    
    def _build_option(self) -> ql.VanillaOption:
        return ql.VanillaOption(self._payoff(), self._exercise())
    

    def price(self) -> dict:
        option = self._build_option()

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
    
    
    def __repr__(self):
        return (f"OptionInstrument(type={self.option_type}, "
                f"style={self.style}, "
                f"strike={self.strike}, "
                f"expiry={self.expiry}, "
                f"spread={self.bid_ask_spread})")

   