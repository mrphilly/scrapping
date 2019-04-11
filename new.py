 try:
                              while(next_url):
                                   driver.get(next_url)
                                   content = driver.find_element_by_xpath("//*[@id='s-results-list-atf']")
                                   data = content.find_elements_by_tag_name("li")
                                   next_url = driver.find_element_by_xpath("//*[@id='pagnNextLink']").get_attribute('href')
                                   print(link)
                                   for el in data:
                                        driver.implicitly_wait(10) # seconds
                                        lib_product = el.find_element_by_tag_name("h2").get_attribute("data-attribute")
                                        print(lib_product)
                                        url_product = el.find_element_by_tag_name("a").get_attribute("href")
                                        img_product = el.find_element_by_xpath("//div/div[2]/div/div/a/img").get_attribute("src")
                                        price_product = el.find_element_by_xpath("//div/div[6]/div/a/span[2]").text.replace(u"EUR ", "").replace(",", ".") 
                                        print(price_product)
                                        #prix = float(price_product) * 657.10
                                      
                                        PRODUCT.append({
                                        "libProduct": lib_product,
                                        "slug": "",
                                        "descProduct": "",
                                        "priceProduct": price_product,
                                        "imgProduct": img_product,
                                        "numSeller": "",
                                        "src": "https://www.amazon.fr",
                                        "urlProduct": url_product,
                                        "logo": "",
                                        "logoS": "",
                                        "origine": 0,
                                        "subcategory_id": item["categorie"]
                                        })
                                        #print(PRODUCT)

                                   
                                   next_url
                         except:
                              continue