import requests
from bs4 import BeautifulSoup
from lxml import etree

siguiente = f'https://listado.mercadolibre.com.pe/iphone-13'
r = requests.get(siguiente)

soup = BeautifulSoup(r.content, 'html.parser')

lista_url = []

urls = soup.find_all('a', attrs={'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'})
urls = [i.get('href') for i in urls]
lista_url.extend(urls)