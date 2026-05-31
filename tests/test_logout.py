# tests/test_logout.py
import pytest
# FIX BUG-5: Import By langsung di sini, bukan pakai __import__() di dalam kode
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogout:

    def test_logout_after_valid_login(self, driver):
        """
        TC-LOGOUT-001
        Skenario : User login berhasil → logout → kembali ke halaman login
        Priority : HIGH
        Teknik   : EP (alur valid end-to-end)
        """
        # STEP 1: Login
        login = LoginPage(driver)
        login.login('tomsmith', 'SuperSecretPassword!')

        # STEP 2: Verifikasi berhasil masuk ke dashboard
        dashboard = DashboardPage(driver)
        assert dashboard.is_on_dashboard(), \
            'Setelah login valid, user harus berada di Dashboard (Secure Area)'

        # STEP 3: Logout
        dashboard.logout()

        # STEP 4: Verifikasi kembali ke halaman Login
        login_page_again = LoginPage(driver)
        assert '/login' in driver.current_url, \
            'Setelah logout, user harus diarahkan kembali ke halaman Login'
        assert login_page_again.is_visible(login_page_again.LOGIN_BTN), \
            'Tombol Login harus tampil setelah logout'

    def test_dashboard_not_accessible_after_logout(self, driver):
        """
        TC-LOGOUT-002
        Skenario : Setelah logout, akses langsung ke /secure harus ditolak
        Priority : MEDIUM
        Teknik   : EP (partisi invalid — akses tanpa session)
        """
        # Login dulu, lalu logout
        login = LoginPage(driver)
        login.login('tomsmith', 'SuperSecretPassword!')
        dashboard = DashboardPage(driver)
        dashboard.logout()

        # Paksa akses /secure langsung
        driver.get('https://the-internet.herokuapp.com/secure')

        # FIX BUG-5: Pakai By yang sudah di-import di atas, bukan __import__()
        assert '/secure' not in driver.current_url or \
               dashboard.is_visible((By.CSS_SELECTOR, '.flash.error')), \
               'Dashboard tidak boleh diakses setelah logout'