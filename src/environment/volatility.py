from abc import ABC, abstractmethod

import QuantLib as ql


class VolatilitySurface(ABC):
    @abstractmethod
    def build(
        self,
        pricing_date: ql.Date,
        calendar: ql.Calendar,
        day_count: ql.DayCounter
    ) -> ql.BlackVolTermStructure:
        
        """
        Build the QuantLib BlackVolTermStructure object.
        Must be implemented by subclasses.
        """
        pass


class FlatVolSurface(VolatilitySurface):
    def __init__(self, vol: float):
        super().__init__()
        self.vol = vol

    
    def build(
        self,
        pricing_date: ql.Date,
        calendar: ql.Calendar,
        day_count: ql.DayCounter
    ):
        return ql.BlackConstantVol(pricing_date, calendar, self.vol, day_count)
    

class VolatilitySurfaceFactory:
    @staticmethod
    def from_config(vol_config: dict) -> VolatilitySurface:
        if isinstance(vol_config, dict):
            surface_type = vol_config.get("type")
            vol = vol_config.get("vol")
        else:  # Assume Pydantic model
            surface_type = vol_config.type
            vol = vol_config.vol

        if surface_type == "flat":
            return FlatVolSurface(vol=vol)

        # Placeholder for future support
        elif surface_type == "term_structure":
            raise NotImplementedError("Term structure vol is not implemented yet.")

        else:
            raise ValueError(f"Unknown vol surface type: {surface_type}")

