# tests/test_register_ddt.py
import pytest
from pages.register_page import RegisterPage
from tests.conftest import load_csv

# Muat semua data dari CSV saat file ini di-import
REGISTER_DATA = load_csv('register_data.csv')

class TestRegisterDDT:

    @pytest.mark.parametrize(
        'row',
        REGISTER_DATA,
        ids=[row['description'] for row in REGISTER_DATA]
    )
    def test_register_from_csv(self, driver, row):
        """
        DDT: Test registrasi dijalankan untuk setiap baris di CSV.
        Screenshot otomatis diambil oleh hook di conftest.py saat FAIL.
        """
        page = RegisterPage(driver)
        page.navigate()
        page.fill_form(
            username         = row['username'],
            password         = row['password'],
            confirm_password = row['confirm_password'],
            first_name       = row['first_name'],
            last_name        = row['last_name'],
            email            = row['email']
        )
        page.submit()

        desc = row['description']

        if row['expected'] == 'PASS':
            assert page.is_registration_successful(), \
                f'[{desc}] Registrasi seharusnya BERHASIL'
        else:
            assert page.is_error_shown(), \
                f'[{desc}] Registrasi seharusnya GAGAL dan muncul pesan error'