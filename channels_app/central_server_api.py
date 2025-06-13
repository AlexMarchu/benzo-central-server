import json
from enum import Enum
from dataclasses import dataclass
from typing import Self, ClassVar

from channels_app.car_number import CarNumber
from channels_app.fuel_price_data import FuelPriceData

from stations.models import FuelType


class MessageType(Enum):
    CONNECT = 'connect'
    CONNECTED = 'connected'
    SERVICE_READY = 'service_ready'
    SERVICE_NOT_READY = 'service_not_ready'
    SERVICE_STARTED = 'service_started'
    SERVICE_ENDED = 'service_ended'
    FUEL_PRICE_DATA_ASK = 'fuel_price_data_ask'
    FUEL_PRICE_DATA_SENT = 'fuel_price_data_sent'
    LOYALTY_CARD_ASK = 'loyalty_card_ask'
    LOYALTY_CARD_SENT = 'loyalty_card_sent'
    SAVE_PAYMENT = 'save_payment'

    MOBILE_APP_CONNECT = 'mobile_app_connect'
    MOBILE_APP_CONNECTED = 'mobile_app_connected'
    MOBILE_APP_SERVICE_ENDED = 'mobile_app_service_ended'
    MOBILE_APP_USED_T1 = 'mobile_app_used_t1'
    MOBILE_APP_SAVE_PAYMENT = 'mobile_app_save_payment'
    GAS_NOZZLE_USED_T2 = 'gas_nozzle_used_t2'
    MOBILE_APP_USED_T2 = 'mobile_app_used_t2'


@dataclass
class ConnectMessage:
    message_type: ClassVar[MessageType] = MessageType.CONNECT

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
class ServiceReadyMessage:
    message_type: ClassVar[MessageType] = MessageType.SERVICE_READY

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
class ServiceNotReadyMessage:
    message_type: ClassVar[MessageType] = MessageType.SERVICE_NOT_READY

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
class ServiceStartedMessage:
    message_type: ClassVar[MessageType] = MessageType.SERVICE_STARTED

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
class ServiceEndedMessage:
    message_type: ClassVar[MessageType] = MessageType.SERVICE_ENDED

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
            if data_dict['price'].get(FuelType.PETROL_92) is not None:
                price[FuelType.PETROL_92] = data_dict['price'][FuelType.PETROL_92]
            if data_dict['price'].get(FuelType.PETROL_95) is not None:
                price[FuelType.PETROL_95] = data_dict['price'][FuelType.PETROL_95]
            if data_dict['price'].get(FuelType.PETROL_98) is not None:
                price[FuelType.PETROL_98] = data_dict['price'][FuelType.PETROL_98]
            if data_dict['price'].get(FuelType.DIESEL) is not None:
                price[FuelType.DIESEL] = data_dict['price'][FuelType.DIESEL]

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
        if self.fuel_price_data.price.get(FuelType.PETROL_92) is not None:
            data_dict['price'][FuelType.PETROL_92] = self.fuel_price_data.price[FuelType.PETROL_92]
        if self.fuel_price_data.price.get(FuelType.PETROL_95) is not None:
            data_dict['price'][FuelType.PETROL_95] = self.fuel_price_data.price[FuelType.PETROL_95]
        if self.fuel_price_data.price.get(FuelType.PETROL_98) is not None:
            data_dict['price'][FuelType.PETROL_98] = self.fuel_price_data.price[FuelType.PETROL_98]
        if self.fuel_price_data.price.get(FuelType.DIESEL) is not None:
            data_dict['price'][FuelType.DIESEL] = self.fuel_price_data.price[FuelType.DIESEL]
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
                car_number=CarNumber(text=data_dict['car_number'])
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
class SavePaymentMessage:
    message_type: ClassVar[MessageType] = MessageType.SAVE_PAYMENT
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


# mobile app


@dataclass
class MobileAppConnectMessage:
    message_type: ClassVar[MessageType] = MessageType.MOBILE_APP_CONNECT

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
class MobileAppConnectedMessage:
    message_type: ClassVar[MessageType] = MessageType.MOBILE_APP_CONNECTED

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
class MobileAppServiceEndedMessage:
    message_type: ClassVar[MessageType] = MessageType.MOBILE_APP_SERVICE_ENDED

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
class MobileAppUsedT1Message:
    message_type: ClassVar[MessageType] = MessageType.MOBILE_APP_USED_T1

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
class MobileAppSavePaymentMessage:
    message_type: ClassVar[MessageType] = MessageType.MOBILE_APP_SAVE_PAYMENT
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
class GasNozzleUsedT2Message:
    message_type: ClassVar[MessageType] = MessageType.GAS_NOZZLE_USED_T2

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
class MobileAppUsedT2Message:
    message_type: ClassVar[MessageType] = MessageType.MOBILE_APP_USED_T2

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