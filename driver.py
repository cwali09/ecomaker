#### For now default to mozilla
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.service as service
from selenium import webdriver

def setup_driver():
    driver = webdriver.Firefox()
    return driver

if __name__ == '__main___':
    pass    