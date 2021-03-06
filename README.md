# simple-http-requests
Simple HTTP/S requests with python

```python
>>> sess = reqs.Session('httpbin.org')
>>> sess.get('/get', headers={'1':'2'}).json
{'args': {}, 'headers': {'1': '2', 'Host': 'httpbin.org', ...

>>> sess.post('/post', json={'Hello': 'There'}).status_code
200
```
## Some (small) features:

### Different TLS fingerprint
* Can get past CF sometimes

### Little annoyance eliminated that bothered me with requests
```python
>>> sess = reqs.Session('httpbin.org')
>>> req = sess.get('/get')
>>> print(req)
{
  "args": {},
  "headers": {
    "Host": "httpbin.org",
...
}
```
## Time comparision
### This module
```python
>>> import time
>>> t = time.time()
>>> sess = reqs.Session('https://httpbin.org')
>>> for i in range(15):
>>>  sess.get('/get')
  
>>> time.time() - t
2.36148
```
### Requests
```python
>>> import requests
>>> t = time.time()
>>> for i in range(15):
>>>   requests.get('https://httpbin.org')
>>> time.time() - t
8.34565
