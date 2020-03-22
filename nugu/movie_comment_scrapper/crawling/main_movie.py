from nugu.movie_comment_scrapper.crawling.naver_movie import get_movie_comm as get_comm
import os
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


with ThreadPoolExecutor(max_workers=100) as executor: # Thread
    # executor.submit(get_comm, 172816)
    for i in range(1, 200000): # 네이버 고유 영화 ID 1 ~ 200000 까지 크롤링
        executor.submit(get_comm, i)
