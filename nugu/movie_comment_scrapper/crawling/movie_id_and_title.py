import pandas as pd
# from tqdm import tqdm
#
# _filename = './comm_n_and_v_utf8_1_ordered_q.csv'
# encoding = 'utf-8'
# columns = ['mid', 'mname', 'score', 'genre', 'comments']
#
# read = pd.read_csv(_filename, encoding=encoding, header=None, names=columns, low_memory=False)
# tmp_mid = 0
#
# list0 = ['a', 'a', 'a', 'b']
# list1 = [['a', 'b', 'c'], ['d', 'e', 'f'], ['a', 'b', 'c'], ['d', 'e', 'f']]
#
# count = 0
# mid_list = []
# for i in tqdm(range(0, len(read.mid))):
#     try:
#         if not read.mid[i] == read.mid[i+1]:
#             mid_list.append(count)
#     except:
#         pass
#     count += 1
# print(mid_list)
# for i in range(1, int(mid_list[0]) + 1):
#     read.comments[0].extend(read.comments[i])
#
# for i in tqdm(range(0, len(mid_list))):
#     for j in range(int(mid_list[i]) + 1, int(mid_list[i+1]) + 1):
#         if j == int(mid_list[i] + 1):
#             pass
#         else:
#             read.comments[int(mid_list[i]) + 1] = ', '.join([str(read.comments[int(mid_list[i]) + 1]), str(
#                 read.comments[j])])
#             # read.comments[int(mid_list[i]) + 1] = str(read.comments[int(mid_list[i]) + 1]) + ', ' + str(read.comments[j])
#             read.comments[j] = ''
#     print(read.comments[int(mid_list[i]) + 1])
#
# print(read.comment)


import pandas as pd
from tqdm import tqdm

# _filename = './comm_n_and_v_utf8_1_ordered_q.csv'
# encoding = 'utf-8'
# columns = ['mid', 'mname', 'score', 'genre', 'comments']
#
# read = pd.read_csv(_filename, encoding=encoding, header=None, names=columns, low_memory=False)
# tmp_mid = 0
#
# list0 = ['a', 'a', 'a', 'b']
# list1 = [['a', 'b', 'c'], ['d', 'e', 'f'], ['a', 'b', 'c'], ['d', 'e', 'f']]
#
# count = 0


# for i in tqdm(range(0, len(read.mid))):
#     try:
#         if not read.mid[i] == read.mid[i+1]:
#             mid_list.append(count)
#     except:
#         pass
#     count += 1
# print(mid_list)
# for i in range(1, int(mid_list[0]) + 1):
#     read.comments[0].extend(read.comments[i])
#
# for i in tqdm(range(0, len(mid_list))):
#     for j in range(int(mid_list[i]) + 1, int(mid_list[i+1]) + 1):
#         if j == int(mid_list[i] + 1):
#             pass
#         else:
#             read.comments[int(mid_list[i]) + 1] = ', '.join([str(read.comments[int(mid_list[i]) + 1]), str(
#                 read.comments[j])])
#             # read.comments[int(mid_list[i]) + 1] = str(read.comments[int(mid_list[i]) + 1]) + ', ' + str(read.comments[j])
#             read.comments[j] = ''
#     print(read.comments[int(mid_list[i]) + 1])
#
# print(read.comment)

import pickle

mid_mname_vec = {}

for _number in tqdm(range(1, 9)):
    _filename = './comm_n_and_v_utf8_' + str(_number) + '_ordered_q.csv'
    encoding = 'utf-8'
    columns = ['mid', 'mname', 'score', 'genre', 'comments']

    read = pd.read_csv(_filename, encoding=encoding, header=None, names=columns, low_memory=False)

    for i in tqdm(range(len(read.mid) - 1)):
        try:
            if not read.mid[i] == read.mid[i+1]:
                mid_mname_vec[int(read.mid[i])] = read.mname[i]
        except:
            pass

with open('../dict_mid_mname.bin', 'wb') as f:
    pickle.dump(mid_mname_vec, f)
