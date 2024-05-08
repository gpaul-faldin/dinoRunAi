from drawRectangles import OpenCVParse;
import cv2
import mss
import numpy as np
import os
from playwrightInteraction import PlaywrightInteraction
import time


def captureScreen(x, y, width, height):
  with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        frame = np.array(sct.grab(monitor))
        return frame


def runWithPlaywright():

  pWClass = PlaywrightInteraction()
  buff = pWClass.captureCanvas()
  openCVParse = OpenCVParse(buff)
  # info, rectImage, originalImage  = openCVParse.drawRectangle()
  # cv2.imwrite("./dinoRunAi/logs/0.png", rectImage)
  # openCVParse.writeImage(os.getcwd() + "\\dinoRunAi\\logs\\0.png", rectImage)
  counter = 0
  while True:
    openCVParse.imagePath = pWClass.captureCanvas()
    
    info, rectImage, originalImage  = openCVParse.drawRectangle()
    cv2.imshow('frame', rectImage)
    # if (info['dino']['y'] == 0):
    #   score = openCVParse.getScore()
    #   break
    key = cv2.waitKeyEx(1)
    print(key)
    if (key == 113):
      break
    elif (key == 32):
      pWClass.jump()
    elif (key == 100):
      pWClass.jump("half")
    elif (key == 119):
      openCVParse.writeImage(os.getcwd() + f"\\logs\\{counter}.png", originalImage)
      counter += 1
  # print(score)
  print(info)
  cv2.destroyAllWindows()



runWithPlaywright()

def main():
  capture_width, capture_height = 685, 150
  frame = captureScreen(652, 375, capture_width, capture_height)
  openCVParse = OpenCVParse(frame)
  counter = 0

  while True:
    openCVParse.imagePath = captureScreen(652, 375, capture_width, capture_height)
    info, rectImage, originalImage  = openCVParse.drawRectangle()

    cv2.imshow('frame', rectImage)
    if (info['dino']['y'] == 0):
      score = openCVParse.getScore()
      break
    key = cv2.waitKey(1)
    if (key == 113):
      break
    elif (key == 119):
      openCVParse.writeImage(os.getcwd() + f"\\logs\\{counter}.png", originalImage)
      counter += 1
  print(score)
  print(info)
  cv2.destroyAllWindows()
  
  # openCVParse.imagePath = (os.getcwd() + "\\logs\\0.png")
  # info, rectImage, originalImage  = openCVParse.drawRectangle()
  # openCVParse.writeImage(os.getcwd() + "\\logs\\Color0.png", rectImage)
  # print(info)
  
  # openCVParse.imagePath = (os.getcwd() + "\\logs\\2.png")
  # info, rectImage, originalImage  = openCVParse.drawRectangle()
  # openCVParse.writeImage(os.getcwd() + "\\logs\\Color2.png", rectImage)
  # print(info)

# main()