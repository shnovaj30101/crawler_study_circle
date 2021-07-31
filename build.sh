BASEDIR=$(dirname "$0")
cd $BASEDIR

if [ ! -e cra_env/ ]; then
    virtualenv -p python3 cra_env/
fi

. cra_env/bin/activate
pip install -r requirements.txt



