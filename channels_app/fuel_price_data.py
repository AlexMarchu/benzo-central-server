from dataclasses import dataclass

from channels_app.fuel_type import FuelType


@dataclass
class FuelPriceData:
    price: dict[FuelType, int]
