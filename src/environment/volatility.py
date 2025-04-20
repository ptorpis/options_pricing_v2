from abc import ABC, abstractmethod

import QuantLib as ql


class VolatilitySurface(ABC):
    """
    Abstract base class for volatility surfaces.

    This class defines the structure for building volatility surfaces that can be
    used in option pricing models. Subclasses must implement the `build` method to
    return a specific `QuantLib` volatility term structure.

    Methods:
        build(pricing_date, calendar, day_count): 
            Abstract method that must be implemented by subclasses to build
            the corresponding volatility structure.
    """

    @abstractmethod
    def build(
        self,
        pricing_date: ql.Date,
        calendar: ql.Calendar,
        day_count: ql.DayCounter
    ) -> ql.BlackVolTermStructure:
        
        """
        Build the QuantLib BlackVolTermStructure object.

        Args:
            pricing_date (ql.Date): The date at which the volatility surface is to be evaluated.
            calendar (ql.Calendar): The calendar used to adjust dates.
            day_count (ql.DayCounter): The day count convention used.

        Returns:
            ql.BlackVolTermStructure: The built volatility term structure.

        Notes:
            This method must be implemented by subclasses.
        """
        pass


class FlatVolSurface(VolatilitySurface):
    """
    A flat volatility surface with a constant volatility value.

    This class implements the `VolatilitySurface` interface to provide a simple,
    flat volatility structure that can be used in models requiring constant volatility.

    Attributes:
        vol (float): The constant volatility used for the surface.

    Methods:
        build(pricing_date, calendar, day_count): 
            Returns a `BlackConstantVol` object with the constant volatility.
    """


    def __init__(self, vol: float):
        """
        Initialize the FlatVolSurface with a constant volatility value.

        Args:
            vol (float): The constant volatility to be used for the surface.
        """

        super().__init__()
        self.vol = vol

    
    def build(
        self,
        pricing_date: ql.Date,
        calendar: ql.Calendar,
        day_count: ql.DayCounter
    ):
        """
        Build a constant volatility term structure.

        Args:
            pricing_date (ql.Date): The date at which the volatility surface is to be evaluated.
            calendar (ql.Calendar): The calendar used to adjust dates.
            day_count (ql.DayCounter): The day count convention used.

        Returns:
            ql.BlackConstantVol: A constant volatility term structure with the given volatility.
        """

        return ql.BlackConstantVol(pricing_date, calendar, self.vol, day_count)
    

class VolatilitySurfaceFactory:
    """
    Factory class to create volatility surface objects from configuration.

    This class is responsible for constructing appropriate volatility surface objects
    based on a configuration dictionary or object.

    Methods:
        `from_config(vol_config)`: 
            Creates a volatility surface object based on the provided configuration.
    """


    @staticmethod
    def from_config(vol_config: dict) -> VolatilitySurface:
        """
        Create a volatility surface object based on the provided configuration.

        Args:
            vol_config (dict or object): The configuration that defines the volatility surface.
            
            It should include the following fields:
                - "type": The type of volatility surface ("flat" or "term_structure").
                - "vol": The volatility value (required for "flat" type).

        Returns:
            VolatilitySurface: An instance of the appropriate volatility surface class.

        Raises:
            ValueError: If the surface type is unknown or unsupported.
            NotImplementedError: If a "term_structure" volatility surface type is encountered.
        """

        if isinstance(vol_config, dict):
            surface_type = vol_config.get("type")
            vol = vol_config.get("vol")
        else:  # Pydantic model
            surface_type = vol_config.type
            vol = vol_config.vol

        if surface_type == "flat":
            return FlatVolSurface(vol=vol)

        # Placeholder for future support
        elif surface_type == "term_structure":
            raise NotImplementedError("Term structure vol is not implemented yet.")

        else:
            raise ValueError(f"Unknown vol surface type: {surface_type}")

