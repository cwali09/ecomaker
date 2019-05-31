import pickle, time, os, json, csv, sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
#import scrapy
#from mobilenium import mobidriver

from aliexpress_engine import AliExpress_Engine
from driver import setup_driver

import pickle
from selenium import webdriver


def filter_name(unfiltered_name):
    filtered_name = ''
    for char in unfiltered_name:
        val = ord(char)
        if ((val >= 65 and val <= 90) or (val >= 97 and val <= 122)):
            filtered_name += char
    return filtered_name

def filter_names(unfiltered_names):
    filtered_names = list()
    for unfiltered_name in unfiltered_names:
        filtered_names.append(filter_name(unfiltered_name))
    return filtered_names

def get_previous_sellers():
    prev_loaded_sellers = set()
    file = open("prev_contacted_sellers.txt", 'r')
    line = file.readline()
    while (line):
        print(line)
        seller_name = filter_name(line)
        prev_loaded_sellers.add(seller_name)
        line = file.readline()
    file.close()
    return prev_loaded_sellers
#hengshuihongzhumedicaltechnologycoltd
#grahopenewmaterialstechnologiesinc
#hengshuigangshengmedicalinstrumentscoltd
#zhongshanchukuangtextilecoltd

def save_seller_to_file(seller):
    file = open("prev_contacted_sellers.txt", 'a+b')
    seller = seller+'\n'
    print("Saving {seller} to file...".format(seller=seller))
    file.write(seller)
    file.close()

username = os.environ.get('ECOMAKER_ALIBABA_USER_NAME_TOKEN')
password = os.environ.get('ECOMAKER_ALIBABA_PASS_TOKEN')

MESSAGE = 'Hello,\n\nI am Nick, a representative of Leisik Co. We are trying to find a seller to do a partnership with in the long-term and want to expand into different markets. Could you tell me what your Top 5 best selling products are, and if you are the manufacturer of those products?\n\nThank you,\nNick'

search_url = 'https://www.alibaba.com//trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText='

capabilities = DesiredCapabilities.FIREFOX
capabilities["marionette"] = True
driver = webdriver.Firefox(capabilities=capabilities)
keyword = sys.argv[1]

# Login to Alibaba
try:
    driver.get('https://passport.alibaba.com/icbu_login.htm?tracelog=hd_signin') 
    driver.find_element_by_name('loginId').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('submit-btn').click()

    # Wait for some random element on the home Alibaba page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-banner")))
except:
    input("Manual user login is required. Press any key when you're done logging in to continue.")

#keyword = input("Enter required keyword: ")
driver.get(search_url + keyword)
response = requests.get(search_url + keyword)

seller_set = set()

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

prev_loaded_sellers = get_previous_sellers()
filtered_names = set()
print("Previously loaded sellers:\n {prev_loaded_sellers}".format(prev_loaded_sellers=prev_loaded_sellers))

if (len(prev_loaded_sellers) != 0):
    for prev_seller in prev_loaded_sellers:
        print(prev_seller)
        prev_seller = filter_name(prev_seller)
        filtered_names.add(prev_seller)

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "list-item__minisite-link")))
items = soup.find_all("div", {"data-role" : "item"})

index = 1
file = open("prev_contacted_sellers.txt", 'w')

for item in items:    
    contact_xpath = '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[7]/div[1]/div[{index}]/div/div[2]/div[2]/div/a[1]'.format(index=index)
    name_xpath = '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[7]/div[1]/div[{index}]/div/div[1]/div[3]/div/a'.format(index=index)
    manufacturer_page_xpath = '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[7]/div[1]/div[{index}]/div/div[1]/div[3]/div/a'.format(index=index)

    manufacturer_page_contact_xpath = '/html/body/div[7]/div[2]/div[1]/a'
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "list-item__minisite-link")))

        name_unfiltered = driver.find_element_by_xpath(name_xpath).text
        filtered_name = filter_name(name_unfiltered).lower()
        product_search_window = driver.current_window_handle

        if ((filtered_name in filtered_names) == False):

            filtered_names.add(filtered_name)
            unfiltered_manf_page_link = driver.find_element_by_xpath(manufacturer_page_xpath)
            manf_page_url = unfiltered_manf_page_link.get_attribute("href").replace('#top-nav-bar', '')
            driver.get(manf_page_url)
            print(manf_page_url)

            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "J-ali-sidebar")))
                
            manf_page_contact_url = driver.find_element_by_xpath(manufacturer_page_contact_xpath).get_attribute("href")
            driver.get(manf_page_contact_url)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inquiry-content")))
            inquiry_text_area = driver.find_element_by_id("inquiry-content")
            inquiry_text_area.send_keys(MESSAGE)

            send_inquiry_btn = driver.find_element_by_class_name("ui2-button.ui2-button-default.ui2-button-primary.ui2-button-large")
            
            # Writing to file
            seller = filtered_name+'\n'
            print("Saving {seller} to file...".format(seller=seller))
            file.write(seller)

            #send_inquiry_btn.click()
            sleep(1)
            driver.get(search_url + keyword)
    except NoSuchElementException:
        print("Selenium cannot find an element. Saving emailed sellers to file, and incrementing index counter to continue the program.")
        for seller in filtered_names:
            file.write(seller + '\n')
        driver.get(search_url + keyword)
        index += 1
    except KeyboardInterrupt:
        print("Keyboard interrupt. Saving all emailed sellers to file...") 
        for seller in filtered_names:
            file.write(seller+'\n')
        exit(1)
        


    index += 1

print(filtered_names)
file.close()




