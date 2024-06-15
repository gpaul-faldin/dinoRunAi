import asyncio
import cv2
from drawRectangles import OpenCVParse
from playwright.async_api import async_playwright, Playwright, Browser, Page

class AsyncPWInteraction:

  def __init__(self): 
    self.playwright: Playwright = None
    self.browser: Browser = None
    self.page: Page = None
    self.buffer = None

  async def init(self):
    self.playwright = await async_playwright().start()
    self.browser = await self.playwright.chromium.launch(headless=True)
    self.page = await self.browser.new_page()
    await self.page.set_viewport_size({"width": 750, "height": 310})
    await self.page.goto("file:///A:/Work/AI%20dinoRun/Python/OverlayDinoRun/dinoRunAi/SiteCopy/test.html", wait_until="domcontentloaded")

  async def closeBrowser(self):
    await self.browser.close()
    await self.playwright.stop()

  async def checkSC(self):
    await self.page.screenshot(path="check.png")

  async def captureCanvas(self, timeout=2):
    try:
      self.buffer = await self.page.locator('canvas').screenshot(timeout=timeout)
    except Exception as e:
      print('---------------------------------')
      print('captureCanvas timed out')
      print('---------------------------------')

  async def jump(self, duration="full"):
    if duration == "full":
      await self.page.keyboard.press(" ")
    else:
      await self.page.keyboard.press(" ", delay=80)

# async def main():
#     asyncPWClass = AsyncPWInteraction()
#     await asyncPWClass.init()
#     openCVClass = OpenCVParse(None)
#     running = False
#     score = 0

#     try:
#         while True:
#             await asyncPWClass.captureCanvas()
#             openCVClass.imagePath = asyncPWClass.buffer
#             info, rectImage, originalImage = openCVClass.drawRectangle()
#             cv2.imshow('frame', rectImage)
#             key = cv2.waitKeyEx(1)
#             if key == 113:  # 'q' key
#                 break
#             elif key == 32:  # Spacebar key
#                 task = asyncio.create_task(asyncPWClass.jump())
#                 try:
#                     await task
#                 except asyncio.CancelledError:
#                     pass
#             elif key == 100:  # 'd' key
#                 task = asyncio.create_task(asyncPWClass.jump("half"))
#                 try:
#                     await task.result()
#                 except asyncio.CancelledError:
#                     pass
#             if (running == False and openCVClass.getScore() < 5):
#                 continue
#             else:
#                 running = True
#             if (info['dino']['y'] == 0):
#                 score = openCVClass.getScore()
#                 break
#         print(score)
#         print(info)
#     finally:
#         await asyncPWClass.closeBrowser()
#         cv2.destroyAllWindows()
#     return 0

# asyncio.run(main())
