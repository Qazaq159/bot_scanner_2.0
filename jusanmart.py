import requests


class Product:
    def __init__(self, link):
        self.shop = None
        self.price = None
        self.name = None
        link = link.split('products')[1].split('/')
        self.id = link[1]
        self.main()

    def get_json(self, url):
        response = requests.get(url)
        return response.json()

    def main(self):
        tovar = self.get_json(f'https://jmart.kz/gw/catalog/v1/products/offers/{self.id}')
        self.name = self.get_json(f'https://jmart.kz/gw/catalog/v1/products/{self.id}')['data']['product']
        self.shop = tovar['data']['offers'][0]['company_name']
        self.price = tovar['data']['offers'][0]['price_formatted']['price']

    def __str__(self):
        return self.name + '\n' + self.shop + ': ' + self.price