import requests

class A:
    def a(self):
        data=requests.get('https://www.wnacg.org//t2.wnacg.download/data/t/0721/17/15526021386717.jpg')
        stream = data.content
        return stream