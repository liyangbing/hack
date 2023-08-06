# install mysql
apt-get update
#apt-get install -y mysql-server
#service mysql start

# install python 
pip install -r requirements.txt
python -m spacy download zh_core_web_sm


apt-get install libssl-dev
export PYTHONPATH=.:$PYTHONPATH
python database/data_init.py
export OPENAI_API_KEY=
export DID_API_KEY=
