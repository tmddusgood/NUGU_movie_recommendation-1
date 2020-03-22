#-*- coding: utf-8 -*-

import re
import MeCab
from datetime import datetime

def save_to_file2(comm_info):
    m = MeCab.Tagger()
    with open("comm3.json", mode="a+", encoding="utf-8-sig", newline='') as f:
        word_list = []
        tagged_str = m.parse(comm_info[0]['story'])
        tagged_str = list(re.split('\t|\n',tagged_str))
        for i in range(1, len(tagged_str), 2):
            if tagged_str[i].startswith('NN') or tagged_str[i].startswith('V'):  # 명사와 용언으로 된 것을 뽑아낸다
                word_list.append(tagged_str[i - 1])
        temp = str({str(comm_info[0]['id']) : word_list}).replace("'", '\"')
        f.write(temp[1:-1]+', ')
    if comm_info[0]['id'] % 2000 == 0:
        print("current id : {}, {}% completed, time : {}".format(comm_info[0]['id'], int(comm_info[0]['id']/2000), datetime.now()))
    return
