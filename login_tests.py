# -*- coding: utf-8 -*-
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver, login, passwd, click=None):
    driver.find_element_by_id('mat-input-0').send_keys(login)
    password = driver.find_element_by_id('mat-input-1')
    password.send_keys(passwd)
    if click is not None:
        print driver.find_element_by_xpath("//span[contains(text(),'Login')]").click()
    password.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, 1).until(EC.url_contains('admin'))
        return 1
    except:
        return 'Page is not loaded'
    finally:
        driver.close()


@pytest.fixture()
def resource_setup():
    driver = Chrome()
    driver.get('http://127.0.0.1:8000/login')
    return driver

def test_empty_password(resource_setup):
    #Поле password остается пустым
    assert login(resource_setup, 'admin', '') != 1

def test_correct_login_by_enter(resource_setup):
    #Авторизация, пользователь существует, нажимается клавиша enter для входа
    assert login(resource_setup, 'admin', 'admin') == 1

def test_uncrorrect_login(resource_setup):
    #Попытка авторизации другим пользователем
    assert login(resource_setup,'otheruser', 'admin') != 1

def test_uncorrect_password(resource_setup):
    #Существующий пользователь с неправильным паролем
    assert login(resource_setup,'admin', 'otherpasswd') != 1

def test_case_sensitivity_login(resource_setup):
    #Проверка на регистрозависимость в поле логин
    assert login(resource_setup,'Admin', 'admin') != 1

def test_correct_login_by_click(resource_setup):
    #Авторизация, пользователь существует, нажимается кнопка Login для входа
    assert login(resource_setup,'admin', 'admin', 'click') == 1

