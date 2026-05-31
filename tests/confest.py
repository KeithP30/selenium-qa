import pytest
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Fixture: Chrome Driver ─────────────────────────────────────
@pytest.fixture(scope='function')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    if os.getenv('CI'):                      # headless di CI/CD
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield d
    d.quit()

# ── Fungsi: Baca CSV ──────────────────────────────────────────
def load_csv(filename):
    """Baca CSV dari folder data/, kembalikan list of dict"""
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

# ── Hook: Screenshot Otomatis saat FAIL ───────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)
            # Nama file: nama test case yang gagal (karakter aman)
            safe_name = item.nodeid.replace('/', '_').replace('::', '__')
            screenshot_path = f'reports/screenshots/{safe_name}.png'
            driver.save_screenshot(screenshot_path)
            print(f'\n📸 Screenshot disimpan: {screenshot_path}')