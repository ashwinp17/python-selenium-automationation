import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver_path = ChromeDriverManager().install()
print("ChromeDriver installed at:", driver_path)

driver = webdriver.Chrome(service=Service(driver_path))
driver.get("https://www.google.com")
driver.implicitly_wait(5)
driver.quit()




