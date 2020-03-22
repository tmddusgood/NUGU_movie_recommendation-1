import MeCab
import pandas as pd
from tqdm import tqdm
import pickle
from gensim.models.word2vec import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import matplotlib

mc = MeCab.Tagger() # Mecab Tagger
encoding = "utf-8"
columns = ['mid', 'mname', 'score', 'genre', 'comments'] # 영화 id, 영화제목, 평점, 장르, 한줄평
md_path = './model_integrated_full(nouns+vs)'
list_pickle_path = './integrated_nouns_vs_list'
raw_path = './comm_raw_utf8_' #
fixed_path = './comm_fixed_utf8_'
n_and_v_path = './comm_n_and_v_utf8_'


def parse_Nouns_Vs(_text):
    '''
    parse_Nouns_Vs : 한줄평을 받아와서 명사와 용언을 뽑아내는 함수
    :param _text: 한줄평(str)
    :return: 명사(Noun)과 용언(Verb)을 가지는 리스트
    '''
    _answer = []
    _list = _text.split()
    for i in range(1, len(_list), 2):
        if _list[i].startswith('NN') or _list[i].startswith('V'): # 명사와 용언으로 된 것을 뽑아낸다
            _answer.append(_list[i-1])
    return _answer # 명사와 용언을 포함하는 리스트 반환

def readcsv(_filename):
    '''
    readcsv : 해당 위치의 csv파일을 DataFrame타입 객체로 반환
    :param _filename: csv파일 위치
    :return: DataFrame객체
    '''
    _read = pd.read_csv(_filename, encoding=encoding, header=None, names=columns, low_memory=False)
    return _read

def try_and_fix(_read, _ecount):
    '''
    try_and_fix :
    :param _read:
    :param _ecount:
    :return:
    '''
    _error = []
    for item in tqdm(_read.comments):
        try:
            _ecount += 1
            mc.parse(item)
        except:
            _error.append(_ecount)
    for i in range(len(_error)):
        _error[i] = int(_error[i]) - 1
    _read = _read.drop(_error, 0)
    return _read


def fixed_to_nandvs(_read):
    _tmp_list = []
    for item in tqdm(_read.comments):
        try:
            mc.parse(item)
            tmp_str = mc.parse(item)
            _tmp_list.append(parse_Nouns_Vs(tmp_str))
        except:
            pass
    _read.comments = _tmp_list
    return _read


def csv_preprocessing(_process):
    '''

    :param _process:
    :return:
    '''
    num = 0
    tmp_list = []
    if _process == 'error_fix':
        for i in tqdm(range(0, 8)):
            ecount = 0
            num = str(int(num) + 1)  # 파일 여러 개에 일괄 적용하기 위해서 넣은 카운트
            filename = raw_path + str(num) + ".csv"
            filename2 = fixed_path + str(num) + '.csv'

            read = readcsv(filename)
            read = try_and_fix(read, ecount)
            read.to_csv(filename2, encoding='utf-8', header=None, index=False)
    elif _process == 'extract_Nouns&Vs':
        for i in tqdm(range(0, 8)):
            num = str(int(num) + 1) # 파일 여러 개에 일괄 적용하기 위해서 넣은 카운트
            filename2 = fixed_path + str(num) + '.csv'
            filename3 = n_and_v_path + str(num) + '.csv'

            read = readcsv(filename2)
            read = fixed_to_nandvs(read)
            read.to_csv(filename3, encoding='utf-8', header=None, index=False)


def integrate_csv_pickle():
    num = 0
    tmp_list = []
    for i in tqdm(range(0, 8)):
        num = str(int(num) + 1)  # 파일 여러 개에 일괄 적용하기 위해서 넣은 카운트
        filename = n_and_v_path + str(num) + '.csv'
        read = readcsv(filename)
        for i in tqdm(range(0, len(read.comments))):
            tmp_list.append(read.comments[i])
    print(tmp_list)
    with open(list_pickle_path, 'wb') as f:
        pickle.dump(tmp_list, f)


def pickle_to_model(_tmp_list):
    with open(list_pickle_path, 'rb') as f:
        _tmp_list = pickle.load(f)  # 단 한줄씩 읽어옴
    print(_tmp_list)
    # model = Word2Vec(tmp_list, size=100, window=3, min_count=20, workers=50)
    # model.init_sims(replace=True)
    # model.save(md_path)


def plot_2d_graph(vocabs, xs, ys):
    plt.figure(figsize=(8,6))
    plt.scatter(xs, ys, marker ='o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))
    plt.show()


def model_application():
    model = Word2Vec.load(md_path)
    model.most_similar('영화')


def model_configuration():
    font_name = matplotlib.font_manager.FontProperties(
                    fname="C:/Windows/Fonts/gulim.ttc"  # 한글 폰트 위치를 넣어주세요
                ).get_name()
    matplotlib.rc('font', family=font_name)

    model = Word2Vec.load(md_path)
    word_vectors = model.wv
    vocabs = word_vectors.vocab.keys()
    word_vectors_list = [word_vectors[v] for v in vocabs]

    pca = PCA(n_components=2)
    xys = pca.fit_transform(word_vectors_list)
    xs = xys[:, 0]
    ys = xys[:, 1]

    plot_2d_graph(vocabs, xs, ys)


if __name__ == "__main__":
    print('nothingxc')