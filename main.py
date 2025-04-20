from src.api.pricing_interface import PricingInterface


if __name__ == "__main__":
    interface = PricingInterface()
    result = interface.price()
    print("Contract Price:", result)
    env = interface.market_env
    option = interface.option
    print(env)
    print(option)
