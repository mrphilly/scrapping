# coding=utf-8


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
#declare a session object

def getURL():
    cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='leads')
    cursor = cnx.cursor(buffered=True)
    site = "https://www.leboncoin.fr"
    options = Options()
    driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver_linux64 (1)/chromedriver", )
    data = []
    driver.get(site)
    (driver.page_source).encode('utf-8')
    driver.implicitly_wait(10) # seconds
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        result = soup.find("section", {"class": "_33mha"})
        data = result.findAll("div", {"class": "_3UM0h"})
    except:
        pass
    tab = []
    _tab = []
    FINAL_TAB = []
    CATEGORIES = []
    INFOS = []
    for a in data:
        try:
            tab = a.findAll("li", {"class": "_3f3p2"})
            for item in tab:
                _tab.append(item)
        except:
            continue
    for i in _tab:
        try:
            url_categorie = i.find('a').get("href")
            lib_categorie = i.find('a').text
            CATEGORIES.append({
                    "categorie": lib_categorie,
                    "url_categorie": site + url_categorie
                })
        except:
            continue
    for link in CATEGORIES:
        try:
            driver.get(link['url_categorie'])
            driver.implicitly_wait(5) # seconds
            number = driver.find_element_by_xpath("//*[@id='container']/main/div/div/div[3]/div/div[6]/div[1]/div/div[1]/div[1]/p/span").text.replace(" ", "")
            nb_page = int(number)/38
            FINAL_TAB.append({
                "categorie":  link['categorie'],
                "url_categorie": link['url_categorie'],
                "nb_page": str(nb_page)
            })
        except:
           continue
    
    for url in FINAL_TAB:
        nb_page = int(url['nb_page'])
        i = 1
        while i < nb_page:
            try:
                url_categorie_page = url['url_categorie'] + "p-" + str(i) + "/"
                driver.get(url_categorie_page)
                driver.implicitly_wait(5) # seconds
                soup = BeautifulSoup(driver.page_source, "html.parser")
                content = soup.find('ul', {'class': 'undefined'}).findAll("li", {"class": "_3DFQ-"})
                for el in content:
                    a = site + el.findAll('a')[0].get('href')
                    titre_annonce = el.findAll('a')[0].get('title').replace(u"\xe9", "e")
                    driver.get(a)
                    try:
                        driver.find_element_by_xpath("//*[@id='container']/main/div/div/div/section/section[2]/section[2]/div[1]/div/div/div/div[3]/div/div[1]").click()
                        driver.implicitly_wait(10) # seconds
                        nom = driver.find_element_by_xpath("//*[@id='container']/main/div/div/div/section/section[2]/section[2]/div[1]/div/div/div/div[1]/div[2]/div[1]").text
                        numero = driver.find_element_by_xpath("//*[@id='container']/main/div/div/div/section/section[2]/section[2]/div[1]/div/div/div/div[3]/div/div[1]/div/div/div/span/a").text.replace(" ", "")
                        INFOS.append({
                                "categorie": url['categorie'].replace(u"\xe9", "e").replace(u"\xe8", "e"),
                                "titre_annonce": titre_annonce.replace(u"\xe9", "e").replace(u"\xe8", "e"),
                                "nom": nom,
                                "numero": "+33" + numero
                        })
                        add_infos = ("""INSERT INTO leboncoin(categorie,titre_annonce,nom,numero)VALUES(%(categorie)s,%(titre_annonce)s,%(nom)s,%(numero)s)""")
                        for data in INFOS:
                            try:
                                print("Patientez svp en cours d'insertion dans la table leboncoin.....")
                                cursor.execute(add_infos, data)
                                cnx.commit()
                                print('suivant')
                            except:
                                print('erreur') 
                        INFOS = []          
                    except:
                        continue
            except:
                continue
            i = i + 1
    cursor.close()
    cnx.close()
    driver.close()
    return INFOS
    
  

print(getURL())
   
