# coding=utf-8


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector


def getURL():
     site = "https://www.amazon.fr/t%C3%A9l%C3%A9phonie-t%C3%A9l%C3%A9phone-portable-smartphone/b/ref=sd_allcat_tele?ie=UTF8&node=13910711"
     options = Options()
     driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver_linux64 (1)/chromedriver", )
     data = []
     driver.get(site)
     content = driver.find_element_by_xpath("//*[@id='mainResults']/ul").text
     print(content)
print(getURL())