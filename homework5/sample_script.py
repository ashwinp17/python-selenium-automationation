from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# get the path to the ChromeDriver executable
driver_path = ChromeDriverManager().install()

# create a new Chrome browser instance
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# open the url
driver.get('https://www.google.com/')

# populate search field
search = driver.find_element(By.NAME, 'q')
search.clear()
search.send_keys('table')

# wait for 4 sec
driver.implicitly_wait(4)

# click search button
driver.find_element(By.NAME, "btnK").click()

# verify search results
q_value = driver.find_element(By.NAME, "q").get_attribute("value").lower()
assert "table" in q_value, f"Expected query not in search box. value={q_value}, url={driver.current_url}"
print('Test Passed')

driver.quit()
