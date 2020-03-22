import requests
from bs4 import BeautifulSoup
import time
from nugu.movie_story_scrapper.crawling.csv_save import save_to_file
from nugu.movie_story_scrapper.crawling.csv2_save import save_to_file2


def get_last_page(M_ID):
    URL = f"https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword={M_ID}&target=after"
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "h5_right_txt"})
    if pagination:
        num = pagination.find("strong").string
        max_page = int(num) / 10 + 1
        return int(max_page)
    else:
        return None


def extract_comm(html, title, genre, M_ID):
    comment = html.get_text('|', strip=True).split('|')[3]
    score = html.find("em").string
    return {'id': M_ID, 'title': title, 'score': score, 'genre': genre, 'comment': comment}


def extract_summary(M_ID):
    URL = f"https://movie.naver.com/movie/bi/mi/basic.nhn?code={M_ID}"
    # story_info = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    info = soup.find("div", {"class": "story_area"})
    story = info.find("p").get_text(strip=True)
    return story


def extract_comms(last_page, M_ID):
    # story = extract_summary(M_ID)
    # if story is None:
    #     return
    URL = f"https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword={M_ID}&target=after"
    comments_info = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    info = soup.find("div", {"class": "choice_movie_info"})
    title = info.find("h5").get_text(strip=True)
    genre = soup.find("td").get_text(strip=True).split('|')[0]
    if '개봉' in genre:
        return

    for page in range(last_page):
        print(f"Scrapping naver page {page+1}")
        result = requests.get(f"{URL}&page={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("td", {"class": "title"})
        # print(results[0].get_text(strip=True))
        for result in results:
            # comments['title']=title
            comm = extract_comm(result, title, genre, M_ID)
            # comments.update(extract_comm(result))
            comments_info.append(comm)
        # print(comments_info)
    return comments_info


# extract_comms(1)


def get_movie_comm(i):
    last_page = get_last_page(i)
    if last_page is None:
        return

    story_info = []
    story = extract_summary(i)

    if story is None:
        return

    story_d = {'id': i, 'story': story}
    story_info.append(story_d)
    save_to_file2(story_info)
    return
    # 밑에는 코멘트 추출하는 코드 동작 시키는 부분
    # if last_page < 120:
    #     comments = extract_comms(last_page, i)
    # else:
    #     comments = extract_comms(120, i)
    #
    # if len(comments) is not 0:
    #     # print(comments)
    #     save_to_file(comments)
    # return comments
