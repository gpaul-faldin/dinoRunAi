from drawRectangles import OpenCVParse;
import cv2
import asyncio
from queue import Queue
from asyncPWInteraction import AsyncPWInteraction
import threading
import time


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
            info, rectImage, _ = openCVClass.drawRectangle()
            resultQueue.put_nowait(info)
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
                break
            time.sleep(0.0001)
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

def getInstance(name):
  commandQueue = Queue()
  resultQueue = Queue()
  t = threading.Thread(target=run_in_thread, name=name, args=(name, False, commandQueue, resultQueue))
  return (t, commandQueue, resultQueue)


# async def main():
#   instance = getInstance('0')
#   instance[0].start()
#   time.sleep(5)
#   while True:
#     if (not instance[2].empty()):
#       print("-------------------------------------------INFO FROM RESULTQUEUE.GET()----------------------------------------")
#       print(instance[2].get_nowait())

#     if not instance[0].is_alive():
#       break
#     await instance[1].put("jump")
#     time.sleep(0.1)

# asyncio.run(main())

instance = getInstance('0')
instance[0].start()
time.sleep(5)
while True:
  if (not instance[2].empty()):
    print(instance[2].get_nowait())

  if not instance[0].is_alive():
    break
  instance[1].put("jump")
  time.sleep(0.00001)
