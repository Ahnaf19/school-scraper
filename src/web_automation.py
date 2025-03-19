from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger as log

from .scraper import get_data

def automation() -> pd.DataFrame:
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Remove to see browser actions
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open the page
    driver.get("https://www.ghsa.net/school-directory")

    # Wait for the dropdown to load
    wait = WebDriverWait(driver, 10)

    # Reading school names
    with open("data/school_names.txt", "r", encoding="utf-8") as file:
        school_names = [line.strip() for line in file.readlines()]
    
    data = []            

    for i in range(len(school_names)):
        log.info(f"{i}")
        select_element = wait.until(EC.presence_of_element_located((By.ID, "edit-dropdown")))

        # Click the dropdown
        select_element.click()

        # Type "school_name" and press ARROW_DOWN & ENTER
        select_element.send_keys(Keys.ARROW_DOWN)
        select_element.send_keys(Keys.ENTER)

        # Wait until the table with class 'directory-table' loads
        table_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "directory-table")))

        # Re-locate the element just before parsing it to avoid stale element
        table_element = driver.find_element(By.CLASS_NAME, "directory-table")

        # Parse the table HTML with BeautifulSoup
        soup = BeautifulSoup(table_element.get_attribute("outerHTML"), "html.parser")

        # Extract the data from the table
        per_school_data = get_data(soup)
        
        data.append(per_school_data)
        
    df = pd.DataFrame(data)
    
    # Save the DataFrame as a CSV file in the data/ directory
    df.to_csv("data/school_data.csv", index=False, encoding="utf-8")
    
    # Quit the driver
    driver.quit()
        
    return df


if __name__ == "__main__":
    # print(automation())
    automation()