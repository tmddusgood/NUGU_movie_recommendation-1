import requests
from bs4 import BeautifulSoup
import time
from nugu.movie_comment_scrapper.crawling.csv_save import save_to_file
from tqdm import tqdm


def get_last_page(M_ID):
    URL = f"https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword={M_ID}&target=after"
    # 한줄평 페이지 주소
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "h5_right_txt"})
    if pagination:
        num = pagination.find("strong").string
        max_page = int(num) / 10 + 1
        return int(max_page) # 마지막 페이지 반환
    else:
        return None


def extract_comm(html, title, genre, mid): # 한줄평 1개 추출하는 함수
    comment = html.get_text('|', strip=True).split('|')[3]
    score = html.find("em").string
    return {'mid': mid, 'title': title, 'score': score, 'genre': genre, 'comment': comment}


def extract_comms(last_page, M_ID):
    URL = f"https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword={M_ID}&target=after"
    # 한줄평 페이지 주소
    comments_info = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    info = soup.find("div", {"class": "choice_movie_info"})
    title = info.find("h5").get_text(strip=True)
    genre = soup.find("td").get_text(strip=True).split('|')[0]
    for page in range(last_page):
        print(f"Scrapping naver page {page + 1}")
        result = requests.get(f"{URL}&page={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("td", {"class": "title"})
        # print(results[0].get_text(strip=True))
        for result in results:
            # comments['title']=title
            comm = extract_comm(result, title, genre, M_ID) # 한줄평 추출
            # comments.update(extract_comm(result))
            comments_info.append(comm)
        # print(comments_info)
    return comments_info


# extract_comms(1)


def get_movie_comm(i):
    last_page = get_last_page(i) # 마지막 페이지 (페이지 수)
    if last_page is None: #페이지가 없다면
        return None

    if last_page < 120: # 페이지 120 미만까지 추출
        comments = extract_comms(last_page, i)
    else:
        comments = extract_comms(120, i)

    if len(comments) is not 0:
        # print(comments)
        save_to_file(comments) # 파일로 저장
    print(comments)
    return comments
