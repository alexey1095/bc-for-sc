# # node/consumers.py
import json

# from channels.generic.websocket import WebsocketConsumer

# # NodeWebSocketConsumer

# class NodeWebSocketConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         # self.send(text_data=json.dumps({"message": "Hello "}))
        
        

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         pass
#         # text_data_json = json.loads(text_data)
#         # message = text_data_json["message"]

#         # self.send(text_data=json.dumps({"message": message+" from server"}))


from channels.generic.websocket import AsyncWebsocketConsumer


class NodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.node_id = self.scope["url_route"]["kwargs"]["node_id"]
        self.node_group_name = "node_%s" % self.node_id

        # Join room group
        await self.channel_layer.group_add(self.node_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.node_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.node_group_name, {"type": "node_message", "message": message}
        )

    # Receive message from room group
    async def node_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))