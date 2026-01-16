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


response = is_site_available(BASE_URL)


url_paths = []


def get_paths(response):

    soup = BeautifulSoup(response.content, 'html.parser')
    

    while True:
        
        next_btn = soup.find('li', class_='next')

        if not next_btn:
            break;

            
        path = next_btn.find('a')['href']
        url_paths.append(path)

        next_url = urljoin(response.url,path)

        response = requests.get(next_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        


get_paths(response)
print(url_paths)





