import requests
from bs4 import BeautifulSoup
from lxml import etree

def todos_productos(producto):
    lista_titulo = []
    lista_url = []
    lista_precios = []

    siguiente = f'https://listado.mercadolibre.com.pe/{producto}'

    while True:
        r = requests.get(siguiente)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # definimos los Títulos
            titulo = soup.find_all('h2', attrs={'class': 'ui-search-item__title'})
            titulo = [i.text for i in titulo]
            lista_titulo.extend(titulo)
            # Traemos las URL
            urls = soup.find_all('a', attrs={'class': 'ui-search-item__group__element shops-custom-secondary-font ui-search-link'})
            urls = [i.get('href') for i in urls]
            lista_url.extend(urls)
            # Precios
            precio = "//li[@class='ui-search-layout__item']//div[@class='ui-search-result__content-columns shops__content-columns']//div[1]//div[1]//div[1]//div[1]//div[1]//span[1]//span[@class='price-tag-amount']//span[2]"
            dom = etree.HTML(str(soup))
            precios = dom.xpath(precio)
            precios = [i.text for i in precios]
            lista_precios.extend(precios)

            inicial = soup.find('span', attrs={'class': 'andes-pagination__link'}).text
            inicial = int(inicial)

            cantidad = soup.find('li', attrs={'class': 'andes-pagination__page-count'}).get_text().split(' ')
            cantidad = int(cantidad[1])
        else:
            break


        if inicial == cantidad:
            # print(f'Finalizado, se reviso {cantidad} paginas ....')
            break

        siguiente = dom.xpath("//div[@class='ui-search-pagination']//li[contains(@class, '--next')]/a")[0].get('href')

    return lista_titulo, lista_url, lista_precios


def limite_productos(producto, limite):
    lista_titulo = []
    lista_url = []
    lista_precios = []

    siguiente = f'https://listado.mercadolibre.com.pe/{producto}'

    while True:
        r = requests.get(siguiente)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # definimos los Títulos
            titulo = soup.find_all('h2', attrs={'class': 'ui-search-item__title'})
            titulo = [i.text for i in titulo]
            lista_titulo.extend(titulo)
            # Traemos las URL
            urls = soup.find_all('a', attrs={'class': 'ui-search-item__group__element shops-custom-secondary-font ui-search-link'})
            urls = [i.get('href') for i in urls]
            lista_url.extend(urls)
            # Precios
            precio = "//li[@class='ui-search-layout__item']//div[@class='ui-search-result__content-columns shops__content-columns']//div[1]//div[1]//div[1]//div[1]//div[1]//span[1]//span[@class='price-tag-amount']//span[2]"
            dom = etree.HTML(str(soup))
            precios = dom.xpath(precio)
            precios = [i.text for i in precios]
            lista_precios.extend(precios)

            inicial = soup.find('span', attrs={'class': 'andes-pagination__link'}).text
            inicial = int(inicial)

            cantidad = soup.find('li', attrs={'class': 'andes-pagination__page-count'}).get_text().split(' ')
            cantidad = int(cantidad[1])
        else:
            break
        
        if len(lista_titulo) >= int(limite):
            # print(f'Limitado a {limite}')
            return lista_titulo[:limite], lista_url[:limite], lista_precios[:limite]

        if inicial == cantidad:
            # print(f'Finalizado, se reviso {cantidad} paginas ....')
            break
        
        siguiente = dom.xpath("//div[@class='ui-search-pagination']//li[contains(@class, '--next')]/a")[0].get('href')

    return lista_titulo, lista_url, lista_precios