import cv2
import os
import time
import threading
from ProdConQ import Queue
clip = "clip.mp4" # clip to extract frames from
frameDelay = 42 # wait 42ms between displaying frames

# Get frames from an mp4 file and enqueue
# them into a producer consumer style queue
def extractFrames(clip, queue):
    count = 1
    vidcap = cv2.VideoCapture(clip)

    success = True
    # read frames from clip and enqueue them    
    while success and count < 72: 
        success, image = vidcap.read()
        queue.enqueue(image)

        # count frames for testing/debugging 
        print(f'Reading frame {count} {success}')
        count += 1
    print(f'Extracted {count} frames successfully')
    queue.enqueue(None) # mark the end of this queue
        
# Dequeue frames from a queue of colored frames,
# convert them to grayscale, then enqueue them
# into a new queue of grayscale frames
def convertToGrayscale(qColor, qGray):
    count = 1
    while True:
        if qColor.isEmpty():
            continue
        else:
            colorFrame = qColor.dequeue()
            if colorFrame is None:
                break # end of the queue
            grayscaleFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
            qGray.enqueue(grayscaleFrame)
            print(f'Converted frame {count} to grayscale')
            count += 1
            
    print(f'Completed conversion of {count} frames to grayscale')
    qGray.enqueue(None) # mark end of this queue

    
# Display grayscale frames using video player
def displayFrames(queue):
    count = 1
    while True:
        if queue.isEmpty():
            continue
        else:
            frame = queue.dequeue()
            if frame is None:
                break # end of queue
            print('Displaying frame {count}')
            cv2.imshow('Video', frame)

            global frameDelay
            if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
                break
            count += 1
            
        cv2.destroyAllWindows()
        print('Completed displaying of {count} frames')

def main():
    qColor = Queue()
    qGray = Queue()

    extractFramesThread = threading.Thread(target = extractFrames, args = (clip, qColor))
    convertFramesThread = threading.Thread(target = convertToGrayscale, args = (qColor, qGray))
    displayFramesThread = threading.Thread(target = displayFrames, args = (qGray,))

    extractFramesThread.start()
    convertFramesThread.start()
    displayFramesThread.start()
    
    
if __name__ == "__main__":
    main()





        
        


        
