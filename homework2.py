#Amazon logo
//i[contains(@class,'a-icon-logo')]

#Email field
//input[@id="ap_email_login"]

#Continue button
//input[@class="a-button-input"]

#Conditions of use link
//a[normalize-space()='Conditions of Use']

#Privacy Notice link
//a[normalize-space()='Privacy Notice']

#Need help link
//a[normalize-space()='Need help?']

#Forgot your password link
//a[contains(normalize-space(),'Forgot your password')]

#Other issues with Sign-In link
//a[contains(normalize-space(),'Other issues')]

#Create your Amazon account button
//a[@id='createAccountSubmit']



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.target.com/")

sleep(2)

driver.find_element(By.ID, "account-sign-in").click()

sleep(2)
driver.find_element(By.XPATH, "//button[@data-test='accountNav-signIn']").click()

sleep(2)
actual_text = driver.find_element(By.XPATH, "//h1[normalize-space()='Sign in or create account']").text
actual_text = driver.find_element(By.XPATH, "//button[contains(@class,'styles_ndsBaseButton__') and @type='button']").text

driver.quit()