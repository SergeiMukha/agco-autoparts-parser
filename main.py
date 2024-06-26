import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from page_parser import get_data


def get_art_page(driver: webdriver.Chrome, art: str):
    search_input = driver.find_element(By.ID, "js-site-search-input")
    search_input.send_keys(art)

    search_input.send_keys(Keys.ENTER)


def start_parser(driver: webdriver.Chrome):
    driver.get("https://parts.agcocorp.com/pl/pl")

    accept_cookie_button = driver.find_element(By.ID, "truste-consent-button")
    accept_cookie_button.click()


def main():
    driver: webdriver.Chrome = webdriver.Chrome()

    start_parser(driver=driver)

    get_art_page(driver=driver, art="3788718M1")

    time.sleep(random.randint(3, 5))

    data = get_data(driver=driver, art="3788718M1")
    print(data)

if __name__ == "__main__":
    main()




