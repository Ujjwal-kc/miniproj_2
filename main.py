import requests
from bs4 import BeautifulSoup
import csv


url = 'https://books.toscrape.com/'

response = requests.get(url)

getStatusCode = response.status_code

fileName = 'books.csv'

if getStatusCode != 200:
    print('Failed to fetch the website')
else:
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('article', class_='product_pod')

    with open(fileName, 'w') as csvFile:

        headers = ['Book Name','Price','Rating']
        
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(headers)

        for product in products:
            title = product.find('img')
            price = product.find('p','price_color')
            rating = product.find('p', class_='star-rating')
            csvWriter.writerow([f"{title['alt']}, {price.get_text()}, {rating['class'][1]}"])

