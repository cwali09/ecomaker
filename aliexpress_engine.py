from driver import setup_driver
import pickle, time, os, json, csv, sys

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
        self.driver = setup_driver()

        mode = input("Search or Analysis mode?\n").lower()
        if (mode == "search"):
            print("Ok. Running Search mode...")

        elif (mode == "analysis"):
            print("Ok. Running Analysis mode...")
            self.run_product_analysis()


    def run_product_analysis(self):
        self.driver.get(self.url)
        self.content = self.driver.page_source
    