from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from settings import ETORO_USERNAME, ETORO_PASSWORD, CHROMEDRIVER_PATH

username = ETORO_USERNAME
password = ETORO_PASSWORD

driver = webdriver.Chrome("{}/{}".format(Path().absolute(), CHROMEDRIVER_PATH))
driver.get("https://www.etoro.com/login")
driver.maximize_window()

wait = WebDriverWait(driver, 10)

username_el = wait.until(ec.visibility_of_element_located((By.ID, "username")))
password_el = wait.until(ec.visibility_of_element_located((By.ID, "password")))
remember_me_el = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#login-remember-me label")))
login_button_el = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "button")))

ActionChains(driver).move_to_element(username_el).click().send_keys(username).perform()
time.sleep(0.5)
ActionChains(driver).move_to_element(password_el).click().send_keys(password).perform()
time.sleep(0.5)
ActionChains(driver).move_to_element(remember_me_el).click().perform()
time.sleep(0.5)
ActionChains(driver).move_to_element(login_button_el).click().perform()
time.sleep(0.5)

# Wait to get logged in
wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))

# driver.close()
