#벅스 차트
import urllib.request
import datetime
import json
import csv
from bs4 import BeautifulSoup
import sqlite3
import re
from urllib.request import urlopen


def getSearchResult(search_day, artists, artistRank, titles, titleRank):
    url = urlopen("http://music.bugs.co.kr/chart/track/day/total?chartdate=" +
                  search_day)
    soup = BeautifulSoup(url, "html.parser", from_encoding="utf8")
    try:
        for link1 in soup.find_all(name="p", attrs={"class":"artist"}):
            try:
                artist = link1.find('a').text
                artists.append(artist)
                artistRank += 1
            except AttributeError as artistError:
                artist = 'N/A'
                artists.append(artist)
                artistRank += 1

            for link2 in soup.find_all(name="p", attrs={"class":"title"}):
                try:
                    title = link2.find('a').text
                    titles.append(title)
                    titleRank += 1
                except AttributeError as titleError:
                    title = 'N/A'
                    titles.append(title)
                    titleRank += 1
    except AttributeError as e: #p태그 자체가 존재하지 않을 경우, 데이터 없는 것으로 여김
        print(search_day + "이 날 데이터가 존재하지 않습니다.")
    except IndexError as index:
        print("인덱스 에러 / " + "아티스트 리스트 길이 : " + str(len(artists))
              + '/ 곡 리스트 길이 : ' + str(len(titles)))

def save_csv(search_day, artists, titles):
    f = open('bugschart_%s.csv' % (search_day,), 'wt', encoding='utf-8', newline='')
    wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    for i in range(0, 100):
        wr.writerow((search_day, str(i+1), artists[i], titles[i]))

    f.close()


def save_sqliteDB(search_day, artists, titles):
    dbconn = sqlite3.connect('bugs.db')
    dbcursor = dbconn.cursor()

    dbcursor.execute("drop table if exists bugs")
    dbcursor.execute("""create table bugs(
                            searchday text,
                            rank integer,
                            artist text,
                            title text)""")

    sql = "insert into bugs(searchday, rank, artist, title) values (?, ?, ?, ?)" # '?' 사용하면 튜플형식으로 데이터 전달
    for i in range(100):
        try:
            dbcursor.execute(sql, (search_day, i+1, artists[i], titles[i]))
        except:
            print('Error!')

    dbconn.commit()
    dbcursor.close()
    dbconn.close()

if __name__ == '__main__':
    artists = []
    artistRank = 0
    titles = []
    titleRank = 0

    search_day = input("검색할 날짜를 8자리로 입력하세요(ex : 20060922~20220923) : ")
    getSearchResult(search_day, artists, artistRank, titles, titleRank)
    save_csv(search_day, artists, titles)
    save_sqliteDB(search_day, artists, titles)