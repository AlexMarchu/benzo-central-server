import json
from enum import Enum
from dataclasses import dataclass
from typing import Self, ClassVar

from channels_app.car_number import CarNumber
from channels_app.fuel_type import FuelType
from channels_app.fuel_price_data import FuelPriceData


class MessageType(Enum):
    CONNECT_REQUEST = 'connect_request'
    CONNECTED = 'connected'

    STATION_NOT_TAKEN_REQUEST = 'station_not_taken_request'
    STATION_NOT_TAKEN = 'station_not_taken'
    STATION_TAKEN_OFFLINE_REQUEST = 'station_taken_offline_request'
    STATION_TAKEN_OFFLINE = 'station_taken_offline'
    FUEL_PRICE_DATA_ASK = 'fuel_price_data_ask'
    FUEL_PRICE_DATA_SENT = 'fuel_price_data_sent'
    LOYALTY_CARD_ASK = 'loyalty_card_ask'
    LOYALTY_CARD_SENT = 'loyalty_card_sent'
    PAYMENT_SENT = 'payment_sent'
    PAYMENT_RECEIVED = 'payment_received'


@dataclass
class ConnectRequestMessage:
    message_type: ClassVar[MessageType] = MessageType.CONNECT_REQUEST

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class ConnectedMessage:
    message_type: ClassVar[MessageType] = MessageType.CONNECTED

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class StationNotTakenRequestMessage:
    message_type: ClassVar[MessageType] = MessageType.STATION_NOT_TAKEN_REQUEST

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class StationNotTakenMessage:
    message_type: ClassVar[MessageType] = MessageType.STATION_NOT_TAKEN

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class StationTakenOfflineRequestMessage:
    message_type: ClassVar[MessageType] = MessageType.STATION_TAKEN_OFFLINE_REQUEST

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class StationTakenOfflineMessage:
    message_type: ClassVar[MessageType] = MessageType.STATION_TAKEN_OFFLINE

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class FuelPriceDataAskMessage:
    message_type: ClassVar[MessageType] = MessageType.FUEL_PRICE_DATA_ASK

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class FuelPriceDataSentMessage:
    message_type: ClassVar[MessageType] = MessageType.FUEL_PRICE_DATA_SENT
    fuel_price_data: FuelPriceData

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            price = dict()
            if (data_dict['price'].get(FuelType.FT_92.value) is not None):
                price[FuelType.FT_92] = data_dict['price'][FuelType.FT_92.value]
            if (data_dict['price'].get(FuelType.FT_95.value) is not None):
                price[FuelType.FT_95] = data_dict['price'][FuelType.FT_95.value]
            if (data_dict['price'].get(FuelType.FT_98.value) is not None):
                price[FuelType.FT_98] = data_dict['price'][FuelType.FT_98.value]
            if (data_dict['price'].get(FuelType.FT_DT.value) is not None):
                price[FuelType.FT_DT] = data_dict['price'][FuelType.FT_DT.value]

            return cls(
                fuel_price_data=FuelPriceData(price=price)
            )
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        data_dict = dict()
        data_dict['message_type'] = self.message_type.value
        data_dict['price'] = dict()
        if (self.fuel_price_data.price.get(FuelType.FT_92) is not None):
            data_dict['price'][FuelType.FT_92.value] = self.fuel_price_data.price[FuelType.FT_92]
        if (self.fuel_price_data.price.get(FuelType.FT_95) is not None):
            data_dict['price'][FuelType.FT_95.value] = self.fuel_price_data.price[FuelType.FT_95]
        if (self.fuel_price_data.price.get(FuelType.FT_98) is not None):
            data_dict['price'][FuelType.FT_98.value] = self.fuel_price_data.price[FuelType.FT_98]
        if (self.fuel_price_data.price.get(FuelType.FT_DT) is not None):
            data_dict['price'][FuelType.FT_DT.value] = self.fuel_price_data.price[FuelType.FT_DT]
        return data_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class LoyaltyCardAskMessage:
    message_type: ClassVar[MessageType] = MessageType.LOYALTY_CARD_ASK
    car_number: CarNumber

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls(
                car_number=data_dict['car_number']
            )
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
            'car_number': self.car_number.text,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class LoyaltyCardSentMessage:
    message_type: ClassVar[MessageType] = MessageType.LOYALTY_CARD_SENT
    loyalty_card_available: bool
    loyalty_card_holder: str | None = None
    loyalty_card_bonuses: int | None = None

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls(
                loyalty_card_available=(data_dict['loyalty_card_available'] == 'true'),
                loyalty_card_holder=data_dict.get('loyalty_card_holder'),
                loyalty_card_bonuses=data_dict.get('loyalty_card_bonuses'),
            )
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        data_dict = dict()
        data_dict['message_type'] = self.message_type.value
        data_dict['loyalty_card_available'] = 'true' if self.loyalty_card_available else 'false'
        if (self.loyalty_card_holder is not None):
            data_dict['loyalty_card_holder'] = self.loyalty_card_holder
        if (self.loyalty_card_bonuses is not None):
            data_dict['loyalty_card_bonuses'] = self.loyalty_card_bonuses
        return data_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class PaymentSentMessage:
    message_type: ClassVar[MessageType] = MessageType.PAYMENT_SENT
    fuel_type: FuelType
    fuel_amount: int
    car_number: CarNumber
    payment_amount: int
    payment_key: str
    used_bonuses: int

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls(
                fuel_type=FuelType(data_dict['fuel_type']),
                fuel_amount=data_dict['fuel_amount'],
                car_number=CarNumber(text=data_dict['car_number']),
                payment_amount=data_dict['payment_amount'],
                payment_key=data_dict['payment_key'],
                used_bonuses=data_dict['used_bonuses']
            )
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
            'fuel_type': self.fuel_type.value,
            'fuel_amount': self.fuel_amount,
            'car_number': self.car_number.text,
            'payment_amount': self.payment_amount,
            'payment_key': self.payment_key,
            'used_bonuses': self.used_bonuses,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class PaymentReceivedMessage:
    message_type: ClassVar[MessageType] = MessageType.PAYMENT_RECEIVED

    @classmethod
    def from_dict(cls, data_dict: dict) -> Self:
        if data_dict['message_type'] == cls.message_type.value:
            return cls()
        raise ValueError('message_type is invalid')

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict:
        return {
            'message_type': self.message_type.value,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
