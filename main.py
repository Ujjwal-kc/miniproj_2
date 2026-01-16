import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

BASE_URL = 'https://books.toscrape.com/'

def is_site_available(BASE_URL):

    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response
        else:
            print(f'Failed to fetch website {response.status_code}')
            return None
    except requests.exceptions.RequestException as err:
        print(f'Error Occured {err}')
        return None



url_paths = []


def pagination(response):

    soup = BeautifulSoup(response.content, 'html.parser')
    

    while True:
        yield soup
        next_btn = soup.find('li', class_='next')

        if not next_btn:
            break;

            
        path = next_btn.find('a')['href']

        next_url = urljoin(response.url,path)

        response = requests.get(next_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        



response = is_site_available(BASE_URL)

with open('books.csv', 'w') as csvFile:

    headers = ['Book Name','Price','Stock','Rating']

    csvWriter = csv.writer(csvFile)

    csvWriter.writerow(headers)

    for page in pagination(response):
        for product in page.find_all('article', class_='product_pod'):
            title = product.find('img').get('alt')
            price = product.find('p', class_='price_color').get_text()
            stock = product.find('p', class_='instock').get_text().strip()
            rating = product.find('p', class_='star-rating').get('class')[1]
            csvWriter.writerow([title, price, stock, rating])        






