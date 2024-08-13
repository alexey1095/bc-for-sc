from enum import Enum
from typing import Type
from redis import StrictRedis
from pprint import pprint
import ast
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Channel(Enum):
    DEV = 'dev'
    BLOCK = 'block'
    BLOCKCHAIN = 'blockchain'
    TRANSACTION = 'transaction'


class RedisPubSub():
    
    # this is a simplified implementastion of
    #  Zhiqin Zhu - Blockchain based consensus checking in decentralized cloud storage

    # def __init__(self, node_id, blockchain:Type[Blockchain], account:Type[Account]):
    def __init__(self, node_id, blockchain, account):

        self.node_id = node_id
        self.redis = StrictRedis(host='localhost', port=6379)
        self.reader = self.redis.pubsub()
        self.blockchain = blockchain
        self.account = account

        # self.channels = ['dev', 'block', 'blockchain']
        self.subscribe()

        self.thread = self.reader.run_in_thread(sleep_time=0.01)


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
            
            print("\nchannel_key_processed " )
            print(channel_key_processed)

            #  node name obtained from the message
            node_name = channel_key_processed[0]
            print("\nnode_name "+node_name )

            #  channel name obtained from the message
            channel = channel_key_processed[1]
            print("\nchannel "+channel )
            

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
            
            
            # adding additional fields to dict to be visible in httml
            
            dict_msg_data['sending_node'] =node_name
            dict_msg_data['channel'] =channel
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
            f'node_{self.blockchain.node_id}',
            {
                'type': 'node_message',
                'message': dict_msg_data
            }
        )

        except ValueError as e:
            #  this is for the case when the received message happens to be not in the standard format
            print('\nError: pubsub -- Message received in unknown format \n')
            pprint(msg)
            print('\n')            
            print(e)
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

