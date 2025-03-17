from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Set up Selenium WebDriver (VISIBLE browser)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Remove to see browser actions
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the page
driver.get("https://www.ghsa.net/school-directory")

# Wait for the dropdown to load
wait = WebDriverWait(driver, 10)
select_element = wait.until(EC.presence_of_element_located((By.ID, "edit-dropdown")))

# Click the dropdown
select_element.click()

# Type "Alcovy High School" and press ENTER
select_element.send_keys("Alcovy High School")
select_element.send_keys(Keys.ENTER)

# Wait until the table with class 'directory-table' loads
table_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "directory-table")))

# Print only the table HTML
print(table_element.get_attribute("outerHTML"))

# Quit the driver
driver.quit()
