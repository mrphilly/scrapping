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
#site = "https://www.amazon.fr"
add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id, infos, livraison)
                              VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s,%(infos)s, %(livraison)s)""")

driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver/chromedriver", )
def livre():
     FIRST_TAB = []
     """ FIRST_TAB = [
          "https://www.amazon.fr/téléphonie-téléphone-portable-smartphone/b?ie=UTF8&node=13910711&ref_=sd_allcat_tele",
          "https://www.amazon.fr/tv-homecinema-barresdeson/b?ie=UTF8&node=13910681&ref_=sd_allcat_tvv",
          "https://www.amazon.fr/s?rh=n%3A682942031%2Cp_72%3A4-&pf_rd_i=682942031&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=e2502c5f-8133-52bb-afae-16814ed13490&pf_rd_r=8JR34MB7FP8W6P5GAANV&pf_rd_s=merchandised-search-10&pf_rd_t=101&ref=Oct_TopRatedC_682942031_SAll",
          "https://www.amazon.fr/appareils-photo-num%C3%A9riques-canon-camescopes/b?ie=UTF8&node=13910691&ref_=sd_allcat_pcam",
          "https://www.amazon.fr/objets-connectes/b?ie=UTF8&node=4551203031&ref_=sd_allcat_obj_con"
     ] """
     TAB = []
     PRODUCT = []
     try:

         #driver = webdriver.Chrome("C:/Users/ibrah/Desktop/scrapping/chromedriver.exe")
         driver.get(u"https://www.amazon.fr/livre-achat-occasion-litterature-roman/b/?ie=UTF8&node=301061&ref_=topnav_storetab_books")
         driver.implicitly_wait(10)
         element = driver.find_element_by_xpath("//*[@id='merchandised-content']/div[4]/div[2]/ul").find_elements_by_tag_name("li")
         for _element in element:
            soup = BeautifulSoup(_element.get_attribute("innerHTML"), "html.parser")
            category_parent = soup.find("span", {"class": "a-list-item"}).find("div", {"class": "octopus-pc-category-card-v2-item-block"}).find("a", {"class": "octopus-pc-category-card-v2-category-link"}).get("title")
            link = u"https://www.amazon.fr"+ soup.find("span", {"class": "a-list-item"}).find("div", {"class": "octopus-pc-category-card-v2-item-block"}).find("a", {"class": "octopus-pc-category-card-v2-category-link"}).get("href")
            FIRST_TAB.append({
                  "url": link,
                  "category_parent": category_parent
             })

         for link in FIRST_TAB:
             driver.get(link["url"])
             driver.implicitly_wait(10)
             try:
                _content = driver.find_element_by_xpath("//*[@id='merchandised-content']/div[4]/div[2]/ul").find_elements_by_tag_name("li")
             except:
                 try:
                    _content = driver.find_element_by_xpath("//*[@id='merchandised-content']/div[3]/div[2]/ul").find_elements_by_tag_name("li")
                 except:
                    _content = driver.find_element_by_xpath("//*[@id='merchandised-content']/div[5]/div[2]/ul")

             for el in _content:
                soup = BeautifulSoup(el.get_attribute("innerHTML"), "html.parser")
                category = soup.find("span", {"class": "a-list-item"}).find("div", {"class": "octopus-pc-category-card-v2-item-block"}).find("a", {"class": "octopus-pc-category-card-v2-category-link"}).get("title")
                url = u"https://www.amazon.fr"+ soup.find("span", {"class": "a-list-item"}).find("div", {"class": "octopus-pc-category-card-v2-item-block"}).find("a", {"class": "octopus-pc-category-card-v2-category-link"}).get("href")
                TAB.append({
                    "url": url,
                    "category": category,
                    "category_parent": link["category_parent"]
                    })
             next = ""
             PROD = []
             for el in TAB:
                site = "https://www.amazon.fr"
                content = []
                driver.get(el["url"])
                driver.implicitly_wait(10)
                try:
                    next = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
                except:
                    next = driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[7]/div/div/div/ul/li[7]/a").get_attribute("href")
                if site not in next:
                    next = site + next
                print(next)
                try:
                    content = driver.find_element_by_xpath("//*[@id='mainResults']/ul").find_elements_by_class_name("s-result-item")
                    for i in content:
                        soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                        lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                            "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("alt")
                        url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                            "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                        img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                            "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                        try:
                               price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                        except:
                               price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",",".").replace(u"\xa0", "")

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
                        PROD.append({
                            "lib": lib_product,
                            "url": url_product,
                            "img": img_product,
                            "prix": price_product,
                            "category": el["category"],
                            "category_parent": el["category_parent"],
                            "livraison": livraison,
                            })
                except:
                    try:
                        content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']").find_elements_by_tag_name("li")
                        for i in content:
                            soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                            lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("alt")
                            url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                            img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                            try:
                                price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                            except:
                                price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
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
                            PROD.append({
                            "lib": lib_product,
                            "url": url_product,
                            "img": img_product,
                            "prix": price_product,
                            "category": el["category"],
                            "category_parent": el["category_parent"],
                            "livraison": livraison,
                            })

                    except:
                         content = driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[3]/div[1]").find_elements_by_tag_name("li")
                         for i in content:
                            soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                            lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("alt")
                            url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                            img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                            try:
                                price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                            except:
                                price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
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
                            PROD.append({
                            "lib": lib_product,
                            "url": url_product,
                            "img": img_product,
                            "prix": price_product,
                            "category": el["category"],
                            "category_parent": el["category_parent"],
                            "livraison": livraison,
                            })
                            print(PROD)
                for link in PROD:
                                print("test")

                                driver.get(link["url"])
                                driver.implicitly_wait(10)

                                try:
                                            infos = driver.find_element_by_xpath("//*[@id='prodDetails']").text

                                except:
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
                                        "subcategory_id": link["category"],
                                        "infos": infos,
                                        "livraison": link["livraison"]
                                })
                                print(PRODUCT)
                                """
                                        PRODUCT contient un produit avec ses information au complet
                                """
                                cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_livre')
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
                                PROD = []
                print(PROD)

                j = 2
                while(next and j<15):
                    driver.get(next)
                    driver.implicitly_wait(10)
                    try:
                        next = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
                    except:
                        try:
                             next = driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[7]/div/div/div/ul/li[7]/a").get_attribute("href")
                        except:
                            break
                    try:
                        content = driver.find_element_by_xpath("//*[@id='mainResults']/ul").find_elements_by_class_name("s-result-item")
                        for i in content:
                            soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                            lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("alt")
                            url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                            img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                            try:
                                price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                            except:
                                price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
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
                            PROD.append({
                            "lib": lib_product,
                            "url": url_product,
                            "img": img_product,
                            "prix": price_product,
                            "category": el["category"],
                            "category_parent": el["category_parent"],
                            "livraison": livraison
                            })

                            print(PROD)
                    except:
                        try:
                            content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']").find_elements_by_tag_name("li")
                            for i in content:
                                soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                                lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                    "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("alt")
                                url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                    "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                                img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                    "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                                try:
                                    price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                except:
                                    price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                if "-" in price_product:
                                    tab = price_product.split("-")
                                    price_product = tab[1]
                                prix = float(str(price_product)) * 655.94
                                if site not in url_product:
                                    url_product = site + url_product
                                PROD.append({
                                "lib": lib_product,
                                "url": url_product,
                                "img": img_product,
                                "prix": price_product,
                                "category": el["category"],
                                "category_parent": el["category_parent"],
                                "livraison": livraison
                                })
                                print(PROD)
                        except:
                            try:
                                content = driver.find_element_by_xpath("//*[@id='search']/div[1]/div[2]/div/span[3]/div[1]").find_elements_by_tag_name("li")
                                for i in content:
                                    soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                                    lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                        "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("alt")
                                    url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                        "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                                    img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                        "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                                    try:
                                        price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                    except:
                                        price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace(u"\xa0", "")
                                    if "-" in price_product:
                                        tab = price_product.split("-")
                                        price_product = tab[1]
                                    prix = float(str(price_product)) * 655.94
                                    if site not in url_product:
                                        url_product = site + url_product
                                    PROD.append({
                                    "lib": lib_product,
                                    "url": url_product,
                                    "img": img_product,
                                    "prix": price_product,
                                    "category": el["category"],
                                    "category_parent": el["category_parent"],
                                    "livraison": livraison,
                                })
                                    print(PROD)
                            except:
                                continue
                    for link in PROD:
                                    print("test 2")
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
                                                                    infos = driver.find_element_by_xpath("//*[@id='productDetailsTable']/tbody/tr/td")
                                                                except:
                                                                    continue


                                    shipping = link["livraison"]

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
                                            "subcategory_id": link["category"],
                                            "infos": infos,
                                            "livraison": link["livraison"]
                                    })
                                    """
                                            PRODUCT contient un produit avec ses information au complet
                                    """
                                    cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_livre')
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
                                    PROD = []


                    j = j + 1
                    next
     except TimeoutException:
         pass

livre()

