from gevent import monkey
monkey.patch_all()

import requests
import time
import os
import gevent

base_url = ""
url_list = []
p = 7

def download(url):
    global url_list
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,z;q=0.8'
        }
    filename = './videos/' + url[-p:]
    if os.path.exists(filename) == False:
        with open(filename, "wb") as fp: 
            start =  start = time.time()
            i = 0
            while i < 5:
                try:
                    response = requests.get(url, headers=headers, timeout = 10)
                    break
                except requests.exceptions.RequestException as e:
                    print("{}: {}".format(url[-p:], e))
                    i += 1
                    time.sleep(max(i/2, 1))
            if i >= 5:
                print("{} failed!".format(url[-p:]))
            else:
                fp.write(response.content)
                url_list.remove(url)
                print("{} has finished! URL remains: {}".format(url[-p:], len(url_list)))
    else:
        url_list.remove(url)



if __name__ == "__main__":
    base_url = input("url:")
    base_url = base_url[:-p]
    num = int(input("max:"))
    url_list = [base_url + str(i).zfill(3) + ".ts" for i in range(0, num+1)]
    start = time.time()
    while len(url_list) > 0:
        job_list = [gevent.spawn(download, url) for url in url_list]
        gevent.joinall(job_list)
    print("it works {}s".format(time.time()-start))