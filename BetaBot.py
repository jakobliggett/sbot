"""
Hopefully this is the more clean version of 'seleniumtesting'
"""

import selenium
from selenium import webdriver
import os

def main():
    chromedriver_path = "{}/chromedriver".format( os.path.dirname(os.path.abspath(__file__)) )
    browser = webdriver.Chrome(chromedriver_path)

if __name__ == '__main__': main()