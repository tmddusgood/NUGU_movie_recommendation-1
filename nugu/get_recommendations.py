#-*- coding: utf-8 -*-
import sys
import logging
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import pickle
from nugu.movie_story_scrapper.get_recommendations import main as get_story_reco
from nugu.movie_comment_scrapper.get_recommendations import main as get_comm_reco
import pandas as pd
import numpy as np
from datetime import datetime
import json

def get_prsnl_vector(id):
    '''
    get_prsnl_vector: id에 맞는 개인 추천 벡터를 반환해주는 함수

    :param id: user id를 String으로 받음
    :return: user에 대한 개인 추천 벡터를 반환해줌
    '''
    address = 'nugu/movie_story_scrapper/'
    dict_name = 'dict_20191206_1937' # 
    with open(address + dict_name + '.bin', 'rb') as f:
        _dict = pickle.load(f)
    vector = np.zeros(100)
    df = pd.read_csv("nugu/user_log.csv") # id, mid, time으로 구성되어 있음
    count = 0
    for i in range(len(df)): # 모든 user log에 대해서
        if str(df['id'][i]) == id: # 현재 user id에 대한 log라면
            try:
                vector += _dict[str(df['mid'][i])] # 해당 mid를 가지는 영화 벡터를 더해준다.
                count += 1
            except:
                continue
    if count != 0:
        vector = list(np.dot(vector, 1/count)) # 그리고 영화 벡터들의 평균을 구해준다.
    return vector # 그리고 이를 개인 영화 추천 벡터로 삼아 반환해준다.


def get_reco(entity, is_vector, n):
    '''
    get_reco: 추천 알고리즘을 통해서 Top N개의 영화를 추천해주는 함수

    :param entity: 유저가 추천 요청을 한 entity (영화 벡터, 개인 벡터, 장르)
    :param is_vector: 들어온 entity가 벡터 형식인지 아닌지 표시해 주는 flag
    :param n: 추천할 n개의 영화
    :return: 유사도 높은 n개의 영화 제목을 지닌 리스트 반환
    '''
    w_story = 0.4 # 줄거리 유사도에 대한 가중치
    w_comment = 0.6 # 한줄평 유사도에 대한 가중치

    story_sim = get_story_reco(entity, is_vector) # 줄거리에 대한 {영화id: 유사도} 형태의 dict 반환
    comment_sim = get_comm_reco(entity, is_vector) # 한줄평에 대한 {영화id: 유사도} 형태의 dict 반환

    with open('nugu/dict_mid_mname.bin', 'rb') as f: # {영화 id : 영화 제목} 형태의 dict
        ID_dict = pickle.load(f)

    entire_sim = [] # 가중치 계산을 통한 최종 유사도를 저장할 리스트
    try:
        for k, v in comment_sim.items():
            try:
                sim = (w_story * story_sim[k]) + (w_comment * v) # 줄거리 가중치 * 줄거리 유사도 + 한줄평 가중치 *  한줄평 유사도 = 최종 유사도
                entire_sim.append((sim, k))
            except:
                continue
    except:
        return []
    entire_sim.sort(reverse=True) # 유사도 높은 순으로 정렬
    print([(ID_dict[int(x[1])], x[0]) for x in entire_sim[:n]])
    return [ID_dict[int(x[1])] for x in entire_sim[:n]] # 유사도 높은 순으로 영화 제목 n개 반환


