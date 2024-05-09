import cv2
from pprint import pprint
import pytesseract
import numpy as np
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class OpenCVParse:
    def __init__(self, imagePath):
      self.imagePath = imagePath
      self.info = None

    def createMat(self):
      if type(self.imagePath) == str:
        return cv2.imread(self.imagePath)
      elif isinstance(self.imagePath, bytes):
        image = Image.open(io.BytesIO(self.imagePath))
        image_array = np.array(image)
        return cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
      return cv2.cvtColor(self.imagePath, cv2.COLOR_RGB2BGR)

    def writeImage(self, path,  math: cv2.Mat):
      cv2.imwrite(path, math)

    def mergeRectangles(self, rects):
        mergedRects = []

        currentRect = {
            "x": rects[0][0],
            "y": rects[0][1],
            "width": rects[0][2],
            "height": rects[0][3]
        }
        for i in range(1, len(rects)):
            nextRect = {
                "x": rects[i][0],
                "y": rects[i][1],
                "width": rects[i][2],
                "height": rects[i][3]
            }

            if ((nextRect["x"] < currentRect["x"] + currentRect["width"]) and
               (nextRect["y"] < currentRect["y"] + currentRect["height"]) and
               (nextRect["y"] + nextRect["height"] > currentRect["y"]) and
               not (nextRect["x"] < 28 and nextRect["width"] == 41 and nextRect["height"] < 50)):

                currentRect["width"] = max(currentRect["x"] + currentRect["width"], nextRect["x"] + nextRect["width"]) - currentRect["x"]
                currentRect["height"] = max(currentRect["y"] + currentRect["height"], nextRect["y"] + nextRect["height"]) - currentRect["y"]
            else:
                mergedRects.append((currentRect["x"], currentRect["y"], currentRect["width"], currentRect["height"]))
                currentRect = {
                    "x": nextRect["x"],
                    "y": nextRect["y"],
                    "width": nextRect["width"],
                    "height": nextRect["height"]
                }
        mergedRects.append((currentRect["x"], currentRect["y"], currentRect["width"], currentRect["height"]))
        return mergedRects

    def parseContours(self, contours):
      sortedContours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[0])

      retContours = []
      for i in range(len(sortedContours)):
        x, y, w, h = cv2.boundingRect(sortedContours[i])

        if x > 500 and y < 15:
            continue
        else:
            retContours.append(sortedContours[i])
      boudingRects = [cv2.boundingRect(contour) for contour in retContours]
      return boudingRects

    def parseDinoFromObstacle(self, mergedRects):
      
      parsedRects = {
        "dino": {
          "x": 0,
          "y": 0,
          "width": 0,
          "height": 0
        },
        "obstacle": []
      }
      for rectangle in mergedRects:
        x, y, w, h = rectangle
        if ((w == 41 and h < 50)):
          parsedRects["dino"] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h
          }
        else:
          parsedRects["obstacle"].append({
            "x": x,
            "y": y,
            "width": w,
            "height": h
          })
      return parsedRects

    def getScore(self):
      originalImage = self.createMat()
      cropped = originalImage[0: 30, 545: 610]
      score: str = pytesseract.image_to_string(cropped)
      score = score.strip()
      if (score == '' or int(score) < 5):
        return 0
      return int(score)

    def calculateVelocity(self, dinoAndObstacle):
      if self.info == None:
        return 0

      velocityX = self.info['obstacle'][0]['x'] - dinoAndObstacle['obstacle'][0]['x']
      if velocityX < 10:
        velocityX = self.info['obstacle'][1]['x'] - dinoAndObstacle['obstacle'][1]['x']
      return velocityX

    def drawRectangle(self):

      originalImage = self.createMat()
      image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
      image = cv2.GaussianBlur(image, (5, 5), 1)
      blackAndWhiteImage = cv2.Canny(image, 300, 500)

      contours, _ = cv2.findContours(blackAndWhiteImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      mergedRects = []
      sorted_contours = self.parseContours(contours)
      try:
        mergedRects = self.mergeRectangles(sorted_contours)
      except:
        pass

      info = self.parseDinoFromObstacle(mergedRects)
      
      rectImage = originalImage.copy()
      for rectangle in mergedRects:
        x, y, w, h = rectangle
        rectImage = cv2.rectangle(rectImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
      velocity = self.calculateVelocity(info)
      info['velocity'] = velocity
      if info['obstacle']:
        self.info = info
      return [info, rectImage, originalImage]
