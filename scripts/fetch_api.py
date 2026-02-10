import urllib.request
r=urllib.request.urlopen('http://127.0.0.1:8000/api/')
print(r.status)
print(r.read().decode('utf-8'))
