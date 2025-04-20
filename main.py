from src.api.pricing_interface import PricingInterface


if __name__ == "__main__":
    interface = PricingInterface()
    result = interface.price()
    print("Pricing result:", result)
