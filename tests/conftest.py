import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope='function')
def driver():
    options = Options()
    
    # Deteksi otomatis: Jika di GitHub Actions, jalankan tanpa GUI (Headless)
    if os.getenv('CI') == 'true':
        options.add_argument('--headless')
    
    options.add_argument('--width=1920')
    options.add_argument('--height=1080')

    # Setup Geckodriver untuk Firefox
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

# Hook otomatis untuk mengambil screenshot saat test FAIL
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