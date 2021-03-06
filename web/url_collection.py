#coding: utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
from Queue import Queue
import threading
from argparse import ArgumentParser
logo="""
u       u          l     |   ccccc  ooooo  l      l     eeeeee  cccccc ttttttt
u       u   r   rr l     |  c      o     o l      l     e      c          t
u       u  r r r   l     |  c      o     o l      l     eeeeee c          t
u       u     r    l     |  c      o     o l      l     e      c          t
u      u u    r    l     |  c      o     o l      l     e      c          t
uuuuuuuu  u   r    lllll |   ccccc  ooooo  llllll lllll eeeeee  cccccc    t
By : Snow wolf
"""
print(logo)
arg = ArgumentParser(description='baidu_url_collect py-script by snowwolf')
arg.add_argument('keyword',help='keyword like inurl:.?id= for searching sqli site')
arg.add_argument('-p','--page', help='page count', dest='pagecount', type=int)
arg.add_argument('-t','--thread', help='the thread_count', dest='thread_count', type=int, default=10)
arg.add_argument('-o','--outfile', help='the file save result', dest='outfile', default='result.txt')
result = arg.parse_args()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

class Bd_url(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self._que = que

    def run(self):
        while not self._que.empty():
            URL = self._que.get()
            try:
                self.bd_url_collect(URL)
            except Exception,e:
                print e
                pass

    def bd_url_collect(self, url):
            r = requests.get(url, headers=headers, timeout=3)
            soup = bs(r.content, 'lxml', from_encoding='utf-8')
            bqs = soup.find_all(name='a', attrs={'data-click':re.compile(r'.'), 'class':None})
            for bq in bqs:
                r = requests.get(bq['href'], headers=headers, timeout=3)
                if r.status_code == 200:
                    print r.url
                    with open(result.outfile, 'a') as f:
                        f.write(r.url + '\n')

def main():
    thread = []
    thread_count = result.thread_count
    que = Queue()
    for i in range(0,(result.pagecount-1)*10,10):
        que.put('https://www.baidu.com/s?wd=' + result.keyword + '&pn=' + str(i))

    for i in range(thread_count):
        thread.append(Bd_url(que))

    for i in thread:
        i.start()

    for i in thread:
        i.join()

if __name__ == '__main__':
    main()
