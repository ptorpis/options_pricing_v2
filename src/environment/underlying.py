from dataclasses import dataclass


@dataclass
class Underlying:
    name: str
    spot: float


    @staticmethod
    def from_config(cfg) -> "Underlying":
        return Underlying(
            name=cfg.name,
            spot=cfg.spot,
        )
