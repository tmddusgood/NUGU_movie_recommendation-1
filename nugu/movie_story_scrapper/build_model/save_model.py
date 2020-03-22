#-*- coding: utf-8 -*-

import pandas as pd
from tqdm import tqdm
from gensim.models.word2vec import Word2Vec
from datetime import datetime

import json
with open('comm3.json', 'r', encoding='utf-8-sig') as json_file:
    json_data = json.load(json_file)

model = Word2Vec(list(json_data.values()), size=100, window=3, min_count=20, workers=50)
model.init_sims(replace=True)
model.save('story_'+str(datetime.now()).replace('-', '').replace(' ', '_').replace(':', '')[:13])
del(json_data)