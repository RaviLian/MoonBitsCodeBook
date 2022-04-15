import requests
import re

class Spyder:
    def __init__(self, fn):
        """
        ptype: fn -> filename string
        """
        self.filename = fn
    def download(self, url):
        """
        ptype: url -> str
        rtype: str
        """
        req = requests.get(url)
        return req.text

    def extract(self, content, pattern):
        """
        ptype: content str
        ptype: pattern str regex
        rtype: List
        """
        result = re.findall(pattern, content)
        return result

    def save(self, info):
        with open(self.filename, 'a+') as f:
            for item in info:
                f.write(' '.join(item) + '\n')

    def crawl(self, url, pattern):
        content = self.download(url)
        info = self.extract(content, pattern)
        self.save(info)


b_crawler = Spyder('douban_new.txt')
content = b_crawler.download('https://www.bilibili.com/v/popular/all')
print(content)
