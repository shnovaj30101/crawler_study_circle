cd $(dirname $0)

. ../cir_env/bin/activate

python import_data.py -mu u154883630_shnovaj30101 -mh 213.190.6.148 -mp 3306 -md u154883630_news_data
