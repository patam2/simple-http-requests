import ssl
import socket
import re
import formatting
import time

BLOCKSIZE = 1024 ** 2
ssl_context = ssl.create_default_context()

##sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

####TODO:
#* Connection lost -> refreshing


class Session():
    def __init__(self, url:str) -> None:
        self.host, self.page, self.port = formatting.parse_url(url)
        self.socket_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_session.connect((self.host, self.port))
        if self.port == 443:
            self.socket_session = ssl_context.wrap_socket(
                self.socket_session,
                server_hostname=self.host, 
                server_side=False, 
                do_handshake_on_connect=False
            )

    def get(self, page):
        block_size = 1024 ** 2

        self.socket_session.send(
            f'GET {page} HTTP/1.1\r\n'
            f'Host: {self.host}\r\n\r\n'
            .encode()
        )

        data, received = self.socket_session \
            .recv(block_size) \
            .split(b"\r\n\r\n")

        parsed = formatting.parse_request_data(data)

        #301 checking
        if b'301 Moved Permanently' in data:
            self.socket_session.shutdown(2)

            redirect, page = re.search(
                'Location: http*://(.*)\\r\\n', data.decode()
            ) \
                .group(1) \
                .split('/', 1)

            page = '/' + page
            return self.get(redirect, page)
        
        if int(parsed['content-length']) > len(received):
            while len(received) < parsed['content-length']:
                received += bytes(self.socket_session.recv(1))

        elif b'content-length' not in data.lower():
            while True:
                received += bytes(self.socket_session.recv(block_size))
                if received.endswith(b'\r\n\r\n'):
                    break

        return received.decode()