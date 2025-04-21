# OPTIONS PRICING ENGINE 
Options Pricing Engine based on QuantLib.
# Dependencies
To install dependencies (QuantLib and pydantic), run:
```bash
pip install -r requirements.txt
```
# Usage

Set up the config by running `setup.py`:

```bash
python setup_cfg.py
```

To reset config:
```bash
python setup_cfg.py --reset
```
Then, configure the market and contract parameters in `config/config,json`

To get the price of the options contract:
```bash
python main.py
```

Get a summary of the contract and the market environment, use `--summary`:
```bash
python main.py --summary
```
# Architecture
The goal for this project is to create a nuanced and configurable options pricing engine with the ability to set up the underlying market environment with different volatility term structures and yield curves.

This gives the user the ability to run a lot of different simulations based on their assumptions.

## Interface

### `PricingInterface` class:

The main interface class to configure and price an option instrument.

This class loads the entire environment and pricing stack from configuration:
- Market data (volatility, curves, etc.) (public: `interface.market_env`)
- Option instrument (call/put, European/American) (public: `interface.option`)
- Pricing model (e.g., Black-Scholes, Heston)
- Engine (e.g., analytic, binomial, etc.)

## Engines
### `PricingEngine` class:

Abstract base class for pricing engines.

This class defines the interface for building QuantLib-compatible pricing engines. Subclasses must implement the `build` method to return a specific engine instance.

Attributes:
- `model_process`: The QuantLib pricing model or process used for option pricing.

---

### `BinomialEngine(PricingEngine)` class:

Binomial tree pricing engine for vanilla options.

This engine uses the Cox-Ross-Rubinstein (CRR) binomial method for pricing.

Attributes: 
- steps (`int`): Number of binomial steps used in the tree.

Can be used with BSM model, for Heston model, use Heston engine.

Retruns: `ql.BinomialVanillaEngine`, the configured binomial pricing engine.

---

### `AnalyticEuropeanEngine(PricingEngine)` class:
Analytic pricing engine for European options using the Black-Scholes model.

Returns:
`ql.AnalyticEuropeanEngine`: The analytic engine based on the Black-Scholes model.

---

### `HestonEngine(PricingEngine)` class:

Pricing engine for options under the Heston stochastic volatility model.

Returns:
`ql.AnalyticHestonEngine`: The engine based on the analytic Heston model.

## Market Environment

### `MarketEnvironment` class:

A class that encapsulates all market-related data required for option pricing.

This class holds all the necessary market data such as pricing date, calendar,
day count convention, underlying asset, volatility surface, risk-free curve,
and dividend curve. It also provides a method to build these data structures
from a configuration.

Attributes:
- pricing_date (`ql.Date`): The pricing date used for building curves and volatilities.
- calendar (`ql.Calendar`): The calendar used for date adjustments.
- day_count (`ql.DayCounter`): The day count convention used for interest rate calculations.
- underlying (`Underlying`): An object representing the underlying asset (e.g., stock).
- vol_surface (`ql.BlackVolTermStructure`): The volatility surface used in option pricing.
- risk_free_curve (`ql.YieldTermStructure`): The risk-free yield curve.
- dividend_curve (`ql.YieldTermStructure`): The dividend yield curve.
- expiries (`list[ql.Date]`): list of generated, realistic options contract expiries.

Methods:
- `from_config(cfg: FullConfig)`: 
Creates a MarketEnvironment instance from the provided configuration. This class method reads the configuration and constructs the market environment by initializing the necessary data structures like the volatility surface, risk-free curve, and dividend curve based on the configuration.
Args:
cfg (pydantic config object): The configuration dictionary containing market parameters.


Returns:
`MarketEnvironment`: An instance of the MarketEnvironment class.

At initialization private method `_generate_expiries()` gets called, which generates a list of expiry dates. By default 4 weeklies, 6 months of monthlies and a YTD expiry one.

This can be used as points where IV term structure is defined (not implemented yet).

- `__repr__()`: 
Returns a string representation of the MarketEnvironment object, including key market details.

