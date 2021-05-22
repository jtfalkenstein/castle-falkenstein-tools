import json
import random
from functools import wraps
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

GENERATOR_URL_TEMPLATE = 'https://www.fantasynamegenerators.com/{name_type}.php'
CACHE_FILE_PATH = Path('name_cache.json')

def cache_with_json(func):
    @wraps(func)
    def wrapper(first_arg, *rest):
        loaded = get_cache()
        items: list = loaded.get(first_arg)
        if not items:
            items = func(first_arg, *rest)
            loaded[first_arg] = items
            
        
        return items
    return wrapper

@cache_with_json            
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

def get_cache():
    if not CACHE_FILE_PATH.exists():
        CACHE_FILE_PATH.touch()
        CACHE_FILE_PATH.write_text('{}')
    with CACHE_FILE_PATH.open(mode='r') as f:
        loaded = json.load(f)
    
    return loaded

def write_cache(cache_dict):
    with CACHE_FILE_PATH.open(mode='w') as f:
        json.dump(cache_dict, f, indent=4, ensure_ascii=False)

def purge_name_from_cache(name_type, name):    
    loaded = get_cache()
    loaded[name_type].remove(name)
    write_cache(loaded)


def generate_random_name(name_types: List[str]):
    name_type = random.choice(name_types)
    random_names = generate_names(name_type)
    selected_random_name = random.choice(random_names)
    purge_name_from_cache(name_type, selected_random_name)
    return selected_random_name.strip()
