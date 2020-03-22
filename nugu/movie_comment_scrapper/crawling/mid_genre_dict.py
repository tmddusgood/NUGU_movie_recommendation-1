import pandas as pd
from tqdm import tqdm
import pickle
import re

# mid_genre_vec = {}
#
# for _number in tqdm(range(1, 9)):
#     _filename = './comm_n_and_v_utf8_' + str(_number) + '_ordered_q.csv'
#     encoding = 'utf-8'
#     columns = ['mid', 'mname', 'score', 'genre', 'comments']
#
#     read = pd.read_csv(_filename, encoding=encoding, header=None, names=columns, low_memory=False)
#
#     for i in tqdm(range(len(read.mid) - 1)):
#         try:
#             if not read.mid[i] == read.mid[i+1]:
#                 mid_genre_vec[int(read.mid[i])] = read.genre[i]
#         except:
#             pass
#
#
# with open('../dict_mid_genre.bin', 'wb') as f:
#     pickle.dump(mid_genre_vec, f)
#
# print(mid_genre_vec)

# mid_genre_dict = {}
# with open('../dict_mid_genre.bin', 'rb') as f:
#     raw_data = pickle.load(f)
#
# for k, v in tqdm(raw_data.items()):
#     mid_genre_dict[k] = re.findall(r"[\w']+", str(v))
#
# with open('../dict_mid_genre_real_eincluded.bin', 'wb') as f:
#     pickle.dump(mid_genre_dict, f)

temp_list = ["world", 'hello']
if 'world' in temp_list:
    print('hi')
else:
    print('sdfsdf')
# print(temp_list.index("world!"))

address = '../movie_story_scrapper/'
model_name = 'story_20191205_1654'  # 모델 이름
dict_name = 'dict_20191206_1937'  # 수정할것
dict_name_2 = 'dict_mid_mname'  # 수정할 것

with open(address + dict_name + '.bin', 'rb') as f:
    _dict = pickle.load(f)

print(_dict['10001'])