---

### `Conventions` class:

Encapsulates financial market conventions such as calendar and day count used for constructing QuantLib objects.

Attributes:
- calendar_name (`str`): The name of the financial calendar to use.
- day_count (`str`): The name of the day count convention to use.

```python
conventions = Conventions.from_config(cfg.market_env)
calendar, day_count = conventions.build()
```

Use the `from_config` method to get the strings stored in the config object then build witht the `build` method.
At the end, you get: `tuple[ql.Calendar, ql.DayCounter]`, containing the calendar and day count convention.

Possible calendars accepted as of now:
- "UnitedStates/NYSE" -> `ql.UnitedStates(ql.UnitedStates.NYSE)`
- "UnitedStates/GovernmentBond" -> `ql.UnitedStates(ql.UnitedStates.GovernmentBond)`
- "TARGET" (European market calendar) -> `ql.TARGET()`
- "UK" -> `ql.UnitedKingdom(ql.UnitedKingdom.Exchange)`

See also: <https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#calendar>.

Day counts: <https://sources.debian.org/data/main/q/quantlib-refman-html/1.20-1/html/group__daycounters.html#:~:text=The%20class%20QuantLib%3A%3ADayCounter%20provides%20more%20advanced%20means%20of,such%20conventions%20is%20contained%20in%20the%20ql%2FDayCounters%20directory.>

---

### `Underlying` class:

Represents an underlying asset in a financial model.

Attributes:
- name (`str`): The name of the underlying asset.
- spot (`float`): The current spot price of the underlying asset.

```python
underlying = Underlying.from_config(cfg.underlying)
```

---

### `VolatilitySurface(ABC)` class:
Abstract base class for volatility surfaces.

This class defines the structure for building volatility surfaces that can be used in option pricing models. Subclasses must implement the `build` method to return a specific `QuantLib` volatility term structure.

Methods:
- `build(pricing_date, calendar, day_count)`: Abstract method that must be implemented by subclasses to build the corresponding volatility structure.

---

### `VolatilitySurfaceFactory` class: 

Factory class to create volatility surface objects from configuration.

This class is responsible for constructing appropriate volatility surface objects
based on a configuration dictionary or object.

Methods:
- `from_config(vol_config)`: Creates a volatility surface object based on the provided configuration.

The config should include the following fields:
- "type": The type of volatility surface ("flat" or "term_structure").
- "vol": The volatility value (required for "flat" type).

Returns:
- `VolatilitySurface`: An instance of the appropriate volatility surface class. `ql.BlackConstantVol` is under the hood for flat surfaces.

Raises:
- `ValueError`: If the surface type is unknown or unsupported.
- `NotImplementedError`: If a "term_structure" volatility surface type is encountered. To be implemented in future versions.

```python
vol_regime = cfg.market_env.volatility_regime
vol_config = cfg.volatility_surfaces[vol_regime]

vol_surface = VolatilitySurfaceFactory.from_config(vol_config).build(
    pricing_date=pricing_date,
    calendar=calendar,
    day_count=day_count
)
```

---

### `YieldCurveBuilder` class:
A builder class for constructing risk-free and dividend yield curves.

This class provides methods to build yield curves using configuration
parameters for both risk-free and dividend rates. It uses QuantLib to
build the respective `YieldTermStructure` objects.

Attributes:
- curves_config (`dict` or object): The configuration containing the risk-free and dividend rates.
- pricing_date (`ql.Date`): The date at which the yield curves are to be evaluated.
- calendar (`ql.Calendar`): The calendar used for date adjustments.
- day_count (`ql.DayCounter`): The day count convention used for the curves.

Methods:
- `build_risk_free_curve()`: Builds and returns the risk-free yield curve.
- `build_dividend_curve()`: Builds and returns the dividend yield curve.
- `build_all()`: Builds and returns both the risk-free and dividend yield curves.

```python
curve_builder = YieldCurveBuilder(cfg.curves, pricing_date, calendar, day_count)
risk_free_curve, dividend_curve = curve_builder.build_all()
```

