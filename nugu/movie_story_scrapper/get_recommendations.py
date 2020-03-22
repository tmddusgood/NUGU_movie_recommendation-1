#-*- coding: utf-8 -*-
import json
import pickle
# 유사도를 구하기 위한 라이브러리
from numpy import dot
from numpy.linalg import norm
import numpy as np
from datetime import datetime
# import torch


def load_corpus(_string_name):
    '''
    load_corpus : 영화 별 가지는 (명사, 용언으로 구성된) 단어들이 저장된 json파일에서 dict형식으로 갖고옴

    :param _string_name: json형식의 파일
    :return: 영화id를 key로 가지고, 해당 영화의 단어들 리스트를 value로 가지는 dict타입 객체
    '''
    with open(_string_name, 'r', encoding='utf-8-sig') as json_data:
        _corpus = json.load(json_data) # 영화별 단어 다 들고옴
    return _corpus


def avrgvec_to_dict(_corpus, _model, _vector_dict):
    '''
    avrgvec_to_dict : 각 영화에 대해서 단어 벡터들의 평균벡터를 dict형식으로 반환해 주는 모듈

    :param _corpus: 각 영화에 대해 단어들을 가지고 있는 dict타입 객체
    :param _model: 전체 영화의 명사, 용언에 대한 word2vec모델 (gensim Word2vec model)
    :param _vector_dict: 각 영화id에 대해서 해당 영화를 나타내는 벡터를 지니는 dict타입 객체
    :return: 각 영화id에 대해서 해당 영화 벡터를 가지는 dict타입 객체
    '''
    for i, v in _corpus.items(): # 각각의 영화에 대해서
        vector = np.zeros(100) # 먼저 word2vec모델 벡터의 차원이 100차원이므로, 처음에 100차원의 0벡터로 초기화
        count = 0 # 모두 더한 단어의 개수 (나중에 평균 구할 때 count로 나눠 줄 것임)
        for j in _corpus[i]: # 현재 보고 있는 영화에서의 모든 단어에 대해서
            if len(j) == 1: # 만약 단어 크기가 1이라면
                continue # 넘어감
            try:
                temp = _model.wv[j] # 단어 벡터를 갖고옴
                vector += temp # 단어 벡터 더해줌
                count += 1 # 더한 단어 벡터 카운트해준다.
            except:
                pass
        try:
            my_vector = vector / count # 총 합벡터, 합한 벡터 수, 평균벡터
            _vector_dict[i] = my_vector # 각 영화 id를 key로 하고, 영화벡터를 value로 해서 dict에 저장
        except:
            pass
    return _vector_dict


def save_as_pickle(_dict, _string_name):
    '''
    save_as_pickle : 영화 id에 대한 영화 벡터를 지니는 dict타입 객체를 pickle 파일으로 저장하는 모듈

    :param _dict: 영화 id에 대한 영화 벡터를 지니는 dict타입 객체
    :param _string_name: 저장할 파일 이름
    :return: None
    '''
    with open(_string_name + '.bin', 'wb') as f:
        pickle.dump(_dict, f)

def load_from_pickle(_string_name):
    '''
    load_from_pickle : pickle파일에서 영화 id에 대한 영화 벡터를 지니는 dict타입 객체로 반환해주는 모듈

    :param _string_name: pickle 파일 이름
    :return: 영화 id에 대한 영화 벡터를 지니는 dict타입 객체
    '''
    with open(_string_name + '.bin', 'rb') as f:
        _dict = pickle.load(f)
        return _dict


def cos_sim(A, B):
    '''
    cos_sim : 2개의 벡터에 대해서 코사인 유사도를 반환해주는 모듈

    :param A: 영화 벡터 A
    :param B: 영화 벡터 B
    :return: 영화 벡터 A, B사이의 유사도를 구해서 반환해줌
    '''
    # x = torch.Tensor(A)
    # y = torch.Tensor(B)
    # print(x, y)
    return dot(A, B) / (norm(A) * norm(B))

