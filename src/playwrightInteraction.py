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

# def main():
#     playwrigth: Playwright = sync_playwright().start()
#     browser:Browser = playwrigth.chromium.launch(headless=False)
#     page: Page = browser.new_page()
#     page.set_viewport_size({"width": 750, "height": 310})
#     page.screenshot(path="test1.png")
#     page.goto("https://trex-runner.com/", wait_until="domcontentloaded")
#     page.mouse.wheel(0, 220)
#     signal.signal(signal.SIGINT, lambda x, y: browser.close())



#     # Run forever until a termination signal is received

#     # page.evaluate(key_down(" ", "keyup"))
#     time.sleep(10000)
#     # while True:
#     #     page.locator("canvas").screenshot(path="test.png")
#     #     print("H")

# if __name__ == "__main__":
#     main()



# def captureCanvas(page: Page):
#     return page.locator("canvas").screenshot()

