import time
from redis import StrictRedis

#  https://tech.webinterpret.com/redis-notifications-python/

def event_handler(msg):
    print(msg)
    # thread.stop()  
    
    
if __name__ == "__main__":
    
    redis = StrictRedis(host='localhost', port=6379)
    # redis = Redis(host='localhost', port=6379)

    pubsub = redis.pubsub()
    # pubsub.psubscribe(**{'__keyevent@0__:expired': event_handler})
    pubsub.psubscribe(**{'user1:channel1': event_handler})
    # pubsub.subscribe('channel1')
    thread = pubsub.run_in_thread(sleep_time=0.01)
    
    print("Hello1")
    print("Hello2")
    print("Hello3")
    print("Hello4")
    print("Hello5")
    print("Hello6")
    print("Hello7")
    
    redis.publish('*:channel1','Hello there!')
    
    thread.stop() 
    thread.join(timeout=1.0)
    pubsub.close()
    redis.close()
    
    
