# coding=utf-8
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector
from ebaysdk.exception import ConnectionError
from selenium.common.exceptions import NoSuchElementException

options = Options()
site = "https://www.amazon.fr"
add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id, infos)
                              VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s,%(infos)s)""")

driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver_linux64 (1)/chromedriver", )
def getURL():

     first_url = "https://www.amazon.fr/gp/site-directory?ref_=nav_shopall_btn"
     data = []
     """
          Porte d'entrée du scrapping urls de toutes les catégories
     """
     driver.get(first_url)
     soup = BeautifulSoup(driver.page_source, "html.parser")
     AMAZON1 = []
     content = soup.find("table", {"id": "shopAllLinks"}).find("tbody").find("tr").findAll("td")
     for el in content:
          div = el.findAll("div", {"class": "popover-grouping"})
          for i in div:
               categorie = i.find("h2", {"class": "popover-category-name"}).text
               lien = i.find("ul", {"class": "nav_cat_links"}).findAll("li")
               for _i in lien:
                    link = site + _i.find("a", {"class": "nav_a"}).get("href")
                    AMAZON1.append({
                         "categorie": categorie,
                         "url": link
                    })
     return AMAZON1
     """
          AMAZON1[] contient toutes les URL des catégories
     """





def getAll():
     tab = getURL()
     longueur = len(tab) - 120  #43
     PRODUCT = []
     table = []
     next_url = ""

     """
          Pour chaque catégories faire
     """
     for item in tab[30:]:
          try:
               reload(sys)
               sys.setdefaultencoding("utf-8")
               url = item['url'].replace('%C3%A9', "é").decode('utf-8')
               """
                    Url d'une catégorie
               """
               driver.get(url)
               try:
                         elements = WebDriverWait(driver, 10).until(
                              EC.presence_of_element_located((By.ID, "mainResults"))
                         )
               except:
                    continue
               """
                    Trouver le block central contenant les résultats et trouver l'url de la page suivante
               """
               content = driver.find_element_by_xpath("//*[@id='mainResults']/ul")
               data = content.find_elements_by_class_name("s-result-card-for-container-noborder")
               next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute('href')
               """
                    data contient tous les résultats de la première page d'une catégorie donnée
               """
               for element in data:
                    table.append(element)
          except:
               continue

          URL = []
          URL_1 = []
          """
               Pour chaque produit trouver ses caractéristiques
          """
          for el in table:
               try:
                    html = el.get_attribute("innerHTML")
                    soup = BeautifulSoup(html, "html.parser")
                    lib_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("alt")
                    url_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).get("href")
                    img_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("src")
                    price_product = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("a", {"class": "a-link-normal"}).find("span", {"class": "a-size-base"}).text.replace(u"EUR ", "").replace(",", ".")
                    if (price_product == "GRATUIT"):
                         prix = "0"
                    elif ("-" in price_product):
                         p = price_product.split("-")
                         prix  = float(p[1]) * 657.10
                    else:
                         prix = float(price_product) * 657.10
                    if site not in url_product:
                         url_product = site + url_product
                    URL.append({
                         "lib": lib_product,
                         "url": url_product,
                         "img": img_product,
                         "prix": prix
                    })
                    """
                         URL contient toutes les caractéristiques de chaque produit trouvé dans la première page
                    """
               except:
                    continue
          """
               On vide ce tableau pour éviter les répétitions de produits
          """
          table = []
          """
               Pour chaque produit contenu dans URL aller vers sa page et trouver ses infos selon le type de page
          """
          for link in URL:
               driver.get(link["url"])
               try:
                         element = WebDriverWait(driver, 10).until(
                              EC.presence_of_element_located((By.ID, "prodDetails"))
                         )
               except:
                    continue
               try:
                    infos = driver.find_element_by_xpath("//*[@id='prodDetails']").text

               except NoSuchElementException:
                    try:
                         infos = driver.find_element_by_xpath("//*[@id='tech-specs-table-left']").text
                    except:
                         try:
                              infos = driver.find_element_by_xpath("//*[@id='product-specification-table']").text
                         except:
                              try:
                                   infos = driver.find_element_by_xpath("//*[@id='detail_bullets_id']").text
                              except:
                                   infos = driver.find_element_by_xpath("//*[@id='tech-specs-desktop']").text


               PRODUCT.append({
                    "libProduct": link["lib"],
                    "slug": "",
                    "descProduct": "",
                    "priceProduct": link["prix"],
                    "imgProduct": link["img"],
                    "numSeller": "",
                    "src": "https://www.amazon.fr",
                    "urlProduct": link["url"],
                    "logo": "",
                    "logoS": "",
                    "origine": 0,
                    "subcategory_id": item["categorie"],
                    "infos": infos
               })
               """
                    PRODUCT contient un produit avec ses information au complet
               """
               cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_db')
               cursor = cnx.cursor(buffered=True)
               for data in PRODUCT:
                    try:
                         print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                         cursor.execute(add_produit, data)
                         cnx.commit()
                         print('suivant')
                    except ConnectionError as e:
                         print(e.response.reply)
               """
                    On vide PRODUCT pour éviter les doublons de produits
               """
               cursor.close()
               cnx.close()
               PRODUCT = []
          URL = []


          i = 2
          while(next_url and i < 7):
                    print("page: " + str(i))
                    print(next_url)
                    driver.get(next_url)

                    try:
                         next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute('href')

                    except NoSuchElementException:
                         break
                    content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']")
                    data = content.find_elements_by_tag_name("li")

                    for el in data:
                                   try:
                                        html = el.get_attribute("innerHTML")
                                        soup = BeautifulSoup(html, "html.parser")
                                        lib_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("alt")
                                        url_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).get("href")
                                        img_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("src")
                                        price_product = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("a", {"class": "a-link-normal"}).find("span", {"class": "a-size-base"}).text.replace(u"EUR ", "").replace(",", ".")
                                        if (price_product == "GRATUIT"):
                                             prix = "0"
                                        elif ("-" in price_product):
                                             p = price_product.split("-")
                                             prix  = float(p[1]) * 657.10
                                        else:
                                             prix = float(price_product) * 657.10
                                        if site not in url_product:
                                             url_product = site + url_product
                                        URL_1.append({
                                             "lib": lib_product,
                                             "url": url_product,
                                             "img": img_product,
                                             "prix": prix
                                        })

                                   except:
                                        continue

                    next_url
                    i = i + 1
          for link in URL_1:
                         print(link["url"])
                         driver.get(link["url"])

                         try:
                              element = WebDriverWait(driver, 10).until(
                                   EC.presence_of_element_located((By.ID, "prodDetails"))
                              )
                         except:
                              continue
                         try:
                              infos = driver.find_element_by_xpath("//*[@id='prodDetails']").text

                         except NoSuchElementException:
                              try:
                                   infos = driver.find_element_by_xpath("//*[@id='tech-specs-table-left']/tbody").text
                              except:
                                   try:
                                        infos = driver.find_element_by_xpath("//*[@id='product-specification-table']/tbody").text
                                   except:
                                        try:
                                             infos = driver.find_element_by_xpath("//*[@id='detail_bullets_id']").text
                                        except:
                                             continue
                         PRODUCT.append({
                              "libProduct": link["lib"],
                              "slug": "",
                              "descProduct": "",
                              "priceProduct": link["prix"],
                              "imgProduct": link["img"],
                              "numSeller": "",
                              "logoS": "",
                              "src": "https://www.amazon.fr",
                              "urlProduct": link["url"],
                              "logo": "",
                              "origine": 0,
                              "subcategory_id": item["categorie"],
                              "infos": infos
                         })
                         cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_db')
                         cursor = cnx.cursor(buffered=True)
                         for data in PRODUCT:
                              try:
                                   print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                                   cursor.execute(add_produit, data)
                                   cnx.commit()
                                   print('suivant')
                              except ConnectionError as e:
                                   print(e.response.reply)
                         cursor.close()
                         cnx.close()
                         PRODUCT = []

          URL_1 = []


     return "ok"




print(getAll())
