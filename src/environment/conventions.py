import QuantLib as ql
from src.utils.config_loader import load_config

class Conventions():
    def __init__(self, calendar_name: str, day_count: str):
        self.calendar_name: str = calendar_name
        self.day_count: str = day_count


    def build(self):
        calendar = self.get_calendar(self.calendar_name)
        dc = self.get_day_count(self.day_count)
        return calendar, dc
    

    @staticmethod
    def get_calendar(name: str) -> ql.Calendar:
        calendar_map = {
            "UnitedStates/NYSE": lambda: ql.UnitedStates(ql.UnitedStates.NYSE),
            "UnitedStates/GovernmentBond": lambda: ql.UnitedStates(ql.UnitedStates.GovernmentBond),
            "TARGET": lambda: ql.TARGET(),
            "UK": lambda: ql.UnitedKingdom(ql.UnitedKingdom.Exchange)            
        }

        try:
            return calendar_map[name]()
        except KeyError:
            raise ValueError(f"Unsupported calendar: {name}")


    @staticmethod
    def get_day_count(name: str) -> ql.DayCounter:
        try:
            return getattr(ql, name)()
        except AttributeError:
            raise ValueError(f"Unsupported day count convention: {name}")


    @staticmethod
    def from_config(cfg) -> "Conventions":
        return Conventions(
            calendar_name=cfg.calendar,
            day_count=cfg.day_count
        )
    

if __name__ == "__main__":
    cfg = load_config()

    conventions = Conventions.from_config(cfg.market_env)
    calendar, dc = conventions.build()

    print(calendar, dc)