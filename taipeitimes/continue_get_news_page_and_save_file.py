
from argparse import ArgumentParser
import requests
from bs4 import BeautifulSoup
from get_news_page import crawl_politics_page, get_news_id
import traceback
import json

from collections import deque

job_queue = deque()
news_id_set = set()
first_url = 'https://www.taiwannews.com.tw/en/news/4238383'
job_queue.append(first_url)
news_id_set.add(get_news_id(first_url))

class ArgumentParserError(Exception):
    pass

class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def process_args():
    parser = ThrowingArgumentParser(description="")
    parser.add_argument("-o", "--output_file", default=None, help="")
    return parser.parse_args()

if __name__ == "__main__":

    args = process_args()

    with open(args.output_file, 'wt') as wf:
        while len(job_queue) > 0:
            url = job_queue.popleft()
            try:
                result_json = crawl_politics_page(url, "json")
                wf.write(json.dumps(result_json, ensure_ascii=False) + '\n')
                for related_url in result_json['related_news_url']:
                    news_id = get_news_id(related_url)
                    if news_id not in news_id_set:
                        print(related_url)
                        job_queue.append(related_url)
                        news_id_set.add(news_id)
                print('success', url)
            except Exception:
                print('fail', url)
                pass

