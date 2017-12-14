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

def FindProducts(browser, site, config):
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
            if config[category] > 0: ##Only add to check list if we're looking for them
                products.append([category, link])
    if len(products) == 0:
        print('No products available!')
        time.sleep(1) ##Refresh Delay
        return 0
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
            #print(product_name, product_price)
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
                print('Break early, cart {}, difference {}, max cart {}'.format(current_cart_value, config['max_cart']-current_cart_value, config['max_cart']))
                break ##Cart full, maxed on price
        except:
            pass
        time.sleep(0.1) ##Is this necessary? # No
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
    ##Add E's code in here later
    data = get_checkoutdata('checkoutdata.txt')
    for did in data:
        if not did == "order_billing_city": ##Lazy solution but oh well
            if did == 'order_billing_state' or 'credit_card_month' or 'credit_card_year':
                option = browser.find_element_by_id(did)
                option.click()
                #option.send_keys(data[did])
                AntiBotMisc.send(option, data[did])
                option.send_keys(Keys.ENTER)
            else:
                if did == 'N/A':
                    pass
                else:
                    element = browser.find_element_by_id(did)
                    element.click()
                    time.sleep(0.1)
                    """
                    element.send_keys(Keys.CONTROL + 'a')
                    element.send_keys(Keys.DELETE)
                    element.send_keys(Keys.COMMAND + 'a') ##Mac Version
                    element.send_keys(Keys.DELETE)
                    """
                    #element.send_keys(data[did])
                    AntiBotMisc.send(element, data[did])

    time.sleep(1)
    print("\nORDERING!")
    try: ##Captcha makes this fail, switch to manual mode
        terms = browser.find_element_by_id("order_terms")
        terms.click()
        time.sleep(2)
        #checkout_final = browser.find_element_by_name("commit")
        #checkout_final.click()
    except Exception as e:
        print("MANUAL MODE ENGAGED!\n {}\n MANUAL MODE ENGAGED!".format(str(e)))

def main():
    #site = "http://webcache.googleusercontent.com/search?q=cache:http://www.supremenewyork.com/shop/all"
    site = "http://www.supremenewyork.com/shop/all"
    current_path = "{}/chromedriver".format( os.path.dirname(os.path.abspath(__file__)) )
    config = LoadConfiguration('prices_config.txt') ##Change this?
    browser = webdriver.Chrome(current_path)
    products = 0
    while products == 0: ##Loops until something found not sold out
        products = FindProducts(browser, site, config)
    try:
        os.system("afplay {}/Alarm.mp3".format(current_path))
    except:
        pass ##This will prob fail on windows?
    print(products)
    ProductsToCart(browser, products, config)
    Checkout(browser)
    time.sleep(20) ##Just for debug so chrome doesn't eat all the ram
    browser.close()

if __name__ == '__main__': main()
