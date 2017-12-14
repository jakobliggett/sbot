from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import os
import AntiBotMisc
VERSION = 0.02
#Alternative 1 with each value having a variable
def get_checkoutdata(in_file):
    with open(in_file) as inp:
        data = inp.read().splitlines()
    dik = {}
    #print(data)
    for key in data:
        dik[key.split(':')[0]] = key.split(': ', 1)[-1]
    #print(dik)
    return dik

def Checkout(browser):
    #checkout_button = browser.find_element_by_css_selector(".button.checkout")
    #checkout_button.click()
    site = "file:///Users/eddieceausu/Desktop/Supreme.htm"
    browser.get(site)
    data = get_checkoutdata('checkoutdata.txt')
    for did in data:
        if did == 'order_billing_state' or 'credit_card_month' or 'credit_card_year':
            option = browser.find_element_by_id(did)
            option.click()
            option.send_keys(data[did])
            option.send_keys(Keys.ENTER)
        else:
            element = browser.find_element_by_id(did)
            if data[did] != 'N/A':
                element.click()
                AntiBotMisc.send(element, data[did])
            else: pass # DOES NOT ENTER N/A

    element = browser.find_element_by_id('order_billing_city')
    element.click()
    element.clear()
    #for i in range(30): element.send_keys(Keys.BACK_SPACE)
    element.send_keys(data['order_billing_city'])

    terms = browser.find_element_by_class_name("order_terms.checkbox")
    terms.click()
    time.sleep(2)
    terms = browser.find_element_by_name("commit")
    terms.click()

chromedriver_path = "{}/chromedriver".format( os.path.dirname(os.path.abspath(__file__)) )
browser = webdriver.Chrome(chromedriver_path)
Checkout(browser)
