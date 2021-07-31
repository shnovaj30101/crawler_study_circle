
from argparse import ArgumentParser
import pymysql
pymysql.install_as_MySQLdb()
import json
import pandas as pd
from pandas import json_normalize
from sqlalchemy import create_engine
import sqlalchemy.ext.automap
import sqlalchemy.orm
import sqlalchemy.schema
import jieba
from sqlalchemy.types import Integer, Text, String, DateTime
import cryptography
from pangres import upsert
import getpass
# jieba.enable_paddle()

class ArgumentParserError(Exception):
    pass

class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def process_args():
    parser = ThrowingArgumentParser(description="")
    parser.add_argument("-i", "--input_file", default='data.json', help="")
    parser.add_argument("-t", "--table_name", default='news_table', help="")
    parser.add_argument("-mu", "--mysql_user", default='root', help="")
    parser.add_argument("-mP", "--mysql_password", default=None, help="")
    parser.add_argument("-mh", "--mysql_hostname", default='localhost', help="")
    parser.add_argument("-mp", "--mysql_port", type=int, default=3306, help="")
    parser.add_argument("-md", "--mysql_database", default='news_data', help="")
    return parser.parse_args()

def df_import_sql():
    df = json_normalize(json_data_list)
    df = df.drop(columns=['related_news_url', 'related_news_text'])
    df.set_index('news_id', inplace=True)

    upsert(
        engine = engine,
        chunksize=500,
        df = df,
        table_name = args.table_name,
        if_row_exists = 'ignore',
        dtype={
            'news_id': String(64),
            'title': String(128),
            'source': String(32),
            'url': String,
            # 'url': String(1024),
            'content': String,
            # 'content': String(65535),
            'post_time': DateTime,
            'image_url': String,
            'image_text': String,
            # 'image_url': String(1024),
            # 'image_text': String(1024),
        },
    )

    # df.to_sql(
        # args.table_name,
        # engine,
        # if_exists='append',
        # index=False,
        # chunksize=500,
        # method= 'upsert_ignore',
        # dtype={
            # 'news_id': String(64),
            # 'title': String(128),
            # 'source': String(32),
            # 'url': String,
            # 'content': String,
            # 'post_time': DateTime,
            # 'image_url': String,
            # 'image_text': String,
        # },
    # )
    # input()

if __name__ == "__main__":

    args = process_args()

    if args.mysql_password is None:
        args.mysql_password = getpass.getpass('Password:')

    engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset={5}'.format(args.mysql_user, args.mysql_password, args.mysql_hostname, args.mysql_port, args.mysql_database, 'utf8'), echo=True)
    metadata = sqlalchemy.schema.MetaData(engine)
    print(metadata)

    json_data_list = []

    with open(args.input_file, 'rt') as rf:
        for line in rf:
            line = line.strip()
            if len(line) == 0:
                continue

            json_data_list.append(json.loads(line))

            if len(json_data_list) > 10:
                df_import_sql()
                json_data_list = []

        df_import_sql()