# def get_similarities_from_title(_string_title, _mid_mname, _vector_dict):
#     '''
#     get_similarities_from_title : 영화
#
#     :param _string_title:
#     :param _mid_mname:
#     :param _vector_dict:
#     :return:
#     '''
#     tmp_id = []
#     sim_score = []
#     for k, v in _mid_mname.items():
#         if str(v) == _string_title:
#             tmp_id.append(k)
#
#     if not len(tmp_id) == 0:
#         mid = tmp_id[0]
#         crt_vec = _vector_dict[str(mid)]
#         for key, value in _vector_dict.items():
#             score = cos_sim(crt_vec, value)
#             sim_score.append([key, score])
#         result = sorted(sim_score, key=lambda sim_score: sim_score[1], reverse=True)
#         # result = result[1:11]
#         return result
#     else:
#         print('NO MATCH!')

def get_similarities(_entity, _mid_mname, _vector_dict, is_vector):
    '''
    get_similarities: 영화 줄거리에 대한 유사도를 구해서 반환해주는 함수

    :param _entity: 추천 entity
    :param _mid_mname: {영화 id: 영화 제목} 을 가지는 dict
    :param _vector_dict: { 영화 id: 영화 벡터 } 를 가지는 dict
    :return:
    '''
    mid = -1
    sim_score = {}
    if is_vector: # 유사도 비교할 entity로 벡터가 왔을 때
        crt_vec = _entity
    else: # entity로 벡터가 아닌 영화 제목으로 왔을 때
        tmp_id = []
        print(datetime.now(), '2.1')
        for k, v in _mid_mname.items():
            if str(v) == _entity: # 동일한 제목을 지닌 영화에 대해서
                tmp_id.append(k) # 영화 id를 저장
        print(datetime.now(), '2.2')

        if not len(tmp_id) == 0:
            mid = tmp_id[0] # 제일 처음에 받은 영화 id에 대해서
            try:
                crt_vec = _vector_dict[str(mid)] # 해당 영화의 벡터를 가져온다.
            except:
                return None
        else:
            print('NO MATCH!')
            return None

    print(datetime.now(), '2.2.1')
    for key, value in _vector_dict.items(): # 모든 영화에 대해서
        if key == str(mid): # 동일한 영화는 제외하고
            continue
        score = cos_sim(crt_vec, value) # consine 유사도를 구한다.
        sim_score[key] = score # {영화 id: 유사도} 저장
        # result = result[1:11]
    print(datetime.now(), '2.3')
    return sim_score # {영화 id: 유사도} 를 지니는 dict 반환



def main(entity, is_vector):
    '''
    main: 줄거리에 대한 유사도를 구해서 {영화 id: 유사도} dict를 반환해주는 함수

    :param entity: 영화 추천 entity (개인 벡터, 영화 벡터...)
    :param is_vector: 벡터인지 아닌지 알려주는 flag (True : 벡터, False : String)
    :return: {영화 id: 유사도} dict
    '''
    vector_dict = {}
    corpus_name = 'comm3.json'
    address = 'nugu/movie_story_scrapper/'
    model_name = 'story_20191205_1654' # 모델 이름
    dict_name = 'dict_20191206_1937'
    dict_name_2 = 'dict_mid_mname'

    # 평균 벡터 구해서 딕셔너리 형태로 저장하는 코드
    # 데이터 부족한 영화는 저장하지 않았음 (count가 0)
    # corpus = load_corpus(corpus_name)
    # model = Word2Vec.load(model_name)  # pre-trained된 word2vec 모델 로드함
    # vector_dict = avrgvec_to_dict(corpus, model, vector_dict)
    # save_as_pickle(vector_dict, dict_name)

    vector_dict = load_from_pickle(address + dict_name) # {영화 id: 영화 벡터} dict
    mid_mname = load_from_pickle(address + dict_name_2) # {영화 id: 영화 제목} dict

    sim_result = get_similarities(entity, mid_mname, vector_dict, is_vector) # 줄거리에 대한 유사도를 계산해주는 함수
    # for mid, score in sim_result:
    #     print(mid_mname[int(mid)], score)

    # print(cos_sim(vector_dict['190254'], vector_dict['10001']))

    return sim_result


# if __name__ == "__main__":
#     # main(sys.argv[1], sys.argv[2])
#     main(sys.argv[1], False)
