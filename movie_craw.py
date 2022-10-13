from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

def print_menu():
    print("*** 메뉴 ***")
    print("1. 조회순")
    print("2. 평점순(현재상영영화)")
    print("3. 평점순(모든영화)")
    print("4. 프로그램 종료")

def proc_cnt(sel, search):
    search_date = input("날짜 선택(ex:20210725) => ")
    f = open('moviechart_%s_%s.csv' % (sel, search_date), 'wt', encoding='utf-8',
             newline='')
    movie_titles = []
    try:
        url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?"
        url += "sel=" + sel
        url += "&date=" + search_date

        urls = urlopen(url)
        soup = BeautifulSoup(urls, "html.parser", from_encoding="utf8")

        for link1 in soup.find_all(name="div", attrs={"class": "tit3"}):
            try:
                movie_title = link1.find('a').text
                movie_titles.append(movie_title)
            except:
                movie_title = 'N/A'
                movie_titles.append(movie_title)

        wr = csv.writer(f, delimiter=",")
        wr.writerow((str(search),))
        print('\n' + search)
        wr.writerow(("rank", "title"))
        for i in range(0, len(movie_titles)):
            wr.writerow((str(i + 1), movie_titles[i]))
            print(str(i + 1) + ',' + movie_titles[i])
    except:
        print("에러 발생!!")
    finally:
        f.close()

def proc_cur(sel, search):
    search_date = input("날짜 선택(ex:20210725) => ")
    f = open('moviechart_%s_%s.csv' % (sel, search_date), 'wt', encoding='utf-8',
             newline='')
    movie_titles = []
    movie_jumsus = []
    try:
        url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?"
        url += "sel=" + sel
        url += "&date=" + search_date

        urls = urlopen(url)
        soup = BeautifulSoup(urls, "html.parser", from_encoding="utf8")

        for link1 in soup.find_all(name="div", attrs={"class": "tit5"}):
            try:
                movie_title = link1.find('a').text
                movie_titles.append(movie_title)
            except:
                movie_title = 'N/A'
                movie_titles.append(movie_title)

        for link2 in soup.find_all(name="td", attrs={"class": "point"}):
            try:
                movie_jumsu = link2.text
                movie_jumsus.append(movie_jumsu)
            except:
                movie_jumsu = 'N/A'
                movie_jumsus.append(movie_jumsu)

        wr = csv.writer(f, delimiter=",")
        wr.writerow((str(search),))
        print('\n' + search)
        wr.writerow(("rank", "title", "point"))
        for i in range(0, len(movie_titles)):
            wr.writerow((str(i + 1), movie_titles[i], movie_jumsus[i]))
            print(str(i + 1) + ',' + movie_titles[i] + ',' + movie_jumsus[i])
    except:
        print("에러 발생!!")
    finally:
        f.close()

def proc_pnt(sel, search):
    search_date = input("날짜 선택(ex:20210725) => ")
    start_page = input("시작 페이지(1부터) => ")
    end_page = input("종료 페이지(40까지) => ")
    f = open('moviechart_%s_%s.csv' % (sel, search_date), 'wt', encoding='utf-8',
             newline='')
    movie_titles = []
    movie_jumsus = []
    try:
        url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?"
        url += "sel=" + sel
        url += "&date=" + search_date

        # urls = urlopen(url)
        # soup = BeautifulSoup(urls, "html.parser", from_encoding="utf8")

        for page in range(int(start_page), int(end_page) + 1):
            # url_page = url
            url += "&page=" + str(page)
            urls = urlopen(url)
            print(url)
            soup = BeautifulSoup(urls, "html.parser", from_encoding="utf8")

            for link1 in soup.find_all(name="div", attrs={"class": "tit5"}):
                try:
                    movie_title = link1.find('a').text
                    movie_titles.append(movie_title)
                except :
                    movie_title = 'N/A'
                    movie_titles.append(movie_title)

            for link2 in soup.find_all(name="td", attrs={"class": "point"}):
                try:
                    movie_jumsu = link2.text
                    movie_jumsus.append(movie_jumsu)
                except:
                    movie_jumsu = 'N/A'
                    movie_jumsus.append(movie_jumsu)

        rank = 1
        wr = csv.writer(f, delimiter=",")
        wr.writerow((str(search),))
        print('\n' + search)
        wr.writerow(("rank", "title", "point"))
        # if menu == '3':
        if int(start_page) > 1:
            rank = (int(start_page) - 1) * 50 + 1
        for i in range(0, len(movie_titles)):
            wr.writerow((str(i + rank), movie_titles[i], movie_jumsus[i]))
            print(str(i + rank) + ',' + movie_titles[i] + ',' + movie_jumsus[i])
    except:
        print("에러 발생!!")
    finally:
        f.close()


if __name__ == "__main__":
    while True:
        print_menu()
        menu = input("메뉴 선택 => ")

        if menu == '1':
            proc_cnt('cnt', "*** 조회순 ***")
        elif menu == '2':
            proc_cur('cur', "*** 평점순(현재상영영화) ***")
        elif menu == '3':
            proc_pnt('pnt', "*** 평점순(모든영화) ***")
        elif menu == '4':
            print("\nThe End...")
            break
        else:
            print("메뉴를 잘못 선택하였습니다!!!")
        print()