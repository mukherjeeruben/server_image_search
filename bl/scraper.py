from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from bl.preprocess_data import preprocess_text
import time

import config


def scraper(search_cr):
    dataset = list()
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    selection_criterias = [search_cr]
    for selection_criteria in selection_criterias:
        link_set = get_image_data(selection_criteria, config.MAX_IMAGE, driver)
        dataset.extend(link_set)
    driver.quit()
    return dataset


def get_image_data(selection_criteria, max_images_to_fetch, web_driver):
    image_data = list()
    web_driver.get(config.SEARCH_URL.format(q=selection_criteria))
    thumbnail_results = web_driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
    for index in range(max_images_to_fetch):
        try:
            thumbnail_results[index].click()
            time.sleep(config.SLEEP_BETWEEN_INTERACTIONS)
        except Exception as exmsg:
            continue
        actual_images = web_driver.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                if actual_image.accessible_name != "":
                    if '?crop' in actual_image.get_attribute('src'):
                        image_url = actual_image.get_attribute('src').split('?crop', 1)[0]
                    else:
                        image_url = actual_image.get_attribute('src')
                    alt_text = preprocess_text(actual_image.accessible_name)
                    image_data.append({'title': alt_text, 'url': image_url})
    return image_data