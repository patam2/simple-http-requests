import re


def get_page(url):
    url = url.split('/', 3)
    if len(url) == 1:
        return url[0]

    if len(url) != 4:
        page = ''
    elif len(url) != 1:
        page = '/' + url[3]

    host = url[2]
    return host

def parse_url(url: str):
    page, port = None, 443
    if url.startswith('http:'):
        port = 80
    if url.startswith('https:'):
        port = 443
  
    host = get_page(url)
    

    return host, port

def parse_request_data(data: bytes) -> dict:
    out = {}
    
    data = data.decode().split('\r\n')
    status_code = re.search('HTTP/1.1 (\d+)', data[0]).group(1)

    for i in data:
        if ':' not in i:
            continue
        key, value = i.split(':', 1)
        out[key.lower()] = value
    return out, status_code

def parse_headers_to_req_data(header:dict) -> str:
    pass


