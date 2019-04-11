import mysql.connector

tables = [
     "amazon_db",
     "amazon_livre",
     "amazon_vetement",
     "amazon_moto",
     "amazon_musique",
]

def send():
     PRODUCT = []
     for table in tables:
          cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database= table)
          cursor = cnx.cursor(buffered=True)
          sql_statement = "SELECT libProduct, slug, descProduct, priceProduct, imgProduct, numSeller, src, urlProduct, logo, logoS, origin, subcategory_id, infos, livraison FROM products"
          cursor.execute(sql_statement)
          result = cursor.fetchall()
          cnx.close()
          cursor.close()
          for item in result:
               PRODUCT.append({
                    "libProduct": item[0],
                    "slug": item[1],
                    "descProduct": item[2],
                    "priceProduct": int(item[3]),
                    "imgProduct": item[4],
                    "numSeller": item[5],
                    "src": item[6],
                    "urlProduct": item[7],
                    "logo": item[8],
                    "logoS": item[9],
                    "origine": item[10],
                    "subcategory_id": item[11],
                    "infos": item[12],
                    "livraison": item[13]
               })
          add_produit = ("""INSERT INTO products
                              (libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS, origin,subcategory_id, infos, livraison)
                              VALUES (%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origine)s,%(subcategory_id)s,%(infos)s, %(livraison)s)""")
          cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_total')
          cursor = cnx.cursor(buffered=True)
          for data in PRODUCT:
               try:
                    cursor.execute(add_produit, data)
                    cnx.commit()
                    print('suivant')
               except mysql.connector.Error as e:
                    print(e)


          cursor.close()
          cnx.close()
          PRODUCT = []


print(send())