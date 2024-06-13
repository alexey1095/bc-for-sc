from pubsub.pubsub import PubSub


if __name__ == "__main__":

    pubsub = PubSub()
    connected = pubsub.connect_and_subscribe()    

    if not connected:
        exit()
        
    
        
        
    
