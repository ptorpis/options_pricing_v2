from abc import ABC, abstractmethod

import QuantLib as ql

from src.environment.conventions import Conventions
from src.utils.config_loader import load_config


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

    
    def build(self, pricing_date, calendar, day_count):
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


if __name__ == "__main__":
    cfg = load_config()

    pricig_date = ql.DateParser.parseISO(cfg.market_env.pricing_date)

    conv = Conventions.from_config(cfg.market_env)
    calendar, day_count = conv.build()

    vol_regime = cfg.market_env.volatility_regime
    vol_surface_config = cfg.volatility_surfaces[vol_regime]

    vol_surface = VolatilitySurfaceFactory.from_config(vol_surface_config)

    ql_vol = vol_surface.build(
        pricing_date=pricig_date,
        calendar=calendar,
        day_count=day_count
    )

    print(f"QL Volatility Surface: {ql_vol}")
    print(f"Vol at T=1, K=100: {ql_vol.blackVol(1.0, 100)}")
