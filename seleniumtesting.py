"""
Make sure to have chromedriver in this folder
Options for "to_buy" field ["jackets", "tops/sweaters", "sweatshirts", "accessories", "pants", "hats", "bags", "skate"]
Includes fuzzing to make wait times slightly random
"""

from selenium import webdriver
import time
import random

VERSION = 0.01
Action_Delay = 0.5
browser = webdriver.Chrome("/Users/jakobliggett/PycharmProjects/sbot/chromedriver")

def wait(wtime=0, wfuzzing=0.20):
    if wtime == 0:
        time.sleep(Action_Delay+random.uniform(-(wtime*wfuzzing), (wtime*wfuzzing)))
    else:
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

def SupremeRoutine(buyclass):
    browser.get('http://www.supremenewyork.com/')
    wait(1)
    shop_link = browser.find_element_by_class_name("shop_link")
    shop_link.click()
    wait()
    ##Found shop, get type
    products = {}
    for category in buyclass:
        try:
            products[category] = browser.find_elements_by_class_name(category)
        except Exception as e:
            print('Error grabbing a category: ', str(e))
    #print(products)
    wait()
    item_names = []
    for category_of_items in list(products.items()):
        for item in category_of_items[1]:
            try:
                wait()
                print(item)
                item.click()
                wait()
                product_name = browser.find_elements_by_class_name("protect")
                item_names.append(product_name)
                wait()
                browser.goBack()
                wait()
            except Exception as e:
                print('Error opening item: ', str(e), '\n')

    print('Item names: ', item_names)
    wait(12)
    browser.close()



if __name__ == "__main__":
    to_buy = ["jackets", "sweatshirts"]
    SupremeRoutine(to_buy)
    #GoogleRoutine()