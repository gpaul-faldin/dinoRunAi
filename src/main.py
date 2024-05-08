from drawRectangles import OpenCVParse;
import cv2
import mss
import asyncio
import numpy as np
import os
from queue import Queue
from asyncPWInteraction import AsyncPWInteraction
import threading
from pynput import keyboard
import time


def captureScreen(x, y, width, height):
  with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        frame = np.array(sct.grab(monitor))
        return frame

async def runWithPlaywright(frameName, headless = False, commandQueue: Queue = None, resultQueue: Queue = None):

    asyncPWClass = AsyncPWInteraction()
    await asyncPWClass.init()
    openCVClass = OpenCVParse(None)
    running = False
    score = 0

    try:
        while True:
            await asyncPWClass.captureCanvas()
            openCVClass.imagePath = asyncPWClass.buffer
            info, rectImage, originalImage = openCVClass.drawRectangle()
            #cv2.imshow(str(frameName), rectImage)
            #cv2.waitKey(1)
            
            if not commandQueue.empty():
              try:
                command =  commandQueue.get_nowait()
                if command == 'jump':
                  await asyncPWClass.jump()
                elif command == 'half':
                  await asyncPWClass.jump("half")
                elif command == 'info':
                  print(info['dino'])
                elif command == 'quit':

                  break
              except asyncio.CancelledError:
                pass
              resultQueue.put(info)
            if (running == False and openCVClass.getScore() < 10):
                continue
            else:
                running = True
            if (info['dino']['y'] == 0):
                score = openCVClass.getScore()
                break
        print("-----------------------------------------------------------------------------------------------")
        print(f'frame: {frameName}')
        print(f'score: {score}')
        print(f'info: {info}')
        print("-----------------------------------------------------------------------------------------------")
    finally:
        await asyncPWClass.closeBrowser()
        cv2.destroyAllWindows()
    return 0

def run_in_thread(frameName, headless=False, commandQueue=None, resultQueue=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(runWithPlaywright(frameName, headless, commandQueue, resultQueue))
    finally:
        loop.close()

threads:list = []

for i in range(1):  # Replace 5 with the number of threads you want
    commandQueue = Queue()
    resultQueue = Queue()
    

    
    t = threading.Thread(target=run_in_thread, name=i, args=(i, False, commandQueue, resultQueue))
    t.start()

    threads.append((t, commandQueue, resultQueue))



time.sleep(5)
while True:
  if (not threads[0][2].empty()):
    print(threads[0][2].get())

  if not threads[0][0].is_alive():
    break
  threads[0][1].put("jump")
  time.sleep(0.1)
  




# time.sleep(10)
# threads[0][1].put("jump")
# print(threads[0][2].get())
# for t in threads:
#     t.join()

# async def threadTest():
#   command = Queue()
#   result = Queue()
#   await asyncio.to_thread(runWithPlaywright, "frame", False, command, result)
  
#   print("here")
  
#   while True:
#     keyboard.on_press_key(" ", lambda _: command.put("jump"))

# asyncio.run(threadTest())

# asyncio.run(runWithPlaywright("frame", False, command, result))

# def main():
#   capture_width, capture_height = 685, 150
#   frame = captureScreen(652, 375, capture_width, capture_height)
#   openCVParse = OpenCVParse(frame)
#   counter = 0

#   while True:
#     openCVParse.imagePath = captureScreen(652, 375, capture_width, capture_height)
#     info, rectImage, originalImage  = openCVParse.drawRectangle()

#     cv2.imshow('frame', rectImage)
#     if (info['dino']['y'] == 0):
#       score = openCVParse.getScore()
#       break
#     key = cv2.waitKey(1)
#     if (key == 113):
#       break
#     elif (key == 119):
#       openCVParse.writeImage(os.getcwd() + f"\\logs\\{counter}.png", originalImage)
#       counter += 1
#   print(score)
#   print(info)
#   cv2.destroyAllWindows()
  
#   # openCVParse.imagePath = (os.getcwd() + "\\logs\\0.png")
#   # info, rectImage, originalImage  = openCVParse.drawRectangle()
#   # openCVParse.writeImage(os.getcwd() + "\\logs\\Color0.png", rectImage)
#   # print(info)
  
#   # openCVParse.imagePath = (os.getcwd() + "\\logs\\2.png")
#   # info, rectImage, originalImage  = openCVParse.drawRectangle()
#   # openCVParse.writeImage(os.getcwd() + "\\logs\\Color2.png", rectImage)
#   # print(info)

# main()