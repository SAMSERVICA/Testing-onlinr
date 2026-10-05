import os
from playwright.sync_api import sync_playwright

def start_environment():
    session_cookie = os.environ.get("PREPARE_COOKIE")
    if not session_cookie:
        print("Error: PREPARE_COOKIE is missing!")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # تزریق کوکی session دریافت شده از مرورگر
        context.add_cookies([{
            'name': 'session',
            'value': session_cookie,
            'domain': 'prepare.sh',
            'path': '/',
            'httpOnly': True,
            'secure': True,
            'sameSite': 'Lax'
        }])

        page = context.new_page()
        print("Opening environments page...")
        page.goto("https://prepare.sh/profile/environments", wait_until="networkidle")
        page.wait_for_timeout(4000)

        # بررسی وجود دکمه‌های روشن کردن
        resume_button = page.locator("button:has-text('Resume'), button:has-text('Start'), a:has-text('Open'), button:has-text('Turn on')")

        if resume_button.is_visible():
            print("Server is hibernated. Clicking to start/resume...")
            resume_button.first.click()
            page.wait_for_timeout(5000)
            print("Server start command sent successfully!")
        else:
            print("Server is already running or no start button found.")

        browser.close()

if __name__ == "__main__":
    start_environment()
