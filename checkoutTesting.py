from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import os
import seleniumtesting
VERSION = 0.02
#Alternative 1 with each value having a variable
def get_checkoutdata(in_file):
    with open(in_file) as inp:
        data = inp.read().splitlines()
    dic = {}
    #print(data)
    for key in data:
        dic[key.split(':')[0]] = key.split(': ', 1)[-1]
    #print(dic)
    return dic

def checkout(browser): # needs to be tested!!!!
    data = get_checkoutdata('checkoutdata.txt'))
    for did in data:
        if did == 'order_billing_state' || 'credit_card_month' || 'credit_card_year':
            option = browser.find_element_by_id(did)
            option.click()
            option.send_keys(data[did])
            option.send_keys(Keys.ENTER)
        else:
            element = browser.find_element_by_id(did)
            element.click()
            element.send_keys(data[did])
    print("Wait 3 seconds before submitting")
