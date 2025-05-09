import json
import os
from pydantic import BaseModel, ValidationError


# === Individual Config Models === #

class MarketEnvConfig(BaseModel):
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


class UnderlyingConfig(BaseModel):
    name: str
    spot: float


class FlatCurveConfig(BaseModel):
    type: str  # currently only supports "flat"
    rate: float


class CurvesConfig(BaseModel):
    risk_free: FlatCurveConfig
    dividend: FlatCurveConfig


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
    engine: str
    steps: int
    bid_ask_spread: float
    model: str
    greek_method: str
    fd_bumps: FDBumps
    heston_params: HestonParams


# === Top-Level Config Model === #

class FullConfig(BaseModel):
    market_env: MarketEnvConfig
    underlying: UnderlyingConfig
    curves: CurvesConfig
    volatility_surfaces: dict[str, VolSurfaceConfig]
    option_instrument: OptionInstrumentConfig
    pricer: PricerConfig


# === Loader Function === #

def load_config(path="config/config.json") -> FullConfig:
    """
    Load and validate a JSON configuration file.

    Args:
        path (str): Path to the configuration file. Defaults to "config/config.json".

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValidationError: If the file contents do not conform to the FullConfig schema.

    Returns:
        FullConfig: A validated configuration object.
    """
    
    if not os.path.exists(path):
        raise FileNotFoundError(f'Config not found at {path}')
    
    with open(path, 'r') as file:
        raw_config = json.load(file)
    
    try:
        config = FullConfig(**raw_config)
    except ValidationError as e:
        print('Config validation failed:')
        print(e.json())
        raise e
    
    return config


# === Debug Entry Point === #

if __name__ == "__main__":
    cfg = load_config()
    print(cfg.model_dump_json(indent=2))
