# OPTIONS PRICING ENGINE 
Options Pricing Engine based on QuantLib with an API.

# Architecture
The goal for this project is to create a nuanced and configurable options pricing engine with the ability to set up the underlying market environment with different volatility term structures and yield curves.

This gives the user the ability to run a lot of different simulations based on their assumptions.
# High Level Wrappers
## `MarketEnvironment`
This class ties all of the underlying market factors into one and builds the environment.
This includes spot (underlying) price, forward price, dividend yield, risk-free and dividend yield term structure, volatility surfaces, calendar and market conventions.

### `UnderlyingMarket`
Manage spot price, forward price, dividend yield
### `YieldCurveBuilder`
Constructs risk-free and dividend yield term strucutures.
### `VolatilitySurface`
Build flat, smile, or full volatility surface.
### `MarketConventions`
Wraps up the market calendar, settlement, day count and business day conventions.
## `OptionInstrument`
Describes the option contract - type, exercise style, strike, expiration.

## `OptionPricer`
Uses the environment and instrument to build a process and price the contract.

## `PricingAPI`
High-level interface for loading config and calling pricing methods.
