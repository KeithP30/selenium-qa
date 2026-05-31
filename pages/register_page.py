# pages/register_page.py
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
    # FIX BUG-7: Tambah locator EMAIL yang sebelumnya tidak ada
    EMAIL            = (By.ID, 'userEmail')
    REGISTER_BTN     = (By.ID, 'register')
    SUCCESS_MSG      = (By.ID, 'output')
    ERROR_MSG        = (By.CSS_SELECTOR, '.field-error, [class*="error"]')

    # ── Actions ───────────────────────────────────────
    def navigate(self):
        self.open(self.URL)

    # FIX BUG-7: Tambah self.type(self.EMAIL, email) agar field email terisi
    def fill_form(self, first_name='', last_name='', username='',
                  password='', confirm_password='', email=''):
        if first_name:        self.type(self.FIRST_NAME, first_name)
        if last_name:         self.type(self.LAST_NAME, last_name)
        if username:          self.type(self.USERNAME, username)
        if password:          self.type(self.PASSWORD, password)
        if confirm_password:  self.type(self.CONFIRM_PASSWORD, confirm_password)
        if email:             self.type(self.EMAIL, email)

    def submit(self):
        self.click(self.REGISTER_BTN)

    # ── Assertions ────────────────────────────────────
    def is_registration_successful(self):
        return self.is_visible(self.SUCCESS_MSG)

    def is_error_shown(self):
        return self.is_visible(self.ERROR_MSG)