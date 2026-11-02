"""Start the LMS first; LMS_BASE_URL defaults to the Docker port mapping."""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = pytest.mark.selenium
BASE_URL = os.environ.get("LMS_BASE_URL", "http://localhost:8080").rstrip("/")


@pytest.fixture
def driver():
    browser = os.environ.get("LMS_BROWSER", "chrome").lower()
    if browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--headless=new")
        instance = webdriver.Edge(options=options)
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        instance = webdriver.Chrome(options=options)
    try:
        yield instance
    finally:
        instance.quit()


def submit_login(driver, username, password):
    driver.get(BASE_URL + "/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
    return wait


def test_successful_login(driver):
    username = os.environ.get("LMS_USERNAME", "admin")
    wait = submit_login(driver, username, os.environ.get("LMS_PASSWORD", "library123"))
    wait.until(EC.url_to_be(BASE_URL + "/dashboard"))
    welcome = wait.until(EC.visibility_of_element_located((By.ID, "welcome")))
    assert welcome.text == f"Welcome, {username}"


def test_invalid_credentials(driver):
    wait = submit_login(driver, os.environ.get("LMS_USERNAME", "admin"), "incorrect-password")
    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='alert']")))
    assert error.text == "Invalid username or password"
    assert driver.current_url.rstrip("/") == BASE_URL
