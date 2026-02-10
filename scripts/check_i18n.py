import urllib.request, time

url = 'http://127.0.0.1:8000/'

def fetch(lang):
    req = urllib.request.Request(url, headers={'Accept-Language': lang})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, r.read().decode('utf-8')

for lang in ('hi','fr','en'):
    for _ in range(10):
        try:
            status, body = fetch(lang)
            print('\n==== LANG:', lang, 'STATUS:', status, '====\n')
            print(body[:1200])
            break
        except Exception as e:
            time.sleep(0.5)
            continue
print('\nDone')
