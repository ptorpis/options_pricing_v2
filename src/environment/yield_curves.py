import QuantLib as ql


class YieldCurveBuilder:
    """
    A builder class for constructing risk-free and dividend yield curves.

    This class provides methods to build yield curves using configuration
    parameters for both risk-free and dividend rates. It uses QuantLib to
    build the respective `YieldTermStructure` objects.

    Attributes:
        curves_config (dict or object): The configuration containing the risk-free and dividend rates.
        pricing_date (ql.Date): The date at which the yield curves are to be evaluated.
        calendar (ql.Calendar): The calendar used for date adjustments.
        day_count (ql.DayCounter): The day count convention used for the curves.

    Methods:
        build_risk_free_curve(): 
            Builds and returns the risk-free yield curve.
        
        build_dividend_curve():
            Builds and returns the dividend yield curve.

        build_all():
            Builds and returns both the risk-free and dividend yield curves.
    """


    def __init__(
            self,
            curves_config,
            pricing_date: ql.Date,
            calendar: ql.Calendar,
            day_count: ql.DayCounter
        ):
        """
        Initialize the YieldCurveBuilder with configuration and market data.

        Args:
            curves_config (dict or object): Configuration containing the risk-free and dividend curve parameters.
            pricing_date (ql.Date): The date at which the curves are to be evaluated.
            calendar (ql.Calendar): The calendar used for date adjustments.
            day_count (ql.DayCounter): The day count convention used for the curves.
        """

        self.curves_config = curves_config
        self.pricing_date = pricing_date
        self.calendar = calendar
        self.day_count = day_count

    
    def build_risk_free_curve(self) -> ql.YieldTermStructure:
        """
        Build and return the risk-free yield curve.

        This method creates a flat forward curve with the risk-free rate from
        the configuration using QuantLib's `FlatForward` class.

        Returns:
            ql.YieldTermStructure: The risk-free yield curve.
        """

        rate = self.curves_config.risk_free.rate
        return ql.FlatForward(self.pricing_date, rate, self.day_count)
    

    def build_dividend_curve(self) -> ql.YieldTermStructure:
        """
        Build and return the dividend yield curve.

        This method creates a flat forward curve with the dividend rate from
        the configuration using QuantLib's `FlatForward` class.

        Returns:
            ql.YieldTermStructure: The dividend yield curve.
        """

        rate = self.curves_config.dividend.rate
        return ql.FlatForward(self.pricing_date, rate, self.day_count)


    def build_all(self) -> tuple:
        """
        Build and return both the risk-free and dividend yield curves.

        This method calls `build_risk_free_curve()` and `build_dividend_curve()` 
        to return both curves as a tuple.

        Returns:
            tuple: A tuple containing the risk-free and dividend yield curves.
        """
        
        risk_free_curve = self.build_risk_free_curve()
        dividend_curve = self.build_dividend_curve()

        return risk_free_curve, dividend_curve
    
