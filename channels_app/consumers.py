import json
from enum import Enum
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

class SenderType(Enum):
    CAMERA = 'camera'
    GAS_NOZZLE = 'gas_nozzle'
    STATION = 'station'

class MessageType(Enum):
    CONNECT = 'connect'

    START_SERVICE = 'start_service'
    RESET_SERVICE = 'reset_service'

    CAR_NUMBER_RECEIVED = 'car_number_received'
    START_GAS_NOZZLE = 'start_gas_nozzle'
    GAS_NOZZLE_FINISHED = 'gas_nozzle_finished'

    CAMERA_CONNECTED = 'camera_connected'
    CAMERA_DISCONNECTED = 'camera_disconnected'
    GAS_NOZZLE_CONNECTED = 'gas_nozzle_connected'
    GAS_NOZZLE_DISCONNECTED = 'gas_nozzle_disconnected'

class ServerConsumer(AsyncWebsocketConsumer):
    groups = ["station_group"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("station_group", self.channel_name)
        print(f"Client connected: {self.channel_name}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard("station_group", self.channel_name)
        print(f"Client disconnected: {self.channel_name}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message_type = MessageType(data['message_type'])
            sender = SenderType(data['sender'])

            if message_type == MessageType.CONNECT:
                if sender == SenderType.CAMERA:
                    await self.channel_layer.group_send(
                        "station_group",
                        {
                            'type': 'camera_connected',
                            'sender': SenderType.STATION.value,
                            'message_type': MessageType.CAMERA_CONNECTED.value
                        }
                    )
                
                elif sender == SenderType.GAS_NOZZLE:
                    await self.channel_layer.group_send(
                        "station_group",
                        {
                            'type': 'gas_nozzle_connected',
                            'sender': SenderType.STATION.value,
                            'message_type': MessageType.GAS_NOZZLE_CONNECTED.value
                        }
                    )
                
        except Exception as e:
            print(f"Error processing message: {e}")
    
    async def camera_connected(self, event):
        await self.send(text_data=json.dumps(event, cls=DjangoJSONEncoder))

    async def gas_nozzle_connected(self, event):
        await self.send(text_data=json.dumps(event, cls=DjangoJSONEncoder))
