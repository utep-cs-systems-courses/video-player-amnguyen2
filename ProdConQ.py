"""
Abram Nguyen

https://docs.python.org/2.0/lib/semaphore-objects.html
"""
import threading

Q_LIMIT = 10

# Custom Q class implemented using threading semaphores 
class Queue:
    def __init__(self):
        self.items = [] # holds values (frames)
        self.empty = Semaphore(Q_LIMIT) # how many spaces in q are empty?
        self.full = Semaphore(0) # how many spaces in q are full?

    def getSize(self):
        return len(self.items)
        
    def isEmpty(self):
        return self.items == []
        
    def enqueue(self, item):
        self.empty.acquire() # if > 0, counter -1. if 0, block, wait for full.release()
        self.items.insert(0, item) # back of the line is item 0 
        self.full.release() # full counter +1

    def dequeue(self):
        self.full.acquire() # if > 0, counter -1. if 0, block, wait for empty.release()
        item = self.items.pop() # front of the line is last item
        self.empty.release() # empty counter +1
        return item

    
# Producer class moves frames into queue
class Producer:
    def __init__(self, q, frames):
        self.q = q # custom q object uses counting semaphores
        self.frames = frames

    def run(self):
        for f in self.frames:
            self.q.enqueue(f)
            
            
# Consumer class retrieves frames from queue
class Consumer:
    def __init__(self, q):
        self.q = q

    def run(self):
        for f in range(self.q.getSize()):
            frame = self.q.dequeue()
            print(frame) 
        
