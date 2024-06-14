from redis import StrictRedis


class RedisPubSub():

    def __init__(self, node_id):

        self.node_id = node_id
        self.redis = StrictRedis(host='localhost', port=6379)
        self.reader = self.redis.pubsub()
        self.channels = ['dev', 'blockchain']
        self.subscribe()

        self.thread = self.reader.run_in_thread(sleep_time=0.01)

    def subscribe(self):

        if not self.redis:
            return False

        for channel in self.channels:
            self.reader.psubscribe(
                **{f'{self.node_id}:' + f'{channel}': self._event_handler_blockchain})

    def _event_handler_blockchain(self, msg):
        print('Message received')
        print(msg)

    def publish_dev(self, msg):
        self.redis.publish(channel=f'{self.node_id}:dev', message=msg)

    def close(self):
        self.thread.stop()
        self.thread.join(timeout=1.0)
        self.reader.close()
        self.redis.close()


if __name__ == "__main__":

    foo = RedisPubSub('node1')

    print("Hello1")
    print("Hello2")
    print("Hello3")
    print("Hello4")
    print("Hello5")
    print("Hello6")
    print("Hello7")
    print("Hello7")
    print("Hello7")
    print("Hello7")

    foo.publish_dev(msg='Hello word!')

    foo.close()












# import redis
# from pprint import pprint


# # redis python development documentaqtion
# # https://redis-py.readthedocs.io/en/stable/index.html



# class PubSub:

#     def __init__(self):
#         # self.publisher = None
#         # self.subscriber = None
#         # self.redis_server = None
#         pass

#     def connect_and_subscribe(self):

#         self.redis = redis.Redis(host='localhost', port=6379)

#         try:
#            self.redis.ping()
#         except Exception as e:
#             print(f'Error: Redis server - {e}')
#             return False
        
#         self.reader = self.redis.pubsub()
        
#         self.reader.subscribe('blockchain')
              

    
#         kwargs = self.redis.get_connection_kwargs()
#         print('***** Connected to Redis server.')
#         print(f'Server IP: {kwargs['host']}')
#         print(f'Server port: {kwargs['port']}')
        
        
        
#         return True
    
#     def publich_blockchain(self,blockchain):
        
#         self.redis.publish('blockchain',blockchain)
        
        
        
        
        
        
        
        
    
#     # def publish(self, message ):
        
#     #     self.publisher.
        
        
