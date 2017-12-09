from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

def checkout(data):
    browser.get('http://www.supremenewyork.com/checkout')
    namef = browser.find_element_by_class_name("payment")
    
if __name__ == '__main__':
    checkout(get_checkoutdata("checkoutdata.txt"))
