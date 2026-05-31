# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # ── URL ───────────────────────────────────────────
    # Setelah login berhasil di the-internet.herokuapp.com,
    # user diarahkan ke /secure
    EXPECTED_URL_PART = '/secure'

    # ── Locators ──────────────────────────────────────
    LOGOUT_BTN  = (By.CSS_SELECTOR, '.button.secondary[href="/logout"]')
    SECURE_MSG  = (By.ID, 'flash')          # Pesan "You logged into..." setelah login
    HEADER_TEXT = (By.TAG_NAME, 'h2')         # "Secure Area" heading

    # ── Actions ───────────────────────────────────────
    def logout(self):
        """Klik tombol Logout dan tunggu redirect ke halaman login"""
        self.logger.info('Klik tombol Logout')
        self.click(self.LOGOUT_BTN)

    # ── Assertion Helpers ─────────────────────────────
    def is_on_dashboard(self):
        """Return True jika URL mengandung '/secure' dan heading tampil"""
        try:
            url_ok      = self.EXPECTED_URL_PART in self.get_current_url()
            heading_ok  = self.is_visible(self.HEADER_TEXT)
            return url_ok and heading_ok
        except:
            return False

    def get_secure_message(self):
        """Ambil teks flash message setelah login berhasil"""
        return self.get_text(self.SECURE_MSG)