#### For now default to mozilla
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.service as service
from selenium import webdriver
import os

def setup_driver():
    # Set Firefox driver
    # driver = webdriver.Firefox()

    # Set headless Chrome Driver
    chrome_options = Options()
    chrome_options.set_headless(headless=True)
    
    # For Windows OS
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options = chrome_options)
    # For Mac/Linux OS
    #driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), chrome_options = chrome_options)

    return driver

if __name__ == '__main___':
    pass    