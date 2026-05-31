from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegisterPage(BasePage):
    URL = 'https://demoqa.com/register'

    # ── Locators ──────────────────────────────────────
    FIRST_NAME       = (By.ID, 'firstname')
    LAST_NAME        = (By.ID, 'lastname')
    USERNAME         = (By.ID, 'userName')
    PASSWORD         = (By.ID, 'password')
    CONFIRM_PASSWORD = (By.ID, 'confirm-password')
    REGISTER_BTN     = (By.ID, 'register')
    SUCCESS_MSG      = (By.ID, 'output')     # Muncul saat registrasi berhasil
    ERROR_MSG        = (By.CSS_SELECTOR, '.field-error, [class*="error"]')

    # ── Actions ───────────────────────────────────────
    def navigate(self):
        self.open(self.URL)

    def fill_form(self, username, password, confirm_password,
                first_name, last_name, email=''):
        if first_name:    self.type(self.FIRST_NAME, first_name)
        if last_name:     self.type(self.LAST_NAME, last_name)
        if username:      self.type(self.USERNAME, username)
        if password:      self.type(self.PASSWORD, password)
        if confirm_password: self.type(self.CONFIRM_PASSWORD, confirm_password)

    def submit(self):
        self.click(self.REGISTER_BTN)

    # ── Assertions ────────────────────────────────────
    def is_registration_successful(self):
        return self.is_visible(self.SUCCESS_MSG)

    def is_error_shown(self):
        return self.is_visible(self.ERROR_MSG)