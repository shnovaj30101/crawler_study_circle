
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
from sqlalchemy.types import Integer, Text, String, DateTime
import cryptography

class ArgumentParserError(Exception):
    pass

class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def process_args():
    parser = ThrowingArgumentParser(description="")
    parser.add_argument("-o", "--output_file", default='export_data.json', help="")
    return parser.parse_args()

if __name__ == "__main__":

    args = process_args()

    table_name = 'news_table'

    engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset={5}'.format('root', 'password', 'localhost', 3306, 'news_data', 'utf8'), echo=True)

    sql_cmd = 'select * from {};'.format(table_name)

    df = pd.read_sql_query(sql_cmd, engine)

    with open(args.output_file, 'wt') as wf:
        result_json_str = df.to_json(orient='records')
        result_json = json.loads(result_json_str)

        for json_item in result_json:
            wf.write(json.dumps(json_item, ensure_ascii=False)+'\n')

