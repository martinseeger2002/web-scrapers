import json
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("https://doggy.market/nfts/rise-of-skulls")
    return driver

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait to load the new content
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image: {url}")

def scrape_items(driver, output_file):
    items = []
    total_items_scraped = 0

    while True:  # Use a loop to navigate through pagination
        scroll_to_bottom(driver)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".listing-nft"))
        )

        item_elements = driver.find_elements(By.CSS_SELECTOR, ".listing-nft")
        for item in item_elements:
            # Scroll into view and add wait time
            driver.execute_script("arguments[0].scrollIntoView(true);", item)
            time.sleep(1)
            try:
                item.click()
            except ElementClickInterceptedException:
                time.sleep(1)
                driver.execute_script("arguments[0].click();", item)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".dogescription-title"))
            )

            inscription_id = driver.find_element(By.CSS_SELECTOR, ".details-value").text
            name = driver.find_element(By.CSS_SELECTOR, ".dogescription-title").text

            # Scrape all traits
            traits = {}
            trait_badges = driver.find_elements(By.CSS_SELECTOR, ".attr-badge")
            for badge in trait_badges:
                trait_name = badge.find_element(By.CSS_SELECTOR, ".attr-name").text
                trait_value = badge.find_element(By.CSS_SELECTOR, ".attr-value").text
                traits[trait_name] = trait_value

            # Scrape the image URL
            image_url = driver.find_element(By.CSS_SELECTOR, ".nft-pic.dogescription-content.dogescription-picture").get_attribute("src")
            file_name = f"{name}.jpg"
            download_image(image_url, file_name)

            item_data = {
                "inscriptionId": inscription_id,
                "name": name,
                "attributes": traits,
                "image": file_name
            }

            items.append(item_data)
            total_items_scraped += 1
            print(f"Total items scraped: {total_items_scraped}")

            # Append the new item to the JSON file
            with open(output_file, 'r+') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                data.append(item_data)
                file.seek(0)
                json.dump(data, file, indent=4)

            driver.back()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".listing-nft"))
            )

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-item.next:not([aria-disabled='true']) button")
            next_button.click()
        except NoSuchElementException:
            break  # Exit loop if no next button is active

    return items

def main():
    output_file = 'rise-of-skulls.json'
    # Initialize the JSON file if it doesn't exist
    with open(output_file, 'w') as file:
        json.dump([], file)

    driver = setup_driver()
    scrape_items(driver, output_file)
    print("Items scraped and saved to JSON.")
    driver.quit()

if __name__ == "__main__":
    main()
