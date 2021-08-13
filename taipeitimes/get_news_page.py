# @Author: shnovaj30101@gmail.com
# @createTime: 2019/7/19
#
# python version: 3.5.2
# 預先安裝模組: requests, bs4
# 安裝指令:
# $ pip install requests
# $ pip install pip install BeautifulSoup

#
# Object:
# 建構一個 python 模組, 抓取自由時報網站下的政治文章
# 抓取的資料類別:
#     url, 標題, 發佈時間, 圖片url, 圖片註解, 文章, 相關新聞url, 相關新聞標題
#

import requests # 處理 http request, response module
from bs4 import BeautifulSoup # 對一個 html source code 做結構化處理
import html
import json
from datetime import datetime


def parse_politics_page_by_text(url, soup):
    output_text = ''

    # 抓取 url
    # ===================================
    output_text += 'url:\t'
    output_text += url + '\n'

    # 抓取標題
    # ===================================
    output_text += 'title:\t'
    title_elem = soup.select_one('div.archives h1')
    # output_text += title_elem.string.strip() + ' ------ '
    # subtitle_elem = soup.select_one('div.archives h3')
    output_text += title_elem.string.strip() + '\n'

    # 抓取發佈時間
    # ===================================
    output_text += 'post_time:\t'
    post_time_elem = soup.select_one('div.where + h6')
    post_time_elem_text = post_time_elem.string.strip()
    post_time_raw_text = post_time_elem_text.rsplit(None, 1)[0]
    post_time_text = datetime.strptime(post_time_raw_text, "%a, %b %d, %Y").strftime("%Y/%m/%d")
    output_text += post_time_text + '\n'

    # 抓取圖片url
    # ===================================
    output_text += 'image_url:\t'
    img_url_elem = soup.select_one('div.imgboxa img')

    if img_url_elem is None:
        output_text += '\n'
    else:
        output_text += img_url_elem['src'] + '\n'

    # 抓取圖片註解
    # ===================================
    output_text += 'image_text:\t'
    img_text_elem = soup.select_one('div.imgboxa h1')

    if img_text_elem is None:
        output_text += '\n'
    else:
        output_text += html.unescape(img_text_elem.string) + '\n'

    # 抓取文章
    # ===================================
    output_text += 'content:\t'
    article_elem_list = soup.select('div.archives > p')

    for article_elem in article_elem_list:
        article_string = article_elem.getText()
        if article_string is not None:
            output_text += html.unescape(article_string).strip() + '\n'

    # related_news_elem_list = soup.select('div.related-words a')

    # # 抓取相關新聞url
    # # ===================================
    # output_text += 'related_news_url:\n'

    # for one_news_elem in related_news_elem_list:
        # output_text += 'https://www.taiwannews.com.tw' + one_news_elem['href'] + '\n'

    # # 抓取相關新聞標題
    # # ===================================
    # output_text += 'related_news_text:\n'

    # for one_news_elem in related_news_elem_list:
        # output_text += one_news_elem['title'] + '\n'

    return output_text

def get_news_id(url):
    return url.split('/')[-1]

def parse_politics_page_by_json(url, soup):
    output_json = {}

    # 抓取 url
    # ===================================
    output_json['url'] = url

    # 抓取 news_id
    # ===================================
    output_json['news_id'] = 'taipeitimes_{0}'.format(get_news_id(url))

    # 抓取 source
    # ===================================
    output_json['source'] = 'taipeitimes'

    # 抓取標題
    # ===================================
    title_elem = soup.select_one('div.archives h1')
    output_json['title'] = title_elem.string.strip()

    # 抓取發佈時間
    # ===================================
    post_time_elem = soup.select_one('div.where + h6')
    post_time_elem_text = post_time_elem.string.strip()
    post_time_raw_text = post_time_elem_text.rsplit(None, 1)[0]
    post_time_text = datetime.strptime(post_time_raw_text, "%a, %b %d, %Y").strftime("%Y/%m/%d")
    output_json['post_time'] = post_time_text

    # 抓取圖片url
    # ===================================
    img_url_elem = soup.select_one('div.imgboxa img')

    if img_url_elem is None:
        output_json['image_url'] = ''
    else:
        output_json['image_url'] = img_url_elem['src']

    # 抓取圖片註解
    # ===================================
    img_text_elem = soup.select_one('div.imgboxa h1')

    if img_text_elem is None:
        output_json['image_text'] = ''
    else:
        output_json['image_text'] = html.unescape(img_text_elem.string)

    # 抓取文章
    # ===================================
    output_json['content'] = ''
    article_elem_list = soup.select('div.archives > p')

    for article_elem in article_elem_list:
        article_string = article_elem.getText()
        if article_string is not None:
            output_json['content'] += html.unescape(article_string).strip() + '\n'

    # related_news_elem_list = soup.select('div.related-words a')

    # # 抓取相關新聞url
    # # ===================================
    # output_json['related_news_url'] = []

    # for one_news_elem in related_news_elem_list:
        # output_json['related_news_url'].append('https://www.taiwannews.com.tw' + one_news_elem['href'])

    # # 抓取相關新聞標題
    # # ===================================
    # output_json['related_news_text'] = []

    # for one_news_elem in related_news_elem_list:
        # output_json['related_news_text'].append(one_news_elem['title'])

    return output_json

def crawl_politics_page(url, fmt="text"):
    '''
    目的：
    給定一個ltn politics url, 傳回此url內的重要新聞資訊

    參數說明：
    url: 待抓取的新聞url
    fmt: 有分兩種格式: "text" or "json"
         text 會回傳string型式的新聞資訊, 適合直接以print的方式檢視
         json 會回傳dict型式的新聞資訊, 適合用在程式的二度處理
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    }

    res = requests.get(url, headers = headers)
    res.encoding = 'utf8'

    soup = BeautifulSoup(res.text, 'html.parser')

    if fmt == "text":
        return parse_politics_page_by_text(url, soup)

    if fmt == "json":
        return parse_politics_page_by_json(url, soup)

if __name__ == "__main__":

    url_list = [ # test crawling url list
            'https://www.taipeitimes.com/News/front/archives/2021/07/31/2003761763',
            'https://www.taipeitimes.com/News/sport/archives/2021/07/28/2003761590',
            'https://www.taipeitimes.com/News/sport/archives/2021/07/25/2003761414',
            'https://www.taipeitimes.com/News/feat/archives/2021/07/26/2003761461',
    ]

    for url in url_list:
        print(crawl_politics_page(url, "text"))
        print('==========================================================')
        print(json.dumps(crawl_politics_page(url, "json"), indent=4, ensure_ascii=False))
        print('==========================================================')