---

## Instruments

### `OptionInstrument` class:

Represents a vanilla option instrument with pricing capabilities.
Supports European and American style call and put options,
with pricing performed via a provided QuantLib pricing engine.

Attributes:
- option_type (`str`): The option type ('call' or 'put').
- strike (`float`): The strike price of the option.
- expiry (`ql.Date`): The expiration date of the option.
- style (`str`): The style of the option ('european' or 'american').
- engine (`ql.PricingEngine`): A QuantLib-compatible pricing engine.
- bid_ask_spread (`float`): Bid-ask spread to simulate market quotes.

Public methods:
- `price(self)`:
Price the option using the assigned pricing engine.

Returns:
`dict`: A dictionary with 'mid', 'bid', and 'ask' prices.

Raises:
`ValueError`: If the pricing engine is not set.

- `__repr__()`: Prints out a string representation of the option instrument.

## Models
Abstract model is defined in `models/base.py`, with one abstract method, which is `build()`.
### `BlackScholesModel(AbstractModel)` class:

Black-Scholes-Merton model implementation for option pricing.

This class wraps the construction of a QuantLib Black-Scholes-Merton process
using the provided market inputs.

Attributes:
- spot (`float`): Current spot price of the underlying asset.
- dividend_curve (`ql.YieldTermStructure`): Term structure of dividends.
- risk_free_curve (`ql.YieldTermStructure`): Risk-free interest rate curve.
- vol_surface (`ql.BlackVolTermStructure`): Volatility surface.

Build method returns: `ql.BlackScholesMertonProcess`.

---

### `HestonModel(AbstractModel)` class:

Heston stochastic volatility model for option pricing.

This class encapsulates the setup of the Heston model in QuantLib using 
configuration parameters for volatility dynamics.

Attributes:
- spot (`float`): Current spot price of the underlying asset.
- risk_free_curve (`ql.YieldTermStructure`): Risk-free interest rate curve.
- dividend_curve (`ql.YieldTermStructure`): Term structure of dividends.
- params: Configuration object `Fullconfig.pricer.heston_params` containing Heston model parameters:
    - v0: Initial variance
    - kappa: Mean reversion speed
    - theta: Long-term variance
    - sigma: Volatility of variance (vol-of-vol)
    - rho: Correlation between asset and volatility

--- 

### `ModelFactory` class:

Factory for creating model instances for pricing options. Provides a static method to instantiate either a Black-Scholes or Heston model based on configuration and market data.

Create an instance of a pricing model based on the specified type.

method: `create_model()`:
Args:
- model_type (`str`): Type of model ('bsm' or 'heston').
- spot (`float`): Current spot price of the underlying asset.
- dividend_curve (`ql.YieldTermStructure`): Dividend yield curve.
- risk_free_curve (`ql.YieldTermStructure`): Risk-free yield curve.
- vol_surface: Black volatility surface for Black-Scholes model.
- heston_params: Heston model parameters from configuration.

Returns: BlackScholesModel or HestonModel: Instantiated model object.

Raises: `ValueError`: If an unknown model type is provided.

--- 

### `EngineFactory` class:
Factory for creating QuantLib-compatible pricing engines. Provides a static method to build a pricing engine for a given model and selected numerical method (e.g., analytic, binomial, Heston).

method: create_engine():
Args:
- model: A Black-Scholes or Heston model instance.
- engine_type (`str`): Type of engine ('binomial', 'analytic', 'heston').
- steps (`int` - *optional*): Number of steps for binomial tree engines.


## Utils

### `config_loader.py`

```python
cfg = load_config()
```

Load and validate a JSON configuration file.

Args:
path (`str` - *optional*): Path to the configuration file. Defaults to `config/config.json`.

Raises:
`FileNotFoundError`: If the configuration file does not exist.
`ValidationError`: If the file contents do not conform to the FullConfig schema.

Returns:
`FullConfig`: A validated configuration object from pydantic