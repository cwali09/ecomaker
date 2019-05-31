from driver import setup_driver
import pickle, time, os, json, csv, sys, threading

from selenium import webdriver
import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from datetime import datetime
from bs4 import BeautifulSoup


class AliExpress_Engine():
    def __init__(self, url, product_id):
        self.url = url
        self.product_id = product_id
        mode = input("Search or Analysis mode?\n").lower()
        if (mode == "search" or mode == "s"):
            print("Ok. Running Search mode...")

        elif (mode == "analysis" or mode == "a"):
            print("Ok. Running Analysis mode...")
            self.setup_soup_and_driver()



    def setup_soup_and_driver(self):
        self.driver = setup_driver()
        # self.driver.get(self.url)
        content = self.driver.page_source
        self.soup = BeautifulSoup(content, 'html.parser')
        print(self.has_epacket_shipping())

    def get_total_num_reviews(self):
        self.soup.find('')
    
    def has_epacket_shipping(self):
        shipping_company = self.soup.find('span', {'id': 'j-shipping-company'}).text
        if (not shipping_company or shipping_company == ""):
            return False
        return True