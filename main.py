import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


marks_image_links = {
    "https://parts.agcocorp.com/medias/MF-logo-new.png?context=bWFzdGVyfHJvb3R8MTA3NjV8aW1hZ2UvcG5nfGg3YS9oYjMvOTA3NDkxNjE2MzYxNC5wbmd8OTkwMDNmNzNjOTA5MTdhNWRlYzEwMTM1MzdkY2Q3MjZiMzdiZDEzZjMwOWE1NzAzYzhiOGJiMzc3NTgxZDBlYw": "Massey Ferguson",
    "https://parts.agcocorp.com/medias/?context=bWFzdGVyfHJvb3R8MzkyOXxpbWFnZS9wbmd8aDYyL2hkOS84ODA2MjM4MDkzMzQyLnBuZ3xjMDJjMmYzYzM0YWIyODU0YzJjZWUzZjA4YzFlN2IzYzVkOTMwNzJhYTIzY2IxOTMxOTAyNjIwMmNhMjUyY2Vk": "Fendt",
    "https://parts.agcocorp.com/medias/CH-logo-blk-140-50.png?context=bWFzdGVyfHJvb3R8MTU3MHxpbWFnZS9wbmd8aDM2L2hlNS84OTQyMjIzNjU0OTQyLnBuZ3w1YmMzMWJjN2Y5YWJlZjYxNTdiMDFiYTAzNzNmZDVmOTg2YjBiMWEyNmMwYmJjMzdkZmE4N2ZjOWEwYzhkNmNl": "Challenger",
    "https://parts.agcocorp.com/medias/?context=bWFzdGVyfHJvb3R8NTc3OXxpbWFnZS9wbmd8aGJkL2g5Ny84ODA2MjM4MTU4ODc4LnBuZ3w0Y2JkNDAzZGUzMDliYmU2OTU3N2U3Y2ZlOGMxNTU0ODRkYTA4YThlNzFjOWQyODVmMWJlZDk1M2Q2NDc2ZTlh": "Valtra",
    "https://parts.agcocorp.com/medias/Gleaner-140-50.png?context=bWFzdGVyfHJvb3R8MTM0MnxpbWFnZS9wbmd8aDc2L2gzOS84OTQyOTA3Nzg1MjQ2LnBuZ3w1OTE1ZTMwZWY1ZTM3OTU5N2Q1NmU1YjM4OTQ2MjE0YmYxZDlmZGI1OWFlMmZmOTE4ZjYyOTU5YThjZWM1MGJk": "Gleaner"
}


def start_parser(driver: webdriver.Chrome):
    accept_cookie_button = driver.find_element(By.ID, "truste-consent-button")
    accept_cookie_button.click()


def get_data(driver: webdriver.Chrome):
    marks_button = driver.find_element(By.CLASS_NAME, "nav-pills").find_element(By.CLASS_NAME, "d-sm-block")
    marks_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "oemTextDiv")))

    marks_container = driver.find_element(By.ID, "suitable-for")

    models_full_string = ""
    marks = ""

    mark_boxes = marks_container.find_elements(By.CLASS_NAME, "sections")

    for box in mark_boxes:
        
        mark_image_link = box.find_element(By.TAG_NAME, "img").get_attribute("src")
        mark_name = marks_image_links[mark_image_link] or None
        if mark_name:
            if marks == "":
                marks = mark_name
            else:
                marks+=f", {mark_name}"

        models = box.find_element(By.CLASS_NAME, "oemTextDiv") or None
        if models:
            if models_full_string == "":
                models_full_string = models.text
            else:
                models_full_string+=f", {models.text}"

    img_link = driver.find_element(By.CLASS_NAME, "lazyOwl").get_attribute("src")
    download_photo(img_link)
    
    return {
        "marks": marks,
        "models": models_full_string
    }


def download_photo(link):
    img_data = requests.get(link).content
    with open('images/image_test.jpg', 'wb') as handler:
        handler.write(img_data)


def main():
    driver: webdriver.Chrome = webdriver.Chrome()

    driver.get("https://parts.agcocorp.com/pl/pl/p/nakr%C4%99tka-specjalna/acw0943650?text=D25700322")

    start_parser(driver=driver)

    data = get_data(driver=driver)
    print(data)

if __name__ == "__main__":
    main()




