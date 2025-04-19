import json
import os
from re import L
from textwrap import indent

from pydantic import BaseModel, Field, ValidationError

from src.engine import pricer


class MarketEnvConfig(BaseModel):
    name: str
    pricing_date: str
    volatility_regime: str
    calendar: str
    day_count: str


class VolSurfaceConfig(BaseModel):
    type: str
    vol: float


class OptionInstrumentConfig(BaseModel):
    option_type: str
    strike: float
    expiry: str
    style: str


class FDBumps(BaseModel):
    bump_spot: float
    bump_vol: float
    bump_rate: float
    bump_days: int


class HestonParams(BaseModel):
    v0: float
    kappa: float
    theta: float
    sigma: float
    rho: float


class PricerConfig(BaseModel):
    spot: float
    r: float
    q: float
    engine: str
    steps: int
    bid_ask_spread: float
    model: str
    greek_method: str
    fd_bumps: FDBumps
    heston_params: HestonParams


class FullConfig(BaseModel):
    market_env: MarketEnvConfig
    volatility_surfaces: dict[str, VolSurfaceConfig]
    option_instrument: OptionInstrumentConfig
    pricer: PricerConfig


def load_config(path="config/config.json") -> FullConfig: 
    if not os.path.exists(path):
        raise FileNotFoundError(f'Config not found at {path}')
    
    with open(path, 'r') as file:
        raw_config = json.load(file)
    
    try:
        config = FullConfig(**raw_config)
    except ValidationError as e:
        print('Config Validation failedL')
        print(e.json())
        raise e
    
    return config




if __name__ == "__main__":
    cfg = load_config()
    print(cfg.model_dump_json(indent=2))