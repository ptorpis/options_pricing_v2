import QuantLib as ql


class YieldCurveBuilder:
    def __init__(
            self,
            curves_config,
            pricing_date: ql.Date,
            calendar: ql.Calendar,
            day_count: ql.DayCounter
        ):

        self.curves_config = curves_config
        self.pricing_date = pricing_date
        self.calendar = calendar
        self.day_count = day_count

    
    def build_risk_free_curve(self) -> ql.YieldTermStructure:
        rate = self.curves_config.risk_free.rate
        return ql.FlatForward(self.pricing_date, rate, self.day_count)
    

    def build_dividend_curve(self) -> ql.YieldTermStructure:
        rate = self.curves_config.dividend.rate
        return ql.FlatForward(self.pricing_date, rate, self.day_count)


    def build_all(self) -> tuple:
        risk_free_curve = self.build_risk_free_curve()
        dividend_curve = self.build_dividend_curve()

        return risk_free_curve, dividend_curve
    
