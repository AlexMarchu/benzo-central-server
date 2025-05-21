import json
from bidict import bidict

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from channels_app.central_server_ws_api import *
from stations.models import Station, StationStatus, FuelType, GasStationLog, PaymentMethod
from users.models import User, LoyaltyCard


class ServerConsumer(AsyncWebsocketConsumer):
    groups = ['all']
    station = bidict()  # channel_name <-> station_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(f'all', self.channel_name)
        print(f'CENTRAL SERVER | client {self.channel_name} connected')

    async def disconnect(self, code):
        channel_name = self.channel_name
        station_id = self.scope['url_route']['kwargs']['station_id']
        room_name = await self.get_room_name(station_id)

        if (self.station.get(channel_name) is not None):
            try:
                station = await Station.objects.aget(pk=station_id)
                station.status = StationStatus.NOT_WORKING
                await station.asave()
            except Station.DoesNotExist:
                print(f'CENTRAL SERVER | Station {station_id} not found')

            await self.channel_layer.group_discard(room_name, channel_name)
            del self.station[channel_name]

        print(f'CENTRAL SERVER | client {self.channel_name} disconnected')
        await self.channel_layer.group_discard('all', channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data is not None:
                await self.on_text_message_received(text_data)
        except Exception as e:
            print(f'Error processing message: {e}')

    async def on_text_message_received(self, json_str: str):
        print(f'CENTRAL SERVER | message received: {json_str}')

        channel_name = self.channel_name
        station_id = self.scope['url_route']['kwargs']['station_id']
        room_name = await self.get_room_name(station_id)

        message_type = MessageType(json.loads(json_str)['message_type'])

        match message_type:
            case MessageType.CONNECT_REQUEST:
                if (self.station.inv.get(station_id) is None):
                    self.station[self.channel_name] = station_id
                    await self.channel_layer.group_add(room_name, channel_name)
                    await self.channel_layer.group_send(room_name, {'type': 'on_station_connect_request'})

                else:
                    print(f'STATION SERVER | warning: one more {station_id} wants connect')

            case MessageType.STATION_NOT_TAKEN_REQUEST:
                await self.channel_layer.group_send(room_name, {'type': 'on_station_not_taken_request'})

            case MessageType.STATION_TAKEN_OFFLINE_REQUEST:
                await self.channel_layer.group_send(room_name, {'type': 'on_station_taken_offline_request'})

            case MessageType.FUEL_PRICE_DATA_ASK:
                await self.channel_layer.group_send(room_name, {'type': 'on_fuel_price_data_ask'})

            case MessageType.LOYALTY_CARD_ASK:
                await self.channel_layer.group_send(room_name, {'type': 'on_loyalty_card_ask', 'json_str': json_str})

            case MessageType.PAYMENT_SENT:
                await self.channel_layer.group_send(room_name, {'type': 'on_payment_sent', 'json_str': json_str})

    async def on_station_connect_request(self, event):
        station_id = self.station.get(self.channel_name)
        try:
            station = await Station.objects.aget(pk=station_id)
            station.status = StationStatus.FREE
            await station.asave()
        except Station.DoesNotExist:
            print(f'CENTRAL SERVER | Station {station_id} not found')

        message = ConnectedMessage()
        await self.send(text_data=message.to_json())

    async def on_station_not_taken_request(self, event):
        station_id = self.station.get(self.channel_name)
        try:
            station = await Station.objects.aget(pk=station_id)
            station.status = StationStatus.FREE
            await station.asave()
        except Station.DoesNotExist:
            print(f'CENTRAL SERVER | Station {station_id} not found')

        message = StationNotTakenMessage()
        await self.send(text_data=message.to_json())

    async def on_station_taken_offline_request(self, event):
        station_id = self.station.get(self.channel_name)
        try:
            station = await Station.objects.aget(pk=station_id)
            station.status = StationStatus.BUSY_OFFLINE
            station.asave()
        except Station.DoesNotExist:
            print(f'CENTRAL SERVER | Station {station_id} not found')

        message = StationTakenOfflineMessage()
        await self.send(text_data=message.to_json())

    async def on_fuel_price_data_ask(self, event):
        station_id = self.station.get(self.channel_name)
        price_data = dict()
        try:
            station = await Station.objects.aget(pk=station_id)

            async for fuel in station.fuels.all():
                price_data[fuel.fuel_type] = fuel.price
            
            new_message = FuelPriceDataSentMessage(
                fuel_price_data=FuelPriceData(price=price_data)
            )

        except Station.DoesNotExist:
            print(f'CENTRAL SERVER | Station {station_id} not found')

            new_message = FuelPriceDataSentMessage(
                fuel_price_data=FuelPriceData(price={})
            )

        await self.send(text_data=new_message.to_json())

    async def on_loyalty_card_ask(self, event):
        message = LoyaltyCardAskMessage.from_json(event['json_str'])
        try:
            user = await User.objects.select_related('loyalty_card').aget(car_number=message.car_number.text)
            available = bool(user.loyalty_card)

            new_message = LoyaltyCardSentMessage(
                loyalty_card_available=available,
                loyalty_card_holder=user.get_full_name() or user.username if available else None,
                loyalty_card_bonuses=user.loyalty_card.balance if available else None
            )

        except User.DoesNotExist:
            new_message = LoyaltyCardSentMessage(
                loyalty_card_available=None,
                loyalty_card_holder=None,
                loyalty_card_bonuses=None
            )

        await self.send(text_data=new_message.to_json())

    async def on_payment_sent(self, event):
        message = PaymentSentMessage.from_json(event['json_str'])
        station_id = self.station.get(self.channel_name)
        try:
            station = await Station.objects.aget(pk=station_id)
            fuel = await station.fuels.aget(fuel_type=message.fuel_type.value)
            fuel.amount -= message.fuel_amount
            await fuel.asave()

            await GasStationLog.objects.acreate(
                station=station,
                fuel_type=message.fuel_type.value,
                fuel_amount=message.fuel_amount,
                car_number=message.car_number.text,
                payment_amount=message.payment_amount,
                payment_method=PaymentMethod.CARD,  # TODO: determine how the payment method will be transmitted
                payment_key=message.payment_key,
                date_time=timezone.now()
            )

            if message.used_bonuses > 0:
                try:
                    user = await User.objects.select_related('loyalty_card').aget(car_number=message.car_number.text)
                    if user.loyalty_card:
                        user.loyalty_card.balance -= message.used_bonuses
                        await user.loyalty_card.asave()
                except User.DoesNotExist:
                    pass

        except Exception as e:
            print(f'CENTRAL SERVER | Error processing payment: {e}')

        new_message = PaymentReceivedMessage()
        await self.send(text_data=new_message.to_json())

    async def get_room_name(self, station_id):
        return f'station_{station_id}'
