import redis
from pprint import pprint


# redis python development documentaqtion
# https://redis-py.readthedocs.io/en/stable/index.html



class PubSub:

    def __init__(self):
        # self.publisher = None
        # self.subscriber = None
        # self.redis_server = None
        pass

    def connect_and_subscribe(self):

        self.redis = redis.Redis(host='localhost', port=6379)

        try:
           self.redis.ping()
        except Exception as e:
            print(f'Error: Redis server - {e}')
            return False
        
        self.reader = self.redis.pubsub()
        
        self.reader.subscribe('blockchain')
              

    
        kwargs = self.redis.get_connection_kwargs()
        print('***** Connected to Redis server.')
        print(f'Server IP: {kwargs['host']}')
        print(f'Server port: {kwargs['port']}')
        
        
        
        return True
    
    def publich_blockchain(self,blockchain):
        
        self.redis.publish('blockchain',blockchain)
        
        
        
        
        
        
        
        
    
    # def publish(self, message ):
        
    #     self.publisher.
        
        
