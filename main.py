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
        print(f"\n--- Generated Expiry Dates Based on Configured Pricing Date ({interface.market_env.pricing_date}) ---")
        
        for i in range(len(interface.market_env.expiries)):
            print(interface.market_env.expiries[i])