# 편집 거리 알고리즘

import pickle


# kor_begin = 44032
# kor_end = 55203
# chosung_base = 588
# jungsung_base = 28
# jaum_begin = 12593
# jaum_end = 12622
# moum_begin = 12623
# moum_end = 12643
#
# chosung_list = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
#         'ㅅ', 'ㅆ', 'ㅇ' , 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'] # 초성
#
# jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ',
#         'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
#         'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
#         'ㅡ', 'ㅢ', 'ㅣ'] # 중성
#
# jongsung_list = [
#     ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ',
#         'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
#         'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
#         'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'] # 종성
#
# jaum_list = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ',
#               'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ',
#               'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'] # 자음
#
# moum_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
#               'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'] # 모음


def load_from_pickle(_string_name):
    '''
    load_from_pickle : pickle파일에서 영화 id에 대한 영화 벡터를 지니는 dict타입 객체로 반환해주는 모듈

    :param _string_name: pickle 파일 이름
    :return: 영화 id에 대한 영화 벡터를 지니는 dict타입 객체
    '''
    with open(_string_name + '.bin', 'rb') as f:
        _dict = pickle.load(f)
        return _dict


def levenshtein(s1, s2, cost=None, debug=False):
    '''
    levenshtein:

    :param s1: 비교할 단어 1
    :param s2: 비교할 단어 2
    :param cost:
    :param debug:
    :return:
    '''
    if len(s1) < len(s2): # 비교할 첫번째 단어가 두번째 단어보다 길어야 한다.
        return levenshtein(s2, s1, debug=debug) # 첫번째 단어, 두번째 단어 위치를 swap해서 알고리즘 진행

    if len(s2) == 0: # 비교할 두번째 단어가 빈칸일 때
        return len(s1) # 첫번째 단어의 길이만큼 반환

    if cost is None:
        cost = {}

    # changed
    def substitution_cost(c1, c2):
        if c1 == c2: # 만약 c1과 c2 길이가 같다면 cost = 0
            return 0
        return cost.get((c1, c2), 1) # cost dict에 (c1, c2)에 대한 value 반환하거나 없다면 1 반환

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1): # 첫번째 단어에 대해 enumerate
        current_row = [i + 1] # 현재 확인할 row
        for j, c2 in enumerate(s2): # 두번째 단어에 대해 enumerate
            insertions = previous_row[j + 1] + 1 # 바로 위쪽의 cost + 1
            deletions = current_row[j] + 1 # 왼쪽의 cost + 1
            # Changed
            substitutions = previous_row[j] + substitution_cost(c1, c2) # 좌상향(↖) 대각선에 있는 cost (비교하는 알파벳 or 한글 음절이 다를 경우 +1)
            current_row.append(min(insertions, deletions, substitutions)) # 현재 열에 위의 3가지 값 중 최소값을 넣는다.

        # if debug:
        #     print(current_row[1:])

        previous_row = current_row

    return previous_row[-1]


# def compose(chosung, jungsung, jongsung):
#     char = chr(
#         kor_begin +
#         chosung_base * chosung_list.index(chosung) +
#         jungsung_base * jungsung_list.index(jungsung) +
#         jongsung_list.index(jongsung)
#     )
#     return char
#
# def decompose(c):
#     if not character_is_korean(c):
#         return None
#     i = ord(c)
#     if (jaum_begin <= i <= jaum_end):
#         return (c, ' ', ' ')
#     if (moum_begin <= i <= moum_end):
#         return (' ', c, ' ')
#
#     # decomposition rule
#     i -= kor_begin
#     cho  = i // chosung_base
#     jung = ( i - cho * chosung_base ) // jungsung_base
#     jong = ( i - cho * chosung_base - jung * jungsung_base )
#     return (chosung_list[cho], jungsung_list[jung], jongsung_list[jong])
#
# def character_is_korean(c):
#     i = ord(c)
#     return ((kor_begin <= i <= kor_end) or
#             (jaum_begin <= i <= jaum_end) or
#             (moum_begin <= i <= moum_end))
#
# def jamo_levenshtein(s1, s2, debug=False):
#     if len(s1) < len(s2):
#         return jamo_levenshtein(s2, s1, debug)
#
#     if len(s2) == 0:
#         return len(s1)
#
#     def substitution_cost(c1, c2):
#         if c1 == c2:
#             return 0
#         return levenshtein(decompose(c1), decompose(c2))/3
#
#     previous_row = range(len(s2) + 1)
#     for i, c1 in enumerate(s1):
#         current_row = [i + 1]
#         for j, c2 in enumerate(s2):
#             insertions = previous_row[j + 1] + 1
#             deletions = current_row[j] + 1
#             # Changed
#             substitutions = previous_row[j] + substitution_cost(c1, c2)
#             current_row.append(min(insertions, deletions, substitutions))
#         #
#         # if debug:
#         #     pass
#         #     # print(['%.3f'%v for v in current_row[1:]])
#
#         previous_row = current_row
#
#     return previous_row[-1]


def main(_string):
    '''
    main: 주어진 String에 대해서 존재하는 단어 중 편집거리가 가장 짧은 단어 반환
    :param _string: 편집거리를 구할 String
    :return: 영화 제목 중에 가장 편집거리가 짧은 단어 반환
    '''
    address = 'nugu/movie_story_scrapper/'
    dict_name_2 = 'dict_mid_mname'
    mid_mname = load_from_pickle(address + dict_name_2) # {영화 id: 영화제목} dict

    result = []
    weight = []
    weight_dic = {}

    for k, v in mid_mname.items():
        w = 0.01
        s1 = _string # NUGU로 부터 받은 entity
        s2 = str(v) # 현재 루프에서의 영화제목
        e_distance = levenshtein(s1, s2, debug=True) # 편집거리 알고리즘
        if e_distance < 20: # 편집거리가 20 이하인 것들에 대해서
            weight_dic[k] = e_distance # {영화 id: 편집거리} dict

    #print(weight_dic)
    result = min(zip(weight_dic.values(), weight_dic.keys()))
    print(mid_mname[result[1]])
    return mid_mname[result[1]] # 자신을 제외한 편집거리가 가장 짧은 영화 제목 반환

