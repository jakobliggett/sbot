"""
Make sure to have chromedriver in this folder
Options for "to_buy" field ["jackets", "tops/sweaters", "sweatshirts", "accessories", "pants", "hats", "bags", "skate"]
Includes fuzzing to make wait times slightly random
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import os
import checkoutTesting as check

VERSION = 0.02
Action_Delay = 0.5
current_direc = os.path.dirname(os.path.abspath(__file__))
browser = webdriver.Chrome("{}/chromedriver".format(current_direc))
#browser = webdriver.Chrome()

def wait(wtime=0, wfuzzing=0.20):
    if wtime == 0:
        time.sleep(Action_Delay+random.uniform(-(wtime*wfuzzing), (wtime*wfuzzing)))
    els
        if wfuzzing == 0:
            time.sleep(wtime)
        else:
            time.sleep(wtime+random.uniform(-(wtime*wfuzzing), (wtime*wfuzzing)))

def RealSend(send_object, text, cpm=500, rand_fuzzing = 0.10): ##200 avg 400 cpm fast
    timeperchar = 60/cpm
    if rand_fuzzing == 0:
        for char in text:
            time.sleep(timeperchar)
            send_object.send_keys(char)
    else:
        for char in text:
            time.sleep(timeperchar+random.uniform(-(timeperchar*rand_fuzzing), (timeperchar*rand_fuzzing))) ##Introduces random delay
            send_object.send_keys(char)

def GoogleRoutine():
    browser.get('http://www.google.com')
    wait()
    linkElem = browser.find_element_by_id("lst-ib")
    linkElem.click()
    RealSend(linkElem, "Supreme")
    wait()
    linkElem.submit()

def TestUA():
    ##If UA is flagged the bot will be "banned", you can check here
    browser.get("https://www.google.com/search?q=what+is+my+user+agent&oq=what+is+my+user+agent")

def ScanforProducts(buyclass):
    products = {}
    for category in buyclass:
        try:
            newprod = browser.find_elements_by_css_selector('.{} a'.format(category)) ##This finds all elements with category
            ##Then it grabs the "a" child which contains the link to the item
            newlst = []
            for element in newprod:
                newlst.append ( (element.get_attribute("href")) ) ##This gets the link text
            products[category] = newlst
        except Exception as e:
            print('Error grabbing a category: ', str(e))
    return products

def SupremeRoutine(buyclass):
    browser.get('http://www.supremenewyork.com/')
    #wait(1)
    shop_link = browser.find_element_by_class_name("shop_link")
    shop_link.click()
    wait()
    ##Found shop, get type
    products = ScanforProducts(buyclass)
    #print(products)
    wait()
    link_dict = {}
    print(list(products.items()))
    for category_of_items in list(products.items()):
        for item in category_of_items[1]:
            try:
                wait()
                print(item)
                browser.get(item)
                wait()
                product_name = browser.find_element_by_class_name("protect").text ##This gets the name of the

                other_colors = browser.find_elements_by_class_name("data-images")
                print('others: ', other_colors)
                for color in other_colors:
                    print('Other color:', color, color.get_attribute("href"))
                print(product_name)
                link_dict[product_name] = item
                wait()
                browser.back()
                wait()
            except Exception as e:
                print('Error opening item: ', str(e), '\n')
                wait(0.2)

    print('\nItem Dict: ', link_dict)
    ##At this point we have all of the items and links! Just not all of the colors...
    ##TODO ADD COLOR CHECKING

    for item in link_dict: ##Fix this to add an approved list
        #if input('Buy {}? (y/n/): '.format(item)).lower().startswith('y'):
        if True:
            ##buy
            browser.get(link_dict[item])
            try:
                purchase = browser.find_element_by_css_selector("input.button")
                purchase.click()
            except Exception as e:
                print('Out of stock, or: {}'.format(str(e)))
            wait()
            browser.back()
            wait()
    wait()
    try:
        checkout = browser.find_element_by_css_selector(".button.checkout")
    except Exception as e:
        print("Couldn't find checkout button, {}".format(str(e)))
    wait()
    checkout.click()
    check.checkout(browser)
    ##browser.close() we dont want the browser to close before they checkout


if __name__ == "__main__":
    to_buy = ["jackets", "sweatshirts"]
    SupremeRoutine(to_buy)
    #GoogleRoutine()
