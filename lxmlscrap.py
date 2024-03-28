from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

from time import sleep
from random import randint

from tqdm import tqdm

# define webdriver parameters
chrome_options = Options()
chrome_options.add_argument("--headless")

# initialize empty lists to store data
urls = []
brands = []
types = []
models = []
cpus = []
lcds = []
rams = []
drives = []
gpus = []
weights = []
panels = []
lcd_hz = []
resolutions = []
wlans = []
keyboards = []
webcams = []
batteries = []
launchdates = []


# prepare to read csv with links
with open('links.csv', 'r') as f:
    csv_raw_cont = f.read()

# split by line
split_csv = csv_raw_cont.split('\n') 

# remove empty lines
split_csv.remove('')

# specify separator
separator = ","

# iterate over each csv line
for each in tqdm(split_csv):

    url_row_index = 0 #sepcify index of starting row
    url = each.split(separator)[url_row_index] #get url
    driver = webdriver.Chrome(chrome_options=chrome_options) #intialize web driver
    driver.get(url) #feed web driver with url

    sleep(randint(3,11)) #delay to prevent server request overload


    # get current url
    url = driver.current_url
    urls.append(url)

    # xpath scraper targeting specific table cells containing specs + if not found skip
    try:
        brand = driver.find_element_by_xpath("//th[text()='Brand']/following-sibling::td").get_attribute('innerHTML') 
        brands.append(brand) 
    except NoSuchElementException:
        brand = 'N/A'
        brands.append(brand)

    try:
        series = driver.find_element_by_xpath("//th[text()='Series']/following-sibling::td").get_attribute('innerHTML') 
        types.append(series)
    except NoSuchElementException:
        series = 'N/A'
        types.append(series)

    try:
        model = driver.find_element_by_xpath("//th[text()='Model']/following-sibling::td").get_attribute('innerHTML') 
        models.append(model)
    except NoSuchElementException:
        model = 'N/A'
        models.append(model)

    try:
        cpu = driver.find_element_by_xpath("//th[text()='CPU']/following-sibling::td").get_attribute('innerHTML') 
        cpus.append(cpu)
    except NoSuchElementException:
        cpu = 'N/A'
        cpus.append(cpu)

    try:
        screen = driver.find_element_by_xpath("//th[text()='Screen']/following-sibling::td").get_attribute('innerHTML')
        lcds.append(screen)
    except NoSuchElementException:
        screen = 'N/A'
        lcds.append(screen)

    try:
        ram = driver.find_element_by_xpath("//th[text()='Memory']/following-sibling::td").get_attribute('innerHTML') 
        rams.append(ram)
    except NoSuchElementException:
        ram = 'N/A'
        rams.append(ram)

    try:
        storage = driver.find_element_by_xpath("//th[text()='Storage']/following-sibling::td").get_attribute('innerHTML') 
        drives.append(storage)
    except NoSuchElementException:
        storage = 'N/A'
        drives.append(storage)

    try:
        gpu = driver.find_element_by_xpath("//th[text()='Graphics Card']/following-sibling::td").get_attribute('innerHTML') 
        gpus.append(gpu)
    except NoSuchElementException:
        gpu = 'N/A'
        gpus.append(gpu)

    try:
        weight = driver.find_element_by_xpath("//th[text()='Weight']/following-sibling::td").get_attribute('innerHTML') 
        weights.append(weight)
    except NoSuchElementException:
        weight = 'N/A'
        weights.append(weight)

    try:
        panel = driver.find_element_by_xpath("//th[text()='Screen Size']/following-sibling::td").get_attribute('innerHTML') 
        panels.append(panel)
    except NoSuchElementException:
        panel = 'N/A'
        panels.append(panel)

    try:
        screen_hz = driver.find_element_by_xpath("//th[text()='Refresh Rate']/following-sibling::td").get_attribute('innerHTML')
        lcd_hz.append(screen_hz)
    except NoSuchElementException:
        screen_hz = 'N/A'
        lcd_hz.append(screen_hz)

    try:
        resolution = driver.find_element_by_xpath("//th[text()='Resolution']/following-sibling::td").get_attribute('innerHTML') 
        resolutions.append(resolution)
    except NoSuchElementException:
        resolution = 'N/A'
        resolutions.append(resolution)

    try:
        wlan = driver.find_element_by_xpath("//th[text()='WLAN']/following-sibling::td").get_attribute('innerHTML') 
        wlans.append(wlan)
    except NoSuchElementException:
        wlan = 'N/A'
        wlans.append(wlan)

    try:
        backlit_key = driver.find_element_by_xpath("//th[text()='Backlit Keyboard']/following-sibling::td").get_attribute('innerHTML') 
        keyboards.append(backlit_key)
    except NoSuchElementException:
        backlit_key = 'N/A'
        keyboards.append(backlit_key)

    try:
        webcam = driver.find_element_by_xpath("//th[text()='Webcam']/following-sibling::td").get_attribute('innerHTML')
        webcams.append(webcam)
    except NoSuchElementException:
        webcam = 'N/A'
        webcams.append(webcam)
        pass

    try:
        battery = driver.find_element_by_xpath("//th[text()='Battery']/following-sibling::td").get_attribute('innerHTML') 
        batteries.append(battery)
    except NoSuchElementException:
        battery = 'N/A'
        batteries.append(battery)

    try:
        release = driver.find_element_by_xpath("//th[text()='Date First Available']/following-sibling::td").get_attribute('innerHTML')
        launchdates.append(release)
    except NoSuchElementException:
        release = 'N/A'
        launchdates.append(release)

    # close driver after job done
    driver.close()


# building dataframe
laptops = pd.DataFrame({
'link': urls,
'brand': brands,
'series': types,
'model': models,
'cpu': cpus,
'screen': lcds,
'memory': rams,
'storage': drives,
'graphics card': gpus,
'weight': weights,
'screen size': panels,
'refresh rate': lcd_hz,
'resolution': resolutions,
'wlan': wlans,
'keyboard': keyboards,
'webcam': webcams,
'battery': batteries,
'release date': launchdates
})

# print to csv
laptops.to_csv('laptops.csv')


# selenium noexception
# https://towardsdatascience.com/web-automation-nightmares-6-tricks-to-overcome-them-4241089953e3
# https://stackoverflow.com/questions/3139402/how-to-select-following-sibling-xml-tag-using-xpath

# legacy solution for scraping
# brand = driver.find_element_by_xpath("//th[text()='Brand']/following-sibling::td").get_attribute('innerHTML') 
# brands.append(brand) 
