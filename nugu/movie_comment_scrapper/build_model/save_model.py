import pandas as pd
from tqdm import tqdm
from gensim.models.word2vec import Word2Vec
from datetime import datetime

num = 0

tmp_list = []
while True:
    dic = {}
    num += 1
    _filename = './comm_n_and_v_utf8_'+str(num)+'_ordered_q.csv'
    encoding = 'utf-8'
    columns = ['mid', 'mname', 'score', 'genre', 'comments']

    try:
        read = pd.read_csv(_filename, encoding=encoding, header=None, names=columns, low_memory=False)
    except:
        break

    for i in tqdm(range(0, len(read.mid))):
        try:
            temp = [x.strip() for x in read.comments[i].split(',')]
            for j in temp:
                if len(j) == 1:
                    temp.remove(j)
            tmp_list.append(temp)
        except:
            pass

model = Word2Vec(tmp_list, size=100, window=3, min_count=20, workers=50)

model.init_sims(replace=True)
model.save('C:/Users/Yeon/PycharmProjects/SAnalysis/movie_comment_scrapper/comm_'+str(datetime.now()).replace('-', '').replace(' ', '_').replace(':', '')[:13])
del(tmp_list)

