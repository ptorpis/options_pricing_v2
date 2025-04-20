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
python setup.py
```

To reset config:
```bash
python setup.py --reset
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
# Architecture (documentation to be added)
The goal for this project is to create a nuanced and configurable options pricing engine with the ability to set up the underlying market environment with different volatility term structures and yield curves.

This gives the user the ability to run a lot of different simulations based on their assumptions.

