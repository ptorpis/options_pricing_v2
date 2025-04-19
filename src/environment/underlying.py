from dataclasses import dataclass

from src.utils.config_loader import load_config

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
    

if __name__ == "__main__":
    cfg = load_config()

    underlying = Underlying.from_config(cfg.underlying)
    print(underlying)