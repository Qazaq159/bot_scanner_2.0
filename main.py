import requests

def get_data(url):
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding" : "gzip,deflate,br",
        "Accept-Language":"en-US,en;q=0.5",
        "Connection" : "keep-alive",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64;rv: 95.0) Gecko/20100101 Firefox/95.0"
    }

    r = requests.get(url=url, headers=headers)

    with open('index.html', 'w') as file:
        file.write(r.text)

def main():
    get_data('https://jmart.kz/products/1336396/P/')


if __name__ == '__main__':
    main()