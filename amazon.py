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


def getURL():
     cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_db')
     cursor = cnx.cursor(buffered=True)
     site = "https://www.amazon.fr/gp/site-directory?ref_=nav_shopall_btn"
     options = Options()
     driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver_linux64 (1)/chromedriver", )
     data = []
     driver.get(site)
     soup = BeautifulSoup(driver.page_source, "html.parser")
     AMAZON1 = []
     content = soup.find("table", {"id": "shopAllLinks"}).find("tbody").find("tr").findAll("td")
     for el in content:
          div = el.findAll("div", {"class": "popover-grouping"})
          for i in div:
               categorie = i.find("h2", {"class": "popover-category-name"}).text
               lien = i.find("ul", {"class": "nav_cat_links"}).findAll("li")
               for _i in lien:
                    link = site + i.find("a", {"class": "nav_a"}).get("href")
                    AMAZON1.append({
                         "categorie": categorie,
                         "url": link
                    })
     longueur = len(AMAZON1) - 83  #43
     PRODUCT = []
     for link in AMAZON1[-longueur:]:
          reload(sys)
          sys.setdefaultencoding("utf-8")
          a = link['url'].replace('%C3%A9', "é")
          try:
               driver.get(a.decode('utf-8').replace("/gp/site-directory?ref_=nav_shopall_btn", ""))

               content = driver.find_element_by_xpath("//*[@id='mainResults']/ul")
               data = content.find_elements_by_tag_name("li")
               next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
               for el in data:
                    lib_product = el.find_element_by_class_name("s-access-detail-page").get_attribute("title")
                    url_product = el.find_element_by_class_name("s-access-detail-page").get_attribute("href")
                    img_product = el.find_element_by_class_name("s-access-image").get_attribute("src")
                    price_product = el.find_element_by_class_name("s-price").text.replace(u"EUR ", "").replace(",", ".")
                    driver.implicitly_wait(20) # seconds
                    if (price_product == "GRATUIT"):
                         prix = "0"
                    else:
                         prix = float(price_product) * 657.10
                    try:
                         driver.get(url_product)
                         driver.implicitly_wait(20) # seconds

                         infos = driver.find_element_by_xpath("//*[@id='prodDetails']/div[2]/div[1]/div/div[2]/div/div/table/tbody/tr[4]/td[2]").text
                         print("infos: " + infos)
                         driver.back()
                    except:
                         continue
                    PRODUCT.append({
                              "libProduct": lib_product,
                              "slug": "",
                              "descProduct": "",
                              "priceProduct": str(prix),
                              "imgProduct": img_product,
                              "numSeller": "",
                              "src": "https://www.amazon.fr",
                              "urlProduct": url_product,
                              "logo": "",
                              "logoS": "",
                              "origine": 0,
                              "subcategory_id": link["categorie"]
                              })
                    print(PRODUCT)
                    add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id)
                             VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s)""")

                    for data in PRODUCT:
                         try:
                              print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                              cursor.execute(add_produit, data)
                              cnx.commit()
                              print('suivant')
                         except ConnectionError as e:
                              print(e.response.reply)

                    PRODUCT = []



                    while(next_url != 'none'):
                         print(next_url)
                         url = next_url
                         if "https://www.amazon.fr" not in next_url:
                              url = "https://www.amazon.fr" + next_url
                         driver.get(url)

                         content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']")
                         data = content.find_elements_by_tag_name("li")
                         next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
                         for el in data:
                              lib_product = el.find_element_by_class_name("s-access-detail-page").get_attribute("title")
                              url_product = el.find_element_by_class_name("s-access-detail-page").get_attribute("href")
                              img_product = el.find_element_by_class_name("s-access-image").get_attribute("src")
                              price_product = el.find_element_by_class_name("s-price").text.replace(u"EUR ", "").replace(",", ".")
                              if (price_product == "GRATUIT"):
                                   prix = "0"
                              else:
                                   prix = float(price_product) * 657.10
                              driver.implicitly_wait(20) # seconds
                              try:
                                   driver.get(url_product)
                                   infos = driver.find_element_by_xpath("//*[@id='prodDetails']/div[2]/div[1]/div/div[2]/div/div/table/tbody/tr[4]/td[2]").text
                                   print("infos: " + infos)

                              except:
                                   continue
                              PRODUCT.append({
                              "libProduct": lib_product,
                              "slug": "",
                              "descProduct": "",
                              "priceProduct": str(prix),
                              "imgProduct": img_product,
                              "numSeller": "",
                              "src": "https://www.amazon.fr",
                              "urlProduct": url_product,
                              "logo": "",
                              "logoS": "",
                              "origine": 0,
                              "subcategory_id": link["categorie"]
                              })
                              add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id)
                              VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s)""")

                              for data in PRODUCT:
                                   try:
                                        print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                                        cursor.execute(add_produit, data)
                                        cnx.commit()
                                        print('suivant')
                                   except ConnectionError as e:
                                        print(e.response.reply)

                              PRODUCT = []
                         driver.implicitly_wait(20) # seconds
                         next_url
          except ConnectionError as e:
                              print(e.response.reply)
                              continue

     cursor.close()
     cnx.close()
print(getURL())