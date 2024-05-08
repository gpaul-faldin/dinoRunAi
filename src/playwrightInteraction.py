from playwright.sync_api import sync_playwright, Playwright, Page, Browser
import signal
import time

class PlaywrightInteraction:
    def __init__(self):
        self.playwright: Playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(headless=False)
        self.page: Page = self.browser.new_page()
        self.page.set_viewport_size({"width": 750, "height": 310})
        self.page.goto("https://trex-runner.com/", wait_until="domcontentloaded")
        self.page.mouse.wheel(0, 220)
        self.page.mouse.click(150, 200)
        self.buffer = None

    def captureCanvas(self):
        screenshot_buffer = self.page.locator("canvas").screenshot()
        self.buffer = screenshot_buffer
        return screenshot_buffer

    def jump(self, duration="full"):
        if duration == "full":
            self.page.keyboard.press(" ")
        else:
            self.page.keyboard.press(" ", delay=80)

    def closeBrowser(self):
        self.browser.close()







# from playwright.sync_api import sync_playwright
# import signal

def main():
    playwrigth: Playwright = sync_playwright().start()
    browser: Browser = playwrigth.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 800, "height": 650},
        screen={"width": 800, "height": 650},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page: Page = browser.new_page()
    page.goto("https://trex-runner.com/", wait_until="domcontentloaded")
    page.mouse.wheel(0, 220)
    signal.signal(signal.SIGINT, lambda x, y: browser.close())
    
    page.screenshot(path="check.png")
    print(page.locator("canvas").bounding_box())
    page.screenshot(path="test.png", clip={"x": 100, "y": 67.921875, "width": 620, "height": 150})
    page.keyboard.press(" ")
    time.sleep(1)
    print(page.locator("canvas").bounding_box())
    page.screenshot(path="test1.png", clip={"x": 100, "y": 67.921875, "width": 620, "height": 150})
    # time.sleep(1)
    # print(page.locator("canvas").bounding_box())
    # page.screenshot(path="test2.png", clip={"x": 100, "y": 67.921875, "width": 600, "height": 150})
    time.sleep(100)


    # Run forever until a termination signal is received

    # page.evaluate(key_down(" ", "keyup"))
    browser.close()
    # while True:
    #     page.locator("canvas").screenshot(path="test.png")
    #     print("H")

if __name__ == "__main__":
    main()



# def captureCanvas(page: Page):
#     return page.locator("canvas").screenshot()

