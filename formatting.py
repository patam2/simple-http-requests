import re


def get_page(url):
    url = url.split('/', 3)
    if len(url) != 4:
        page = ''
    else:
        page = '/' + url[3]

    host = url[2]
    return host, page

def parse_url(url: str):
    page, port = None, 443
    if url.startswith('http:'):
        port = 80
    if url.startswith('https:'):
        port = 443
  
    host, page = get_page(url)
    

    return host, page, port


def parse_request_data(data: bytes) -> dict:
    out = {}
    data = data.decode().split('\r\n')
    for i in data:
        if ':' not in i:
            continue
        
        key, value = i.split(':', 1)
        out[key.lower()] = value
    return out

