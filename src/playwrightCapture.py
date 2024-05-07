from playwright.sync_api import sync_playwright, Playwright


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 750, "height": 310})
    page.screenshot(path="test1.png")
    page.goto("https://trex-runner.com/", wait_until="domcontentloaded")
    page.screenshot(path="test2.png")
    page.locator("canvas").screenshot(path="dino.png")
    input("Press Enter to close the browser...")

    #browser.close()

with sync_playwright() as playwright:
    run(playwright)