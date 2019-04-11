# coding: utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import mysql.connector

def musique():
    add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id, infos, livraison)
                              VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s,%(infos)s, %(livraison)s)""")
    PRODUCT = []
    FIRST_TAB = []
    TAB = []
    options = Options()
    driver = webdriver.Chrome(chrome_options=options, executable_path="../chromedriver/chromedriver", )
    driver.get(u"https://www.amazon.fr/Musique-cd-disques-coffrets-classique-imports-doccasion/b/ref=sd_allcat_dm_cds_vinyl?ie=UTF8&node=301062")
    driver.implicitly_wait(10)
    element = driver.find_element_by_class_name("a-unordered-list").find_elements_by_tag_name("li")
    for _element in element:
        soup = BeautifulSoup(_element.get_attribute("innerHTML"), "html.parser")
        category_parent = soup.find("span", {"class": "a-list-item"}).find("div", {"class": "octopus-pc-category-card-v2-item-block"}).find("a", {"class": "octopus-pc-category-card-v2-category-link"}).get("title")
        link = u"https://www.amazon.fr"+ soup.find("span", {"class": "a-list-item"}).find("div", {"class": "octopus-pc-category-card-v2-item-block"}).find("a", {"class": "octopus-pc-category-card-v2-category-link"}).get("href")
        FIRST_TAB.append({
              "url": link,
              "category_parent": category_parent
         })
    print(FIRST_TAB)
    for link in FIRST_TAB:
         driver.get(link["url"])
         driver.implicitly_wait(10)
         _content = driver.find_element_by_class_name("a-unordered-list").find_elements_by_tag_name("li")
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
                           price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                    except:
                        try:
                           price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                        except:
                            price_product = soup.find("span", {"class": "a-size-small"}).text.replace("EUR", "").replace(",", ".").replace("de ", "")
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
                                print("test___aa")

                                driver.get(link["url"])
                                print(link["url"])
                                driver.implicitly_wait(10)
                                print("start")
                                try:
                                    print("start1")

                                    print("start2")
                                    infos = driver.find_element_by_xpath("//*[@id='prodDetails']").text
                                    print(infos)
                                except:
                                    try:
                                                print("start3")
                                                infos = driver.find_element_by_xpath("//*[@id='tech-specs-table-left']").text
                                                print(infos)
                                    except:
                                        try:
                                                    print("start4")
                                                    infos = driver.find_element_by_xpath("//*[@id='product-specification-table']").text
                                                    print(infos)
                                        except:
                                            try:
                                                        print("start5")
                                                        infos = driver.find_element_by_xpath("//*[@id='detail_bullets_id']").text
                                                        print(infos)
                                            except:
                                                        try:
                                                            print("start6")
                                                            infos = driver.find_element_by_xpath("//*[@id='tech-specs-desktop']").text
                                                            print(infos)
                                                        except:
                                                            try:
                                                                print("start7")
                                                                infos = driver.find_element_by_xpath("//*[@id='productDescription_feature_div']").text
                                                                print(infos)
                                                            except:
                                                                try:
                                                                    print("start8")
                                                                    infos = driver.find_element_by_xpath("//*[@id='productDetailsTable']/tbody/tr/td").text
                                                                    print(infos)
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
                                cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_musique')
                                cursor = cnx.cursor(buffered=True)
                                for data in PRODUCT:
                                        try:
                                            print("Patientez svp en cours d'insertion dans la base de données amazon.....")
                                            cursor.execute(add_produit, data)
                                            cnx.commit()
                                            print('suivant')
                                        except:
                                            continue
                                """
                                        On vide PRODUCT pour éviter les doublons de produits
                                """
                                cursor.close()
                                cnx.close()
                                PRODUCT = []
                                PROD = []
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
                            price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                        except:
                            try:
                                price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                            except:
                                price_product = soup.find("span", {"class": "a-size-small"}).text.replace("EUR", "").replace(",", ".").replace("de ", "")
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
                    cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_musique')
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

                except:
                     print("block")
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
                            price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                        except:
                            price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
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
                                cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_musique')
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
                while(next and j<20):
                    driver.get(next)
                    driver.implicitly_wait(10)
                    try:
                        next = next = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute("href")
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
                                price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                            except:
                                try:
                                    price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                                except:
                                    price_product = soup.find("span", {"class": "a-size-small"}).text.replace("EUR", "").replace(",", ".").replace("de ", "")
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
                                    cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_musique')
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
                    except:
                        try:
                            content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']").find_elements_by_tag_name("li")
                            for i in content:
                                soup = BeautifulSoup(i.get_attribute("innerHTML"), "html.parser")
                                print(i.get_attribute("innerHTML"))

                                lib_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).findAll(
                                    "div", {"class": "a-fixed-left-grid-col"})[0].findAll("a")[0].find("img").get("alt")
                                url_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                    "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].get("href")
                                img_product = soup.find("div", {"class": "s-item-container"}).find("div", {"class": "a-fixed-left-grid"}).find("div", {"class": "a-fixed-left-grid-inner"}).find(
                                    "div", {"class": "a-fixed-left-grid-col"}).findAll("a")[0].find("img").get("src")
                                try:
                                    price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                                except:
                                    try:
                                        price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".").replace("de ", "")
                                    except:
                                        price_product = soup.find("span", {"class": "a-size-small"}).text.replace("EUR", "").replace(",", ".").replace("de ", "")
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
                                    cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_musique')
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
                                    price_product = soup.find("span", {"class": "s-price"}).text.replace("EUR ", "").replace(",", ".")
                                except:
                                    try:
                                        price_product = soup.find("span", {"class": "a-size-base"}).text.replace("EUR ", "").replace(",", ".")
                                    except:
                                        price_product = soup.find("span", {"class": "a-size-small"}).text.replace("EUR", "").replace(",", ".").replace("de ", "")
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
                                    cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_musique')
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
    return "ok"

musique()

