import mysql.connector
import requests

def send():
     PRODUCT = []
     prix = 0
     cnx = mysql.connector.connect(user='root', password='1234@Zerty', host='localhost', database='amazon_total')
     cursor = cnx.cursor(buffered=True)
     sql_statement = "SELECT libProduct, slug, descProduct, priceProduct, imgProduct, numSeller, src, urlProduct, logo, logoS, origin, infos, livraison FROM products"
     cursor.execute(sql_statement)
     result = cursor.fetchall()
     cnx.close()
     cursor.close()
     for item in result:
          if int(item[3]) < 500:
               prix = float(item[3])*658.39
          else:
               prix = float(item[3])
          if item[12] == "GRATUITE":

               PRODUCT.append({
                    "libProduct": item[0],
                    "slug": item[1],
                    "descProduct": item[2],
                    "priceProduct": int(prix),
                    "imgProduct": item[4],
                    "numSeller": item[5],
                    "src": item[6],
                    "urlProduct": item[7],
                    "logo": item[8],
                    "logoS": item[9],
                    "origin": item[10],
                    "infos": item[11],
                    "country": "amz",
                    "provider_fee": 0,
               "subcategory": "none"
               })
          elif item[12] == "":
               PRODUCT.append({
               "libProduct": item[0],
               "slug": item[1],
               "descProduct": item[2],
               "priceProduct": int(prix),
               "imgProduct": item[4],
               "numSeller": item[5],
               "src": item[6],
               "urlProduct": item[7],
               "logo": item[8],
               "logoS": item[9],
               "origin": item[10],
               "infos": item[11],
               "country": "amz",
               "provider_fee": 0,
	          "subcategory": "none"
               })
          else:
               PRODUCT.append({
               "libProduct": item[0],
               "slug": item[1],
               "descProduct": item[2],
               "priceProduct": int(prix),
               "imgProduct": item[4],
               "numSeller": item[5],
               "src": item[6],
               "urlProduct": item[7],
               "logo": item[8],
               "logoS": item[9],
               "origin": item[10],
               "infos": item[11],
               "country": "amz",
               "provider_fee": float(item[12]),
	          "subcategory": "none"
          })



     for data in PRODUCT:

          request = requests.post("http://sn.comparez.co/ads/insert-product/", data = data)
          print(request.json())

     return "success"

print(send())
