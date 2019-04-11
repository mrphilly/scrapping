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
add_produit = ("""INSERT INTO products(libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id, infos) VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s,%(infos)s, %(livraison)s)""")

driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver/chromedriver", )

CAT= [
     "https://www.amazon.fr/b/ref=sd_allcat_fashion_men?ie=UTF8&node=12422073031", #Hommes
     "https://www.amazon.fr/b/ref=sd_allcat_fashion_women?ie=UTF8&node=12422072031", #Femmes
     "https://www.amazon.fr/b/ref=sd_allcat_fashion_girls?ie=UTF8&node=12422074031" ,#Filles
     "https://www.amazon.fr/b/ref=sd_allcat_fashion_boys?ie=UTF8&node=12422075031", #Garcons
     "https://www.amazon.fr/b/ref=sd_allcat_fashion_baby?ie=UTF8&node=12422076031", #Bébé
     #"https://www.amazon.fr/sacs-femme/b/ref=sd_allcat_handbags?ie=UTF8&node=1765336031", #Sac à main
     #"https://www.amazon.fr/Bijoux-Bagues-Bracelets-Colliers-Boucles-d-oreilles/b/ref=sd_allcat_jewelry?ie=UTF8&node=193710031" #Bijoux


]

def main():
     table = []
     URL = []
     PRODUCT = []
     for cat in CAT:
          site = "https://www.amazon.fr"
          try:
               driver.get(cat)
          except TimeoutException:
               continue
          driver.implicitly_wait(20)
          content = driver.find_element_by_id("merchandised-content")
          element = content.find_element_by_xpath("//*[@id='merchandised-content']/div[4]").find_element_by_class_name("bxc-grid__container").find_elements_by_class_name("bxc-grid__column")
          tab = []
          for el in element:

               try:
                    url = el.find_element_by_class_name("bxc-grid__image").find_element_by_tag_name("a").get_attribute("href")
                    categorie = el.find_element_by_class_name("bxc-grid__image").find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("alt")
                    if site not in url:
                         url = site + url
                    tab.append({
                         "categorie": categorie,
                         "url": url
                    })
               except NoSuchElementException:
                    continue


          for item in tab:
               livraison = ""

               driver.get(tab)
               driver.implicitly_wait(10)
               next_url = ""
               try:
                    next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
               except NoSuchElementException:
                         pass

               try:
                         content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']")
                         data = content.find_elements_by_tag_name("li")
                         for el in data:

                              html = el.get_attribute("innerHTML")
                              soup = BeautifulSoup(html, "html.parser")
                              lib_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("alt")
                              url_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).get("href")
                              img_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("src")
                              try:
                                   price_product = soup.findAll("div", {"class": "a-spacing-none"})[2].find("a", {"class": "a-link-normal"}).find("span", {"class": "a-size-base"}).text.replace(u"EUR ", "").replace(",", ".").replace(u"\xa0", "")
                              except:
                                   price_product = soup.findAll("div", {"class": "a-spacing-none"})[2].find("a", {"class": "a-link-normal"}).find("span", {"class": "a-color-price"}).text.replace(u"EUR ", "").replace(",", ".").replace(" ", "").replace(u"\xa0", "")
                              try:
                                   icon = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("i", {"class": "a-icon-prime"})
                                   livraison = "GRATUITE"
                                   print(livraison)
                              except:
                                   try:
                                        _livraison =  soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("span", {"class": "a-size-small"})
                                        _livraison = _livraison.text.replace(u"+ EUR", "").replace(",", ".").replace(u" Livraison", "")
                                        livraison = str(float(_livraison.replace(" ", "")) * 658.39)
                                        print(livraison)
                                   except:
                                        livraison = ""
                              print("livraison "+ livraison)
                              if (price_product == "GRATUIT"):
                                   prix = "0"
                              elif ("-" in price_product):
                                   p = price_product.split("-")
                                   prix  = float(p[1].replace(" ", "")) * 658.39
                              else:
                                   prod = price_product.replace(" ", "")
                                   print(prod)
                                   prix = float(prod) * 658.39
                              if site not in url_product:
                                   url_product = site + url_product
                              URL.append({
                              "lib": lib_product,
                              "url": url_product,
                              "img": img_product,
                              "prix": prix,
                              "categorie": item["categorie"],
                              "livraison": livraison
                              })

                         for link in URL:
                              driver.get(link["url"])
                              driver.implicitly_wait(10)
                              try:
                                   infos = driver.find_element_by_xpath("//*[@id='prodDetails']").get_attribute("innerHTML")
                              except NoSuchElementException:
                                   try:
                                        infos = driver.find_element_by_xpath("//*[@id='tech-specs-table-left']/tbody").get_attribute("innerHTML")
                                   except:
                                        try:
                                             infos = driver.find_element_by_xpath("//*[@id='product-specification-table']/tbody").get_attribute("innerHTML")
                                        except:
                                             try:
                                                  infos = driver.find_element_by_xpath("//*[@id='detail_bullets_id']").get_attribute("innerHTML")
                                             except:
                                                  try:
                                                            infos = driver.find_element_by_xpath("//*[@id='tech-specs-desktop']").text
                                                  except:
                                                            try:
                                                                 infos = driver.find_element_by_xpath("//*[@id='productDescription_feature_div']").text
                                                            except:
                                                                 try:
                                                                      infos = driver.find_element_by_xpath("//*[@id='productDetailsTable']/tbody/tr/td").text
                                                                 except:
                                                                      continue

                              shipping = link["livraison"]
                              if shipping == "":
                                   try:
                                        offer = driver.find_element_by_xpath("//*[@id='buybox-see-all-buying-choices-announce']").get_attribute("href")
                                        if site not in offer:
                                             offer = site + offer
                                        driver.get(offer)
                                        offer_price = driver.find_element_by_xpath("//*[@id='olpOfferList']/div/div/div[2]/div[1]/p/span/span[1]").text.replace("EUR ", "").replace(",", ".")
                                        shipping = str(float(offer_price) * 658.39)
                                   except:
                                        try:
                                             offer = driver.find_element_by_xpath("//*[@id='usedbuyBox']/div[1]/div").text.replace(u"+ EUR", "").replace(",",".").replace(u" (livraison)")
                                             print(offer)
                                             shipping = str(float(offer) * 658.39)
                                        except:
                                             try:
                                                  offer = driver.find_element_by_xpath("//*[@id='soldByThirdParty']/span[2]").text.replace(u"+ EUR", "").replace(",", ".").replace(u" Livraison", "")
                                                  shipping = str(float(offer) * 658.39)
                                             except:
                                                       shipping = ""


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
                              "subcategory_id": link["categorie"],
                              "infos": infos,
                              "livraison": link["livraison"]
                              })
                              cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_vetement')
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
                         URL = []
               except NoSuchElementException as e:
                    print(e)
               i = 2
               while(next_url and i < 15 ):
                              try:
                                   driver.get(next_url)
                              except:
                                   break
                              driver.implicitly_wait(10)
                              try:
                                   next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
                              except:
                                   break
                              try:
                                   elements = WebDriverWait(driver, 15).until(
                                   EC.presence_of_element_located((By.ID, "s-results-list-atf"))
                                   )
                              except:
                                   continue


                              try:
                                        content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']")
                                        data = content.find_elements_by_tag_name("li")
                                        for el in data:

                                             html = el.get_attribute("innerHTML")
                                             soup = BeautifulSoup(html, "html.parser")
                                             lib_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("alt")
                                             url_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).get("href")
                                             img_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("src")
                                             try:
                                                  price_product = soup.findAll("div", {"class": "a-spacing-none"})[2].find("a", {"class": "a-link-normal"}).find("span", {"class": "a-size-base"}).text.replace(u"EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                             except:
                                                  price_product = soup.findAll("div", {"class": "a-spacing-none"})[2].find("a", {"class": "a-link-normal"}).find("span", {"class": "a-color-price"}).text.replace(u"EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                        try:
                                             icon = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("i", {"class": "a-icon-prime"})
                                             livraison = "GRATUITE"
                                             print(livraison)
                                        except:
                                             try:
                                                  _livraison =  soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("span", {"class": "a-size-small"})
                                                  _livraison = _livraison.text.replace(u"+ EUR", "").replace(",", ".").replace(u" Livraison", "")
                                                  livraison = str(float(_livraison.replace(" ", "")) * 658.39)
                                                  print(livraison)
                                             except:
                                                  livraison = ""
                                        print("livraison "+ livraison)
                                        if (price_product == "GRATUIT"):
                                             prix = "0"
                                        elif ("-" in price_product):
                                             p = price_product.split("-")
                                             prix  = float(p[1].replace(" ", "")) * 658.39
                                        else:
                                             prod = price_product.replace(" ", "")
                                             print(prod)
                                             prix = float(prod) * 658.39


                                             print("livraison "+ livraison)
                                             URL.append({
                                             "lib": lib_product,
                                             "url": url_product,
                                             "img": img_product,
                                             "prix": prix,
                                             "categorie": item["categorie"],
                                             "livraison": livraison
                                             })

                                        for link in URL:
                                             driver.get(link["url"])
                                             driver.implicitly_wait(10)
                                             try:
                                                  infos = driver.find_element_by_xpath("//*[@id='prodDetails']").get_attribute("innerHTML")
                                             except NoSuchElementException:
                                                  try:
                                                       infos = driver.find_element_by_xpath("//*[@id='tech-specs-table-left']/tbody").get_attribute("innerHTML")
                                                  except:
                                                       try:
                                                            infos = driver.find_element_by_xpath("//*[@id='product-specification-table']/tbody").get_attribute("innerHTML")
                                                       except:
                                                            try:
                                                                 infos = driver.find_element_by_xpath("//*[@id='detail_bullets_id']").get_attribute("innerHTML")
                                                            except:
                                                                try:
                                                                 infos = driver.find_element_by_xpath("//*[@id='tech-specs-desktop']").text
                                                                except:
                                                                      try:
                                                                           infos = driver.find_element_by_xpath("//*[@id='productDescription_feature_div']").text
                                                                      except:
                                                                           try:
                                                                                infos = driver.find_element_by_xpath("//*[@id='productDetailsTable']/tbody/tr/td").text
                                                                           except:
                                                                                continue


                                             shipping = link["livraison"]
                                             if shipping == "":
                                                  try:
                                                       offer = driver.find_element_by_xpath("//*[@id='buybox-see-all-buying-choices-announce']").get_attribute("href")
                                                       if site not in offer:
                                                            offer = site + offer
                                                       driver.get(offer)
                                                       offer_price = driver.find_element_by_xpath("//*[@id='olpOfferList']/div/div/div[2]/div[1]/p/span/span[1]").text.replace("EUR ", "").replace(",", ".")
                                                       shipping = str(float(offer_price) * 658.39)
                                                  except:
                                                       try:
                                                            offer = driver.find_element_by_xpath("//*[@id='usedbuyBox']/div[1]/div").text.replace(u"+ EUR", "").replace(",",".").replace(u" (livraison)")
                                                            print(offer)
                                                            shipping = str(float(offer) * 658.39)
                                                       except:
                                                            try:
                                                                 offer = driver.find_element_by_xpath("//*[@id='soldByThirdParty']/span[2]").text.replace(u"+ EUR", "").replace(",", ".").replace(u" Livraison", "")
                                                                 shipping = str(float(offer) * 658.39)
                                                            except:
                                                                      shipping = ""


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
                                             "subcategory_id": link["categorie"],
                                             "infos": infos,
                                             "livraison": link["livraison"]
                                             })
                                             cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_vetement')
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
                                        URL = []
                              except:
                                   continue
                              next_url
                              i = i + 1


     return "Script done !"


print(main())

