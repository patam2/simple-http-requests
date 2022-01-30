import ssl
import socket
import formatting
import json as jsonmodule

BLOCKSIZE = 1024**2

####TODO:
# * Connection lost -> refreshing


class Response:
    def __init__(self, body, headers, status_code) -> None:
        self.headers = headers
        self.body = body
        self.status_code = int(status_code)

    @property
    def cookies(self):
        if "set-cookie" in self.headers:
            return self.headers["set-cookie"]
        else:
            return None

    @property
    def json(self):
        return jsonmodule.loads(self.body)


class Session:
    def __init__(self, url: str) -> None:
        self.host, self.port = formatting.parse_url(url)
        self.socket_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_session.connect((self.host, self.port))
        if self.port == 443:
            self.socket_session = ssl.wrap_socket(
                self.socket_session,
                server_side=False,
                do_handshake_on_connect=False,
                ssl_version=ssl.PROTOCOL_TLSv1_2,
            )

    def request(self, method, page, headers={}, json=None):
        method, body = method.upper(), ""
        message = f"{method} {page} HTTP/1.1\r\nHost: {self.host}\r\n"

        if method == "POST":
            headers["content-length"] = len(str(json))
            headers["content-type"] = "application/json"
            body = str(json)

        if isinstance(headers, dict) and len(headers) != 0:
            for i, k in headers.items():
                message += f"{i}: {k}\r\n"
    
        if body != '':
            message += "\r\n" + body + "\r\n\r\n"
        else:
            message += '\r\n'
        self.socket_session.send(message.encode())

        data, received = self.socket_session.recv(BLOCKSIZE).split(b"\r\n\r\n", 1)
        headers, status_code = formatting.parse_request_data(data)
        # 301 checking

        if b"301 Moved Permanently" in data or b"308 Permanent Redirect" in data:
            redirect = headers["location"]
            parsed = formatting.parse_url(redirect)
            self.host = parsed[0]
            return self.request(method, parsed[1], headers)
        if "content-length" not in headers:
            while True:
                received += bytes(self.socket_session.recv(BLOCKSIZE))
                if received.endswith(b"\r\n\r\n"):
                    break
        elif int(headers["content-length"]) > len(received):
            content_length = int(headers["content-length"])
            while len(received) < content_length:
                received += bytes(self.socket_session.recv(content_length))
        return Response(received.decode(), headers, status_code)

    def get(self, page, headers={}):
        return self.request("get", page, headers)

    def post(self, page, headers={}, json=None):
        return self.request("post", page, headers, json)
