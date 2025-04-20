import sys
from pricing_engine.api.pricing_interface import PricingInterface

if __name__ == "__main__":
    interface = PricingInterface()
    result = interface.price()
    print("Contract Price:", result)

    if "--summary" in sys.argv:
        print("\n--- Market Environment Summary ---")
        print(interface.market_env)
        print("\n--- Option Instrument Summary ---")
        print(interface.option)
