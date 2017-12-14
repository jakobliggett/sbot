"""
Hopefully this is the more clean version of 'seleniumtesting'

"""

import selenium
from selenium import webdriver
import os, time
from selenium.webdriver.common.keys import Keys
import AntiBotMisc

def LoadConfiguration(cfile):
    config = {}
    with open(cfile, 'r') as f:
        text = f.readlines()
        for line in text:
            line = line.rstrip()
            split_line = line.split(':')
            config_category = split_line[0]
            config_num = float(split_line[1])
            config[config_category] = config_num
    print(config)
    return config

def FindProducts(browser, site):
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
    current_cart_value = 0
    for product in products:
        category = product[0]
        link = product[1]
        browser.get(link)
        try:
            product_name = browser.find_element_by_class_name("protect").text
            product_price = float((browser.find_element_by_class_name("price").text[1:]).replace(',', '')) ##Strips dollar sign and converts to int
            print(product_name, product_price)
        except:
            product_name = 'N/A'
            product_price = 0

        try:
            add_to_cart = browser.find_element_by_css_selector("input.button")
            if ((current_cart_value+product_price) < config['max_cart']) and (0 < product_price <= config[category]):
                add_to_cart.click()
                print('\nBuying {}, current cart:{}, cart after this: {}'.format(product_name, current_cart_value, current_cart_value+product_price))
                current_cart_value += product_price
            if (config['max_cart']-current_cart_value) <= config['max_cart']*0.2: ##if cart is within 20% of max checkout early
                break ##Cart full, maxed on price
        except:
            pass
        time.sleep(0.2) ##Is this necessary? # No
        browser.back()
    print('CART FULL!')

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
    checkout_button = browser.find_element_by_css_selector(".button.checkout")
    checkout_button.click()
    data = get_checkoutdata('checkoutdata.txt')
    for did in data:
        print(data[did])
        if did == 'order_billing_state' or 'credit_card_month' or 'credit_card_year':
            option = browser.find_element_by_id(did)
            option.click()
            option.send_keys(data[did])
            option.send_keys(Keys.ENTER)
        else:
            element = browser.find_element_by_id(did)
            element.click()
            AntiBotMisc.send(element, data[did])

    element = browser.find_element_by_id('order_billing_city')
    element.click()
    element.clear()
    element.send_keys(data['order_billing_city'])
    browser.find_element_by_css_selector('input#order_terms.checkbox').click()
    time.sleep(3.5)
    ppay = browser.find_element_by_css_selector('input.button')
    ppay.click()


def main():
    #site = "http://webcache.googleusercontent.com/search?q=cache:http://www.supremenewyork.com/shop/all"
    site = "http://www.supremenewyork.com/shop/all"
    chromedriver_path = "{}/chromedriver".format( os.path.dirname(os.path.abspath(__file__)) )
    browser = webdriver.Chrome(chromedriver_path)
    products = FindProducts(browser, site)
    print(products)
    config = LoadConfiguration('prices_config.txt') ##Change this?
    ProductsToCart(browser, products, config)
    Checkout(browser)
    time.sleep(20) ##Just for debug so chrome doesn't eat all the ram
    browser.close()

if __name__ == '__main__': main()
