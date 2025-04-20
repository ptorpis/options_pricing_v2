from dataclasses import dataclass


@dataclass
class Underlying:
    """
    Represents an underlying asset in a financial model.

    Attributes:
        name (str): The name of the underlying asset.
        spot (float): The current spot price of the underlying asset.
    """

    name: str
    spot: float


    @staticmethod
    def from_config(cfg) -> "Underlying":
        """
        Create an Underlying instance from a configuration object.

        Args:
            cfg: A configuration object containing the `name` and `spot` attributes.

        Returns:
            Underlying: An instance of the Underlying class.
        """
        
        return Underlying(
            name=cfg.name,
            spot=cfg.spot,
        )
