import logging
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from settings import WEBDRIVER_PATH


logger = logging.getLogger(__name__)


WAIT_BETWEEN_USER_ACTIONS = 0.5  # Seconds between any user action


def post_status(username, password, message):
    logger.info("Opening Chrome...")
    driver = webdriver.Chrome("{}/{}".format(Path().absolute(), WEBDRIVER_PATH))
    driver.get("https://www.etoro.com/login")
    driver.maximize_window()

    wait = WebDriverWait(driver, 5)

    # Login screen elements
    username_el = wait.until(ec.visibility_of_element_located((By.ID, "username")))
    password_el = wait.until(ec.visibility_of_element_located((By.ID, "password")))
    remember_me_el = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#login-remember-me label")))
    login_button_el = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "button")))

    # Perform the actions
    logger.info("Trying to log in eToro...")
    ActionChains(driver).move_to_element(username_el).click().send_keys(username).perform()
    time.sleep(WAIT_BETWEEN_USER_ACTIONS)
    ActionChains(driver).move_to_element(password_el).click().send_keys(password).perform()
    time.sleep(WAIT_BETWEEN_USER_ACTIONS)
    ActionChains(driver).move_to_element(remember_me_el).click().perform()
    time.sleep(WAIT_BETWEEN_USER_ACTIONS)
    ActionChains(driver).move_to_element(login_button_el).click().perform()
    time.sleep(WAIT_BETWEEN_USER_ACTIONS)

    # Wait to get logged in and open the "write a post" dialog
    wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
    post_status_el = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "header a[data-feed-create-post-button]")))
    logger.info("Logged in eToro successfully.")
    ActionChains(driver).move_to_element(post_status_el).click().perform()
    logger.info('Clicked on "Write a post" button.')
    time.sleep(WAIT_BETWEEN_USER_ACTIONS)

    # Now, send_keys() doesn't support emojis and eToro's textarea validation sucks, so let's do some trickery here...
    status_textarea_el = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".uidialog .w-share-modal textarea[data-feed-form-link]")))
    logger.info('"Write a post" dialog opened successfully, textarea targeted.')
    message = message.replace('"', '\\"').replace("\n", "&#13;&#10;")
    driver.execute_script(f'document.querySelector(".uidialog .w-share-modal textarea[data-feed-form-link]").value = "{message}";')
    ActionChains(driver).move_to_element(status_textarea_el).click().send_keys(" ").send_keys(Keys.BACKSPACE).perform()
    time.sleep(WAIT_BETWEEN_USER_ACTIONS)
    status_button_el = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".uidialog .w-share-modal button")))
    ActionChains(driver).move_to_element(status_button_el).click().perform()
    logger.info("Post published successfully.")

    driver.close()
