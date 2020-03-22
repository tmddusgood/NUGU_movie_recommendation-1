'''
영화 줄거리 크롤링 하는 모듈
크롤링 완료 이후에 json파일에 들어가서
파일 제일 마지막 부분 ",}" 에서 ","부분을 지우고 저장할 것
'''

from nugu.movie_story_scrapper.crawling.naver_movie import get_movie_comm as get_comm
import os
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

with open("comm3.json", mode="a+", encoding="utf-8-sig", newline='') as f:
    f.write('{')
with ThreadPoolExecutor(max_workers=5) as executor:
    for i in range(1, 200000):
        executor.submit(get_comm, i)
# with open("comm3.json", mode="a+", encoding="utf-8-sig", newline='') as f:
#     f.write('}')
content = ''
with open("comm3.json", mode="r", encoding="utf-8-sig", newline='') as f:
    content += f.read()
with open("comm3.json", mode="w", encoding="utf-8-sig", newline='') as f:
    f.write(content[:-1] +"}")