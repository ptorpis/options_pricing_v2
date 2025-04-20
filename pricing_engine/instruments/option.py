import QuantLib as ql


class OptionInstrument:
    """
    Represents a vanilla option instrument with pricing capabilities.

    Supports European and American style call and put options,
    with pricing performed via a provided QuantLib pricing engine.
    """


    def __init__(
            self,
            option_type: str,
            strike: float,
            expiry: ql.Date,
            style: str,
            engine: ql.PricingEngine,
            bid_ask_spread: float
        ):
        """
        Initialize an OptionInstrument instance.

        Args:
            option_type (str): The option type ('call' or 'put').
            strike (float): The strike price of the option.
            expiry (ql.Date): The expiration date of the option.
            style (str): The style of the option ('european' or 'american').
            engine (ql.PricingEngine): A QuantLib-compatible pricing engine.
            bid_ask_spread (float): Bid-ask spread to simulate market quotes.
        """
        
        self.option_type = option_type
        self.strike = strike
        self.expiry = expiry
        self.style = style
        self.engine = engine
        self.bid_ask_spread = bid_ask_spread
    

    def _payoff(self) -> ql.Payoff:
        """
        Construct the payoff object for the option.

        Returns:
            ql.Payoff: A QuantLib PlainVanillaPayoff.

        Raises:
            ValueError: If the option type is not recognized.
        """

        if self.option_type == "call":
            return ql.PlainVanillaPayoff(ql.Option.Call, self.strike)
        elif self.option_type == "put":
            return ql.PlainVanillaPayoff(ql.Option.Put, self.strike)
        else:
            raise ValueError(f'Unknown option type: {self.option_type}')
        

    def _exercise(self) -> ql.Exercise:
        """
        Construct the exercise object based on the option style.

        Returns:
            ql.Exercise: A QuantLib EuropeanExercise or AmericanExercise.

        Raises:
            ValueError: If the option style is not recognized.
        """

        if self.style == "european":
            return ql.EuropeanExercise(self.expiry)
        elif self.style == "american":
            today = ql.Settings.instance().evaluationDate
            return ql.AmericanExercise(today, self.expiry)
        else:
            raise ValueError(f"Unknown option style: {self.style}")
        
    
    def _build_option(self) -> ql.VanillaOption:
        """
        Construct the QuantLib VanillaOption object.

        Returns:
            ql.VanillaOption: The constructed option.
        """

        return ql.VanillaOption(self._payoff(), self._exercise())
    

    def price(self) -> dict:
        """
        Price the option using the assigned pricing engine.

        Returns:
            dict: A dictionary with 'mid', 'bid', and 'ask' prices.

        Raises:
            ValueError: If the pricing engine is not set.
        """

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
        """
        Return a human-readable string representation of the option.

        Returns:
            str: Summary of the option's key attributes.
        """

        return (f"OptionInstrument(type={self.option_type}, "
                f"style={self.style}, "
                f"strike={self.strike}, "
                f"expiry={self.expiry}, "
                f"spread={self.bid_ask_spread})")