def get_reco2(prsnl_vector, reco_entity, include_genre, n):
    '''
    get_reco2: 개인 영화 추천, 장르 추천을 해주는 함수

    :param prsnl_vector: 개인 추천 벡터 (유저의 시청 기록을 토대로 생성된 벡터)
    :param reco_entity: 장르 추천의 경우 장르 이름이 넘어온다. ex) 공포, 드라마, 로맨스, ...
    :param include_genre: 장르 추천인지 아닌지(개인 영화 추천) 판단해주는 (True: 장르 추천, False: 개인 추천)
    :param n: 추천할 n개의 영화
    :return: 유사도 높은 n개의 영화 제목을 지닌 리스트 반환
    '''

    w_story = 0.4 # 줄거리 유사도에 대한 가중치
    w_comment = 0.6 # 한줄평 유사도에 대한 가중치

    story_sim = get_story_reco(prsnl_vector, True) # 개인 추천 벡터에 대해서 줄거리에 대한 {영화id: 유사도} 형태의 dict 반환
    comment_sim = get_comm_reco(prsnl_vector, True) # 개인 추천 벡터에 대해서 한줄평에 대한 {영화id: 유사도} 형태의 dict 반환

    with open('nugu/dict_mid_mname.bin', 'rb') as f: # {영화 id : 영화 제목} 형태의 dict
        ID_dict = pickle.load(f)

    with open('nugu/dict_mid_genre_real_eincluded_1212.bin', 'rb') as f: # {영화 id : [장르]} 형태의 dict
        mid_genre_dict = pickle.load(f)

    entire_sim = [] # 가중치 계산을 통한 최종 유사도를 저장할 리스트
    try:
        for k, v in comment_sim.items():
            try:
                sim = (w_story * story_sim[k]) + (w_comment * v) # 줄거리 가중치 * 줄거리 유사도 + 한줄평 가중치 *  한줄평 유사도 = 최종 유사도
                entire_sim.append((sim, k))
            except:
                continue
    except:
        return []
    entire_sim.sort(reverse=True) # 유사도 높은 순으로 정렬
    if not include_genre: # 만약 개인 추천 요청이라면
        return [ID_dict[int(x[1])] for x in entire_sim[:n]] # 유사도 높은 순으로 영화 제목 n개 반환

    # 장르 추천
    new_sim = entire_sim[:1000] # 개인 추천 벡터와 유사한 1000개의 영화들을 뽑아냄.
    count = 0
    count_list = []
    temp_list = []
    for x in new_sim: # 유사한 1000개의 영화들 중에서
        count = count + 1
        if reco_entity in mid_genre_dict[int(x[1])]: # 유저가 원하는 장르를 가지고 있는 영화를 따로 저장
            temp_list.append(x)
    for item in count_list:
        del new_sim[int(item)]
    return [ID_dict[int(x[1])] for x in temp_list[:n]] # 유사도 높은 순으로 영화 제목 n개 반환


def main(reco_num, reco_entity):
    '''
    main: 추천도가 높은 영화 제목들을 반환해주는 함수
    :param reco_num: 추천 종류 (1: 개인 추천, 2: 장르 추천, 3: 유사 영화 추천)
    :param reco_entity: user가 원하는 추천에 대한 entity
    :return: 추천도에 따른 영화 제목 반환해주는 리스트
    '''
    n = 10 # 추천받을 영화 개수

    if reco_num == '1':  # 개인 추천

        # with open(address + dict_name + '.bin', 'rb') as f:
        #     _dict = pickle.load(f)
        # prsnl_vector = _dict['10001']  # 시네마 천국이 일단은 벡터값으로 들어가게 된다
        prsnl_vector = get_prsnl_vector(reco_entity) #
        return get_reco2(prsnl_vector, reco_entity, False, n)

    elif reco_num == '2':  # 장르 추천
        prsnl_vector = get_prsnl_vector(reco_entity)
        print(prsnl_vector)
        return get_reco2(prsnl_vector, reco_entity, True, n)

    elif reco_num == '3':  # 유사 영화 추천
        return get_reco(reco_entity, False, n)
    else:
        logging.info("잘못된 입력입니다. 1.개인추천 2.장르추천 3.유사영화추천")
    return None


# if __name__ == "__main__":
#     '''
#     python get_recommendations.py {arg 1} {arg 2}
#     [arg 1 : 추천 종류]
#     개인추천 : 1
#     장르추천 : 2
#     유사영화추천 : 3
#
#     [arg 2 : 추천 entity]
#     개인추천 ex) '해당 사람의 ID'
#     장르추천 ex) '공포', '드라마', '스릴러', '액션', ...
#     유사영화추천 ex) '신과함께', '명량', ...
#     '''
#     print(main(sys.argv[1], sys.argv[2]))



