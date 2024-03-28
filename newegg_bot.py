from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import json
import csv

from time import sleep
from random import randint

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()   
# use this if you want to hide webdriver, but not recommended
# driver = webdriver.Chrome(chrome_options=chrome_options)   

wait = WebDriverWait(driver, 10)          

# Discord Channel Webhooks
hook_rtx3000 = "https://discord.com/api/webhooks/816355108052533258/Xxo-bl0pJHxpwu5Mh35BUIszG2UWRA5kfIQhfAaUcoo2oTLJViGJ0hPhyUBF4Y1eHuTZ"
hook_rxs6000 = "https://discord.com/api/webhooks/816355512340971520/Ir4IbO5H4RhF0D2dnoiyhB8LcGYInoXuQi7aibTO3FQPBRT7Js73QhMyAJqNK0SUnKhm"
hook_ryz5000 = "https://discord.com/api/webhooks/816355404619186216/pd5AF0bvOU9nbqFqcRdo7bpTOXyELRR5zJhViLW4ptrURaa06W7aRFPFqrp2USaFNxRt"

# Open the file in 'r' mode
csv_file = open('keywords.csv', 'r')
dataA = []
dataB = []
dataC = []

# Read off and discard first line, to skip headers
csv_file.readline()

# Split columns while reading
for a, b, c in csv.reader(csv_file, delimiter =','):
    # Append each variable to a separate list
    dataA.append(a)
    dataB.append(b)
    dataC.append(c)

# Parameters: retrieves webhook, product url & title
def discord_notification(webhook_url, url_d, title_raw): 
    title = title_raw.strip()
    data = {"content": "{} in stock at {}".format(title, url_d)}
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try: 
        result.raise_for_status()
    except requests.exceptions.HTTPError as err: 
        print(err)
    else:
        print("Payload delivered successfully.")

def search_rtx3000():
    for rtx3000 in dataA:
        urlA = rtx3000
        # retrieves url from list A
        driver.get(urlA)                   
        print ('Feeding webdriver...')
        sleep(randint(5,15))

        try:
            stock_newegg = driver.find_element_by_css_selector("#ProductBuy > div > div:nth-child(2) > button")
            title_raw = driver.find_element_by_css_selector("#app > div.page-content > div.page-section > div > div > div.row-body > div.product-main.display-flex > div.product-wrap > h1").text
            discord_notification(hook_rtx3000, urlA, title_raw) # forwards data to new subfunction
        except NoSuchElementException:
            print("Item not found on Newegg.")

    # driver.close() # if enabled gives session id error
        
def search_ryz5000():
    for ryz5000 in dataB:
        urlB = ryz5000
        driver.get(urlB)
        print ('Feeding webdriver...')
        sleep(randint(5,15))

        try:
            stock_newegg = driver.find_element_by_css_selector("#ProductBuy > div > div:nth-child(2) > button")
            title_raw = driver.find_element_by_css_selector("#app > div.page-content > div.page-section > div > div > div.row-body > div.product-main.display-flex > div.product-wrap > h1").text
            discord_notification(hook_rtx3000, urlB, title_raw) #forwards data to new subfunction
        except NoSuchElementException:
            print("Item not found on Newegg.")

def search_rxs6000():
    for rxs6000 in dataC:
        urlC = rxs6000
        driver.get(urlC)
        print ('Feeding webdriver...')
        sleep(randint(5,15))

        try:
            stock_newegg = driver.find_element_by_css_selector("#ProductBuy > div > div:nth-child(2) > button")
            title_raw = driver.find_element_by_css_selector("#app > div.page-content > div.page-section > div > div > div.row-body > div.product-main.display-flex > div.product-wrap > h1").text
            discord_notification(hook_rtx3000, urlC, title_raw) #forwards data to new subfunction
        except NoSuchElementException:
            print("Item not found on Newegg.")

def main():
    x = 0
    while x <1:
        search_rtx3000()
        search_rxs6000()
        search_ryz5000()

# executes main function
main()



# https://gist.github.com/Bilka2/5dd2ca2b6e9f3573e0c2defe5d3031b2