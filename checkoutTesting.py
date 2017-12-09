#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

#browser = webdriver.Chrome("{}/chromedriver".format(current_direc))
'''
Alternative 1 with each value having a variable
with open("checkoutdata.txt") as inp:
    data = inp.read().splitlines()
print(data)
name = data[0].split(': ', 1)[-1]
print(name)
email = data[1].split(': ', 1)[-1]
tel = data[2].split('')
'''
d = {}
nkey = ""
with open("checkoutdata.txt") as f:
    for line in f:
        key, val = line.split(": ")
        if key.find("\n") != -1:
            key = key.replace("\n", "")
        if val.find("\n") != -1:
            val = val.replace("\n", "")
        d[key] = val
print(d)
for key, val in d.items():
    if val == "N/A":
        del d[key]
print(d)
#namef = browser.find_element_by_class_name("payment")
