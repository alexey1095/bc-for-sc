# from pubsub.pubsub import PubSub


# if __name__ == "__main__":

#     pubsub = PubSub()
#     connected = pubsub.connect_and_subscribe()

#     if not connected:
#         exit()

# import time
# import asyncio

# import redis.asyncio as redis

# STOPWORD = "STOP"


# async def reader(channel: redis.client.PubSub):
#     while True:
#         # time.sleep(1)
#         message = await channel.get_message(ignore_subscribe_messages=True)
#         if message is not None:
#             print(f"(Reader) Message Received: {message}")
#             # if message["data"].decode() == STOPWORD:
#             #     print("(Reader) STOP")
#             #     break


# async def main():

#     r = redis.from_url("redis://localhost")
#     async with r.pubsub() as pubsub:
#         await pubsub.subscribe("channel:1", "channel:2")

#         future = asyncio.create_task(reader(pubsub))

#         await r.publish("channel:1", "Hello")
#         await r.publish("channel:2", "World")
#         await r.publish("channel:1", STOPWORD)
        
#         print("Hello , how are you 0")

#         await future


# if __name__ == "__main__":

#     asyncio.run(main())
#     # await main()
    
#     print("Hello , how are you 1")
#     print("Hello , how are you 2")
#     print("Hello , how are you 3")
#     print("Hello , how are you 4")
#     print("Hello , how are you 5")
#     print("Hello , how are you 6")
#     print("Hello , how are you 7")
#     print("Hello , how are you 8")
#     print("Hello , how are you 9")


#     import redis

#     # Connect to local Redis instance
#     redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
#     channel = 'my_channel'
#     # while True:
#     #     message = input("Enter a message: ")
#     #     redis_client.publish(channel, message)


#     channel = 'my_channel'
#     pubsub = redis_client.pubsub()
#     pubsub.subscribe(channel)
#     print(f"Subscribed to {channel}. Waiting for messages...")
#     for message in pubsub.listen():
#         if message['type'] == 'message':
#             print(f"Received: {message['data'].decode('utf-8')}")


#  https://saktidwicahyono.name/blogs/async-and-sync-python-pubsub-with-redis/

#  https://stackoverflow.com/questions/63573906/how-can-i-publish-a-message-in-redis-channel-asynchronously-with-python

# import asyncio
# import async_timeout
# import json
# import logging
# import redis.asyncio as redis

# CHANNEL_NAME = "notification"

# logging.basicConfig(level=logging.DEBUG)


# async def send_message(user_id: int, message: str):
#     # write real code here
#     logging.debug(f"Sending message to user {user_id}: {message}")
#     await asyncio.sleep(0.2)


# async def handle_notification():
#     r = redis.Redis()
#     pubsub = r.pubsub()
#     await pubsub.subscribe(CHANNEL_NAME)
#     while True:
#         try:
#             async with async_timeout.timeout(1):
#                 message = await pubsub.get_message()
#                 if message and message["type"] == "message":
#                     payload = json.loads(message["data"])
#                     # TODO: do validation on payload
#                     await send_message(payload["user_id"], payload["message"])
#         except (asyncio.TimeoutError, json.decoder.JSONDecodeError) as e:
#             logging.error(e)


# if __name__ == "__main__":
#     asyncio.run(handle_notification())
