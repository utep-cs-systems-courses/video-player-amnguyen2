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
        self.empty = threading.Semaphore(Q_LIMIT) # how many spaces in q are empty?
        self.full = threading.Semaphore(0) # how many spaces in q are full?

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
