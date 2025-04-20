import QuantLib as ql


class Conventions():
    """
    Encapsulates financial market conventions such as calendar and day count
    used for constructing QuantLib objects.

    Attributes:
        calendar_name (str): The name of the financial calendar to use.
        day_count (str): The name of the day count convention to use.
    """


    def __init__(self, calendar_name: str, day_count: str):
        """
        Initialize the Conventions object with a calendar and day count.

        Args:
            calendar_name (str): Name of the financial calendar.
            day_count (str): Name of the day count convention.
        """

        self.calendar_name: str = calendar_name
        self.day_count: str = day_count


    def build(self) -> tuple[ql.Calendar, ql.DayCounter]:
        """
        Build the QuantLib calendar and day count convention objects.

        Returns:
        tuple[ql.Calendar, ql.DayCounter]: A tuple containing the calendar and day count convention.
        """

        calendar = self.get_calendar(self.calendar_name)
        dc = self.get_day_count(self.day_count)
        return calendar, dc
    

    @staticmethod
    def get_calendar(name: str) -> ql.Calendar:
        """
        Map a calendar name string to a QuantLib calendar object.

        Args:
            name (str): The calendar name.

        Returns:
            ql.Calendar: Corresponding QuantLib calendar.

        Raises:
            ValueError: If the calendar name is not supported.
        """

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
        """
        Get a QuantLib day count convention object by name.

        Args:
            name (str): The name of the day count convention.

        Returns:
            ql.DayCounter: Corresponding QuantLib day counter.

        Raises:
            ValueError: If the day count name is not valid.
        """

        try:
            return getattr(ql, name)()
        except AttributeError:
            raise ValueError(f"Unsupported day count convention: {name}")


    @staticmethod
    def from_config(cfg) -> "Conventions":
        """
        Create a Conventions object from a configuration object.

        Args:
            cfg: A configuration object with `calendar` and `day_count` attributes.

        Returns:
            Conventions: An instance of the Conventions class.
        """
        
        return Conventions(
            calendar_name=cfg.calendar,
            day_count=cfg.day_count
        )
