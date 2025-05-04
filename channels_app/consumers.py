import json
from bidict import bidict

from channels.generic.websocket import AsyncWebsocketConsumer

from channels_app.central_server_ws_api import *


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
            # TODO: save that station is not working

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

            case MessageType.LOYALTY_CARD_ASK:
                await self.channel_layer.group_send(room_name, {'type': 'on_loyalty_card_ask', 'json_str': json_str})

            case MessageType.PAYMENT_SENT:
                await self.channel_layer.group_send(room_name, {'type': 'on_payment_sent', 'json_str': json_str})

    async def on_station_connect_request(self, event):
        # TODO: save that station is working

        message = ConnectedMessage()
        await self.send(text_data=message.to_json())

    async def on_station_not_taken_request(self, event):
        # TODO: save that station is not taken

        message = StationNotTakenMessage()
        await self.send(text_data=message.to_json())

    async def on_station_taken_offline_request(self, event):
        # TODO: save that station is taken offline

        message = StationTakenOfflineMessage()
        await self.send(text_data=message.to_json())

    async def on_loyalty_card_ask(self, event):
        message = LoyaltyCardAskMessage.from_json(event['json_str'])
        # TODO: get loyalty card data

        new_message = LoyaltyCardSentMessage(
            loyalty_card_available=True,
            # if loyalty_card_available is False, then other fields should be None
            loyalty_card_holder='SOME NAME',
            loyalty_card_bonuses=10000
        )
        await self.send(text_data=new_message.to_json())

    async def on_payment_sent(self, event):
        message = PaymentSentMessage.from_json(event['json_str'])
        # TODO: save payment data in logs

        new_message = PaymentReceivedMessage()
        await self.send(text_data=new_message.to_json())

    async def get_room_name(self, station_id):
        return f'station_{station_id}'
