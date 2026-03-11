from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from getpass import getpass

fd_login_url = "https://sizeup.firstduesizeup.com/auth/signin-v2"
visual = True
firefox_binary = r"/usr/bin/firefox"

# input username and password for FirstDue
username = input("FirstDue username: ")
password = getpass("Password: ")

# set up webdriver
options = Options()
options.binary_location = firefox_binary
if visual == False:
    options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# fetch login page
driver.get(fd_login_url)

# input username & click
username_box = driver.find_element(By.ID, "email")
username_box.send_keys(username)
driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]').click()

# import password and authenticate
password_box = driver.find_element(By.ID, "password")
password_box.send_keys(password)
driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]').click()

# Close the browser
driver.quit()