from enum import Enum
from redis import StrictRedis
from pprint import pprint
import ast
# from account.account import Account


class Channel(Enum):
    DEV = 'dev'
    BLOCK = 'block'
    BLOCKCHAIN = 'blockchain'
    TRANSACTION = 'transaction'


class RedisPubSub():

    def __init__(self, node_id, blockchain, account):

        self.node_id = node_id
        self.redis = StrictRedis(host='localhost', port=6379)
        self.reader = self.redis.pubsub()
        self.blockchain = blockchain
        self.account = account

        # self.channels = ['dev', 'block', 'blockchain']
        self.subscribe()

        self.thread = self.reader.run_in_thread(sleep_time=0.01)

        # print(Channel.DEV)

    # def subscribe(self):
    #     ''' subscribe to all pre-defined channels'''

    #     if not self.redis:
    #         return False

    #     for channel in self.channels:
    #         self.reader.psubscribe(
    #             **{'*:' + f'{channel}': self._message_handler})

    def subscribe(self):
        ''' subscribe to all pre-defined channels'''

        if not self.redis:
            return False

        for channel in Channel:
            self.reader.psubscribe(**{'*:' + f'{channel.value}': self._message_handler})
            # self.reader.psubscribe(**{'*:' + f'{channel.value}': self.parent.redis_handler})
            
            
    def _process_received_payload(self, channel, payload):
        
        match channel:

            case Channel.DEV.value:
                #print(Channel.DEV.value)
                return

            case Channel.BLOCK.value:
                #print(Channel.BLOCK.value)
                # self.parent.redis_block_channel_handler(payload)
                self.blockchain.append_block(payload, notify=False)
                return

            case Channel.BLOCKCHAIN.value:
                #print(Channel.BLOCKCHAIN.value)
                return
            
            case Channel.TRANSACTION.value:
                
                #  this should be only for the transactions generated externally
                
                self.account.add_transaction_to_pool(payload)
                
                return

            case _:
                print('Error: Unknown channel')
                

    def _message_handler(self, msg):
        ''' Process received message
        the Redis `pubsub message` sent in the following format:
        {'type': 'pmessage', 'pattern': b'node:channel', 'channel': b'node:channel', 'data': b'payload'}
        '''

        try:

            if msg['type'] != 'pmessage':
                raise ValueError('Error: Message has a wrong format')

            channel_key_processed = msg['channel'].decode(
                'utf-8').split(':', 1)

            #  node name obtained from the message
            node_name = channel_key_processed[0]

            #  channel name obtained from the message
            channel = channel_key_processed[1]

            #  we do not want to process own message published by the node so just exit
            if node_name == self.node_id:
                return

            # converting string represeting dict to dict-type - adopted from
            # https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
            dict_msg_data = ast.literal_eval(msg['data'].decode('utf-8'))

            print('\n***** NEW MESSAGE RECEIVED *****')
            print(f'Sending node: {node_name}')
            print(f'Channel: {channel}')
            print('Message content:')
            pprint(dict_msg_data)
            print('***** END OF MESSAGE *****')

        except ValueError:
            #  this is for the case when the received message happens to be not in the standard format
            print('Error: Message received in unknown format ')
            print(msg)
            return
        
        
        self._process_received_payload(channel, dict_msg_data)

      
                
                
                

    def publish_dev(self, msg):
        self.redis.publish(channel=f'{self.node_id}:dev', message=msg)

    def publish_block(self, msg):
        self.redis.publish(channel=f'{self.node_id}:block', message=msg)
        
    def publish_transaction(self, msg):
        self.redis.publish(channel=f'{self.node_id}:transaction', message=msg)
        

    def close(self):
        self.thread.stop()
        self.thread.join(timeout=1.0)
        self.reader.close()
        self.redis.close()

    # def publish_block(self):


# if __name__ == "__main__":

#     foo = RedisPubSub('node1')

#     print("Hello1")
#     print("Hello2")
#     print("Hello3")
#     print("Hello4")
#     print("Hello5")
#     print("Hello6")
#     print("Hello7")
#     print("Hello7")
#     print("Hello7")
#     print("Hello7")

#     foo.publish_dev(msg='Hello word!')

#     foo.close()


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
