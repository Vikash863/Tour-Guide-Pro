import urllib.request, urllib.parse, http.cookiejar

BASE = 'http://127.0.0.1:8000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def get_csrf():
    opener.open(BASE + '/')
    for c in cj:
        if c.name == 'csrftoken':
            return c.value
    return None

def set_lang(lang):
    csrf = get_csrf()
    print('CSRF token:', csrf)
    data = urllib.parse.urlencode({'language': lang, 'next': '/'}).encode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': BASE + '/',
    }
    if csrf:
        headers['X-CSRFToken'] = csrf
    req = urllib.request.Request(BASE + '/i18n/setlang/', data=data, headers=headers)
    resp = opener.open(req)
    print('setlang response:', resp.getcode())
    # show cookies
    cookies = {c.name: c.value for c in cj}
    print('Cookies after setlang:', cookies)
    r = opener.open(BASE + '/')
    body = r.read().decode('utf-8')
    print('\n--- Home page snippet (lang=%s) ---' % lang)
    print(body[:800])

for lang in ('hi','fr'):
    print('\n=== Switching to', lang, '===')
    set_lang(lang)

print('\nDone')
