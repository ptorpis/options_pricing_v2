import QuantLib as ql

from src.utils.config_loader import load_config

from src.environment.conventions import Conventions

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
    

if __name__ == "__main__":

    cfg = load_config()

    pricing_date = ql.DateParser.parseISO(cfg.market_env.pricing_date)
    calendar, day_count = Conventions.from_config(cfg.market_env).build()

    curves_builder = YieldCurveBuilder(cfg.curves, pricing_date, calendar, day_count)

    risk_free_curve, dividend_curve = curves_builder.build_all()

    print(f"Risk-Free Curve: {risk_free_curve}")
    print(f"Dividend Yield Curve: {dividend_curve}")
