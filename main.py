import pickle, time, os, json, csv, sys

from selenium import webdriver
import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from datetime import datetime
from bs4 import BeautifulSoup

from aliexpress_engine import AliExpress_Engine


if __name__ == '__main__':
    raw_aliexpress_url = sys.argv[1]
    product_id = sys.argv[2]
    
    #wish_url = sys.argv[1]
    #ebay_url = 
    #amazon_url = 
    AliExpress_Engine(raw_aliexpress_url, product_id)      





