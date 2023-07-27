pip install -r requirements.txt
python -m spacy download zh_core_web_sm
apt-get install libssl-dev
export PYTHONPATH=/mnt/data/hack:$PYTHONPATH
python /mnt/data/hack/database/data_init.py
export OPENAI_API_KEY=
export DID_API_KEY=
