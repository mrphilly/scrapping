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
from selenium.common.exceptions import NoSuchElementException

options = Options()
site = "https://www.amazon.fr"
add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id, infos, livraison)
                              VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s,%(infos)s, %(livraison)s)""")

driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver/chromedriver", )
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
     #tab = getURL()
     #longueur = len(tab) - 80  #43
     PRODUCT = []
     table = []
     next_url = ""
     tab = [
          "https://www.amazon.fr/téléphonie-téléphone-portable-smartphone/b?ie=UTF8&node=13910711&ref_=sd_allcat_tele",
          "https://www.amazon.fr/tv-homecinema-barresdeson/b?ie=UTF8&node=13910681&ref_=sd_allcat_tvv",
          "https://www.amazon.fr/s?rh=n%3A682942031%2Cp_72%3A4-&pf_rd_i=682942031&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=e2502c5f-8133-52bb-afae-16814ed13490&pf_rd_r=8JR34MB7FP8W6P5GAANV&pf_rd_s=merchandised-search-10&pf_rd_t=101&ref=Oct_TopRatedC_682942031_SAll",
          "https://www.amazon.fr/appareils-photo-num%C3%A9riques-canon-camescopes/b?ie=UTF8&node=13910691&ref_=sd_allcat_pcam",
          "https://www.amazon.fr/objets-connectes/b?ie=UTF8&node=4551203031&ref_=sd_allcat_obj_con",
          "https://www.amazon.fr/b/?node=429882031&ref_=Oct_CateC_13921051_4&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7&pf_rd_s=merchandised-search-4&pf_rd_t=101&pf_rd_i=13921051&pf_rd_m=A1X6FK5RDHNB96&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7",
          "https://www.amazon.fr/b/?node=13910721&ref_=Oct_CateC_13921051_8&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7&pf_rd_s=merchandised-search-4&pf_rd_t=101&pf_rd_i=13921051&pf_rd_m=A1X6FK5RDHNB96&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7",
          "https://www.amazon.fr/b/?node=14060591&ref_=Oct_CateC_13921051_9&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7&pf_rd_s=merchandised-search-4&pf_rd_t=101&pf_rd_i=13921051&pf_rd_m=A1X6FK5RDHNB96&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7",
          "https://www.amazon.fr/b?node=13910711&ref_=Oct_CateC_13921051_2&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7&pf_rd_s=merchandised-search-4&pf_rd_t=101&pf_rd_i=13921051&pf_rd_m=A1X6FK5RDHNB96&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7",
          "https://www.amazon.fr/b/?node=13910741&ref_=Oct_CateC_13921051_7&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7&pf_rd_s=merchandised-search-4&pf_rd_t=101&pf_rd_i=13921051&pf_rd_m=A1X6FK5RDHNB96&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_r=J36X0SP7AG1GMB0Q60N1&pf_rd_p=c0925392-063a-5ea8-9ec4-340ef93be5c7",


     ]
     """
          Pour chaque catégories faire
     """
     for item in tab:
          try:
               #reload(sys)
               #sys.setdefaultencoding("utf-8")
               #url = item['url'].replace('%C3%A9', "é").decode('utf-8')
               """
                    Url d'une catégorie
               """
               driver.get(item)
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
                    table.append(element.get_attribute("innerHTML"))
          except NoSuchElementException as e:
               print(e)


          URL = []
          URL_1 = []
          """
               Pour chaque produit trouver ses caractéristiques
          """
          for el in table:
               livraison = ""
               try:

                    html = el
                    soup = BeautifulSoup(html, "html.parser")
                    try:
                         lib_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("alt")
                    except:
                         try:
                              lib_product = el.find_element_by_tag_name("h2").text
                         except:
                              print(soup)
                    url_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).get("href")
                    img_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("src")

                    try:
                         price_product = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("a", {"class": "a-link-normal"}).find("span", {"class": "a-size-base"}).text.replace(u"EUR ", "").replace(",", ".").replace(" ", "").replace(u"\xa0", "")
                    except:
                         try:
                              price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(" ", "").replace(u"\xa0", "")
                         except:
                              price_product = "0"

                    #icon = ""
                    try:
                         icon = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("i", {"class": "a-icon-prime"})
                         if icon != None:
                              livraison = "GRATUITE"
                              print(livraison)
                         else:
                              try:
                                   _livraison =  soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("span", {"class": "a-size-small"})
                                   _livraison = _livraison.text.replace(u"+ EUR", "").replace(",", ".").replace(" ","").replace(u" Livraison", "")
                                   livraison = str(float(_livraison) * 658.39)
                                   print(livraison)
                              except:
                                   livraison = ""


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
                         prix  = float(p[1].replace(" ","")) * 658.39
                    else:
                         print(price_product)
                         print(price_product.replace(" ",""))

                         prod = price_product.replace(u"\xa0", "")
                         print(prod)
                         prix = float(prod) * 658.39
                    if site not in url_product:
                         url_product = site + url_product
                    URL.append({
                         "lib": lib_product,
                         "url": url_product,
                         "img": img_product,
                         "prix": prix,
                         "livraison": livraison
                    })
                    #print(URL)
                    """
                         URL contient toutes les caractéristiques de chaque produit trouvé dans la première page
                    """
               except:
                    continue
                    #break
          """
               On vide ce tableau pour éviter les répétitions de produits
          """
          table = []
          """
               Pour chaque produit contenu dans URL aller vers sa page et trouver ses infos selon le type de page
          """
          for link in URL:
               driver.get(link["url"])
               driver.implicitly_wait(10)
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
                    #"subcategory_id": item["categorie"],
                    "subcategory_id": "",

                    "infos": infos,
                    "livraison": shipping
               })
               """
                    PRODUCT contient un produit avec ses information au complet
               """
               cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon2')
               cursor = cnx.cursor(buffered=True)
               for data in PRODUCT:
                    try:
                         if data["livraison"] != "":
                              print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                              print("Les frais de livraison de ce produit sont: "+ shipping)
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
          while(next_url != None and i < 15):

                    livraison = ""
                    #print("page: " + str(i))
                    #print(next_url)
                    driver.get(next_url)

                    try:
                         next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute('href')
                         if site not in next_url:
                              next_url = site + next_url

                    except NoSuchElementException:
                         next_url = None
                    try:
                         content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']")
                    except:
                         content = driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[3]/div[1]")
                    data = content.find_elements_by_tag_name("li")

                    for el in data:

                                   try:
                                        html = el.get_attribute("innerHTML")

                                        soup = BeautifulSoup(html, "html.parser")
                                        #print(soup)
                                        try:
                                             lib_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("alt")
                                        except:
                                             lib_product = el.find_element_by_tag_name("h2").text
                                        url_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).get("href")
                                        img_product = soup.find("div", {"class": "a-spacing-base"}).find("div", {"class", "a-text-left"}).find("div", {"class": "s-position-relative"}).find("a", {"class": "a-link-normal"}).find("img").get("src")
                                        try:
                                             price_product = soup.findAll("div", {"class": "a-spacing-mini"})[1].find("div", {"class": "a-spacing-none"}).find("a", {"class": "a-link-normal"}).find("span", {"class": "a-size-base"}).text.replace(u"EUR ", "").replace(",", ".").replace(" ", "").replace(u"\xa0", "")
                                        except:
                                             try:
                                                  price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                             except:
                                                  price_product = "0"


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
                                            print(price_product)
                                            print(price_product.replace(" ",""))

                                            prod = price_product.replace(u"\xa0", "")
                                            print(prod)
                                            prix = float(prod) * 658.39
                                        if site not in url_product:
                                             url_product = site + url_product
                                        URL_1.append({
                                             "lib": lib_product,
                                             "url": url_product,
                                             "img": img_product,
                                             "prix": prix,
                                             "livraison": livraison
                                        })

                                   except NoSuchElementException as e:
                                        print(e)
                                        continue

                    next_url
                    i = i + 1
          for link in URL_1:
                         #print(link["url"])
                         driver.get(link["url"])



                         driver.implicitly_wait(10)
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
                              "logoS": "",
                              "src": "https://www.amazon.fr",
                              "urlProduct": link["url"],
                              "logo": "",
                              "origine": 0,
                    #          "subcategory_id": item["categorie"],
                    "subcategory_id": "",

                              "infos": infos,
                              "livraison": shipping
                         })
                         cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon2')
                         cursor = cnx.cursor(buffered=True)
                         for data in PRODUCT:
                              try:
                                   if data["livraison"] != "":
                                        print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                                        print("Les frais de livraison de ce produit sont: "+ shipping)
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
