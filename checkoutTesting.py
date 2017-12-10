from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import os

current_direc = os.path.dirname(os.path.abspath(__file__))
browser = webdriver.Chrome()

#Alternative 1 with each value having a variable
def get_checkoutdata(in_file):
    with open(in_file) as inp:
        data = inp.read().splitlines()
    dic = {}
    #print(data)
    for i in data:
        dic[i.split(':')[0]] = i.split(': ', 1)[-1]
    print(dic)
    return dic

def getItems():
    items = int(input('What items do you want?\nJackets\t1\ntops\t2\nsweaters\t3\nsweatshirts\t4\naccessories\t5\npants\t6\nhats\t7\nskate\t8'))
    if items == 1:
        return 'Jackets'
    if items == 2:
        return 'tops'
    if items == 3:
        return 'sweaters'
    if items == 4:
        return 'sweatshirts'
    if items == 5:
        return 'accessories'
    if items == 6:
        return 'pants'
    if items == 7:
        return 'hats'
    if items == 8:
        return 'skate'

def checkout():
        data = get_checkoutdata("checkoutdata.txt")
        browser.find_element_by_name("order[billing_name]").send_keys(data[name])
        browser.find_element_by_name("order[email]").send_keys(data[email])
        browser.find_element_by_name("order[tel]").send_keys(data[tel])
        browser.find_element_by_name("order[billing_address]").send_keys(data[address])
        browser.find_element_by_name("order[billing_zip]").send_keys(data[zipp])
        browser.find_element_by_name("order[billing_city]").send_keys(data[city])
        if(data[apt] != 'N/A'):
            browser.find_element_by_name("order[billing_address_2]").send_keys(data[apt])
        parent = browser.find_element_by_name("order[billing_state]")
        all_options = parent.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == data[state]:
                option.click()
                break
        browser.find_element_by_name("credit_card[nlb]").send_keys(data[CCN])
        browser.find_element_by_name("credit_card[rvv]").send_keys(data[CCV])
        parent = browser.find_element_by_name("credit_card[month]")
        all_options = parent.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_get_attribute("value") == data[CCM]:
                option.click()
                break
        parent = browser.find_element_by_name("credit_card[year]")
        all_options = parent.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_get_attribute("value") == data[CCY]:
                option.click()
                break
        browser.find_element_by_class_name("icheckbox_minimal").find_element_by_name("order[terms]").click()

def SupremeRoutine(buyclass):
    browser.get('http://www.supremenewyork.com/')
    #wait(1)
    shop_link = browser.find_element_by_class_name("shop_link")
    shop_link.click()
    wait()
    ##Found shop, get type
    products = getitems()
    browser.find_element_by_class_name("shop_link").click()
    

if __name__ == '__main__':
    checkout()
