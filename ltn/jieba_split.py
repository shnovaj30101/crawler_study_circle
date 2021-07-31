
from argparse import ArgumentParser
import jieba
import json

class ArgumentParserError(Exception):
    pass

class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def process_args():
    parser = ThrowingArgumentParser(description="")
    parser.add_argument("-i", "--input_file", default='data.json', help="")
    parser.add_argument("-o", "--output_file", default='output_data.json', help="")
    return parser.parse_args()


if __name__ == "__main__":

    args = process_args()

    with open(args.input_file, 'rt') as rf, open(args.output_file, 'wt') as wf:
        for line in rf:
            line = line.strip()
            if len(line) == 0:
                continue

            json_data = json.loads(line)
            json_data['title'] = ' '.join(jieba.cut(json_data['title'], cut_all=False, HMM=True))
            json_data['content'] = ' '.join(jieba.cut(json_data['content'], cut_all=False, HMM=True))

            wf.write(json.dumps(json_data, ensure_ascii=False) + '\n')


