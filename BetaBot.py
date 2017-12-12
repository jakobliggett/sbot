"""
Hopefully this is the more clean version of 'seleniumtesting'

"""

import selenium
from selenium import webdriver
import os, time

def LoadConfiguration(cfile):
    config = {}
    with open(cfile, 'r') as f:
        text = f.readlines()
        for line in text:
            split_line = line.split(':')
            config_category = split_line[0]
            config_num = split_line[1]
            config[config_category] = config_num
    return config

def FindProducts(browser, site):
    #browser.get("http://www.supremenewyork.com/shop/all")
    browser.get(site)
    unsorted_products = browser.find_elements_by_xpath("""//*[@id="container"]/article[*]/div/a""")
    #"""//*[@id="container"]/article[88]/div/a"""
    products = []
    for product in unsorted_products:
        href_unsorted = product.get_attribute('href')
        href_split = href_unsorted.split('/')
        try:
            sold_out_element = product.find_element_by_class_name("sold_out_tag")
        except Exception: ##I put this in here so it only triggers if
            category = (href_split[4])
            link = ("{}/{}/{}".format(site, href_split[5], href_split[6]))
            products.append([category, link])
    return products


def ProductsToCart(browser, products, config):
    for product in products:
        category = product[0]
        link = product[1]
        browser.get(link)
        time.sleep(1) ##Testing only
        browser.back()



def main():
    #site = "http://webcache.googleusercontent.com/search?q=cache:http://www.supremenewyork.com/shop/all"
    site = "http://www.supremenewyork.com/shop/all"
    chromedriver_path = "{}/chromedriver".format( os.path.dirname(os.path.abspath(__file__)) )
    browser = webdriver.Chrome(chromedriver_path)
    products = FindProducts(browser, site)
    print(products)
    #config = LoadConfiguration('config.txt') ##Change this?
    config = []
    ProductsToCart(browser, products, config)
    time.sleep(20) ##Just for debug so chrome doesn't eat all the ram
    browser.close()

if __name__ == '__main__': main()