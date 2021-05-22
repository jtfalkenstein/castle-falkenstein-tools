from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
from typing import List
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


GENERATOR_URL_TEMPLATE = 'https://www.fantasynamegenerators.com/{name_type}.php'

def generate_names(name_type):
    url = GENERATOR_URL_TEMPLATE.format(name_type=name_type)
    chrome_driver = ChromeDriverManager().install()

    options = Options()
    options.headless = True
    chrome = webdriver.Chrome(chrome_driver, chrome_options=options)

    try:
        timeout = 5
        chrome.get(url)
        element_present = EC.presence_of_element_located((By.ID, 'result'))
        WebDriverWait(chrome, timeout).until(element_present)
        result = chrome.find_element_by_id('result')
        return result.text.splitlines()
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        chrome.quit()

def generate_random_name(name_types: List[str]):
    name_type = random.choice(name_types)
    random_names = generate_names(name_type)
    selected_random_name = random.choice(random_names)
    return selected_random_name.strip()