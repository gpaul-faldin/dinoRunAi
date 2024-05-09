from drawRectangles import OpenCVParse;
import cv2
import asyncio
from queue import Queue
from asyncPWInteraction import AsyncPWInteraction
import threading
import time


async def runWithPlaywright(frameName, headless = False, commandQueue: Queue = None, dataQueue: Queue = None, resultQueue: Queue = None):

    asyncPWClass = AsyncPWInteraction()
    await asyncPWClass.init()
    openCVClass = OpenCVParse(None)
    running = False
    score = 0

    try:
        while True:
            await asyncPWClass.captureCanvas()
            openCVClass.imagePath = asyncPWClass.buffer
            info, rectImage, _ = openCVClass.drawRectangle()
            dataQueue.put_nowait(info)
            # cv2.imshow(frameName, rectImage)
            # cv2.waitKey(1)
            if not commandQueue.empty():
              try:
                command = commandQueue.get_nowait()
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
            if (running == False and openCVClass.getScore() < 10):
                continue
            else:
                running = True
            if (info['dino']['y'] == 0):
                score = openCVClass.getScore()
                resultQueue.put_nowait(score)
                break
            time.sleep(0.0001)
        # print("-----------------------------------------------------------------------------------------------")
        # print(f'frame: {frameName}')
        # print(f'score: {score}')
        # print(f'info: {info}')
        # print("-----------------------------------------------------------------------------------------------")
    finally:
        await asyncPWClass.closeBrowser()
        cv2.destroyAllWindows()
    return 0

def run_in_thread(frameName, headless=False, commandQueue=None, dataQueue=None, resultQueue=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(runWithPlaywright(frameName, headless, commandQueue, dataQueue, resultQueue))
    finally:
        loop.close()

def getInstance(name):
  commandQueue = Queue()
  dataQueue = Queue()
  resultQueue = Queue()
  t = threading.Thread(target=run_in_thread, name=name, args=(name, False, commandQueue, dataQueue, resultQueue))
  return (t, commandQueue, dataQueue, resultQueue)

# instance = getInstance('0')
# instance[0].start()
# time.sleep(5)
# while True:
#   if (not instance[2].empty()):
#     print(instance[2].get_nowait())

#   if not instance[0].is_alive():
#     print(instance[3].get_nowait())
#     break
#   instance[1].put("jump")
#   time.sleep(0.00001)
