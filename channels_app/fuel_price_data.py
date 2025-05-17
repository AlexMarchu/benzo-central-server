from dataclasses import dataclass


@dataclass
class FuelPriceData:
    price: dict[str, int]
