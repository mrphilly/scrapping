# coding=utf-8


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector

def main():
     cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='leads')
     cursor = cnx.cursor(buffered=True)
     site = "https://search.vivastreet.com/annonces/fr?lb=new&search=1&start_field=1&select-this=00&searchGeoId=0&offer_type=offer&end_field="
     options = Options()
     driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver_linux64 (1)/chromedriver", )
     driver.get(site)

     nb_result = driver.find_element_by_xpath("//*[@id='toolbar']/ul/li/h2").text.replace(",", "")
     split = nb_result.split(" ")
     nb_page = int(split[0])/35
     print(nb_page)
     URL = []
     INFOS = []
     j = 1
     while(j < nb_page):
          lien = site[:42] + "/t+" + str(j) + site[42:]
          driver.get(lien)
          soup = BeautifulSoup(driver.page_source, "html.parser")
          _link = []
          try:
               link = soup.find("ul", {"class": "list"}).findAll("li", {"class": "classified"})
          except:
               continue
          for item in link:
               try:
                    url = item.find('div', {"class", "clad"}).find("a").get("href")
                    titre = item.find('div', {"class", "clad"}).find("a").find("div", {"class": "clad__summary"}).find("div", {"class": "clad__title"}).find("h4").text
                    categorie = item.find('div', {"class", "clad"}).find("a").find("div", {"class": "clad__geo"}).find('div', {"class": "clad__link"}).text
                    driver.get(url)
                    try:
                         nom = driver.find_element_by_xpath("//*[@id='classified-detail-block']/div[1]/span").text
                         driver.find_element_by_xpath("//*[@id='contact_phone_right_wrapper']/span[2]").click()
                         driver.implicitly_wait(5) # seconds
                         telephone = []
                         mobile = driver.find_element_by_xpath("//*[@id='contact_phone_right_wrapper']/span[3]/span").text.replace(" ", "")
                         for letter in mobile[:10]:
                              telephone.append(letter)
                         tel="+33" + ''.join(telephone)
                        
                         INFOS.append({
                              "categorie": categorie,
                              "titre_annonce": titre.replace(u"\xe9", "e").replace(u"\xe8", "e"),
                              "nom": nom.replace(u"\xe9", "e").replace(u"\xe8", "e").replace(u"Publiee par ", ""),
                              "numero": tel
                         })
                         
                         add_infos = ("""INSERT INTO vivastreet(categorie,titre_annonce,nom,numero)VALUES(%(categorie)s,%(titre_annonce)s,%(nom)s,%(numero)s)""")
                         for data in INFOS:
                              try:
                                   print("Patientez svp en cours d'insertion dans la table vivastreet.....")
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
          j = j + 1
     cursor.close()
     cnx.close()
     driver.close()
     return INFOS
     
               

print(main())