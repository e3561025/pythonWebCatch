import requests

with requests.Session() as s:
    r = s.get('https://www.google.com/search?q=cat&oq=cat&aqs=chrome..69i57j0j69i60l2j69i65j69i60.1628j0j7&sourceid=chrome&ie=UTF-8')
    print(r.headers)
    print(r.request.headers)



