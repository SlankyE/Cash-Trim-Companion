from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

print("Script started")

options = Options()
options.headless = True  # Or False to see the browser

service = Service(r"C:\Users\ksasw\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")


driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()
