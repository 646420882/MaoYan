#coding+utf-8
import requests
import json
import re
from multiprocessing import Pool


titles = []
scores = []
def get_html(url):
    header={"User-Agent":":Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    try:
        r = requests.get(url,headers=header)
        return r.text
    except:
        print(r.status_code)
def parse(html):
    # pattern = re.compile('<dd>.*?class="channel-detail movie-item-title" title="(.*?)">.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>.*?</dd>', re.S)
    pattern = re.compile('<dd>.*?<div class="channel-detail movie-item-title" title="(.*?)">.*?</div>.*?<i class="integer">(.*?)</i><i class="fraction">(.*?)</i>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '标题': item[0],
            '评分': item[1] + item[2]
        }
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
def main(offset):
    sordID = 1
    # sordID = input("1按热门排序\n2按时间排序\n3按评分排序\n")
    url = "http://maoyan.com/films?sortId=%s&offset=%s"%(sordID,offset)
    html = get_html(url)
    for item in parse(html):
        print(item)
        write_to_file(item)

if __name__=="__main__":
    page = 10  # 抓取页数
    pool = Pool()
    pool.map(main,[i*30 for i in range(page)])
    pool.close()
    pool.join()



