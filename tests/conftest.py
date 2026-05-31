# tests/conftest.py
import pytest
import os
import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope='function')
def driver():
    options = Options()

    # FIX BUG-6: Firefox headless flag yang benar adalah '-headless' (1 dash)
    # '--headless' (2 dash) adalah flag Chrome, bukan Firefox
    if os.getenv('CI'):
        options.add_argument('-headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')

    # Matikan tab welcome / default browser check
    options.set_preference("browser.shell.checkDefaultBrowser", False)
    options.set_preference("browser.startup.homepage", "about:blank")
    options.set_preference("startup.homepage_welcome_url", "about:blank")
    options.set_preference("startup.homepage_welcome_url.additional", "about:blank")

    service = Service(GeckoDriverManager().install())
    d = webdriver.Firefox(service=service, options=options)
    d.implicitly_wait(10)

    yield d
    d.quit()


# Fixture untuk login page
@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


# FIX BUG-9: Ganti csv.reader -> csv.DictReader agar row bisa diakses
# dengan row['key'] bukan row[index]
def load_csv(file_name):
    """Baca CSV dari folder data/, kembalikan list of dict (DictReader)."""
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
    with open(file_path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


# Hook otomatis screenshot saat test FAIL
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)
            name = item.nodeid.replace('/', '_').replace('::', '_')
            driver.save_screenshot(f'reports/screenshots/{name}.png')
            print(f'\nScreenshot disimpan: reports/screenshots/{name}.png')