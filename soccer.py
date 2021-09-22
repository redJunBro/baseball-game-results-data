from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time
from db import *

webdriver_options = webdriver.ChromeOptions()
webdriver_options.add_argument('headless')

# # driver = webdriver.Chrome("/Users/ijinseong/Downloads/chromedriver",options=webdriver_options)
# driver = webdriver.Chrome("/Users/Administrator/Downloads/chromedriver")
# url = "https://www.oddsportal.com/soccer/england/premier-league-2020-2021/results"
# driver.get(url)
# driver.implicitly_wait(4)
#
# posting = driver.find_element_by_xpath('//*[@id="user-header-timezone-expander"]')
# posting.click()
# driver.implicitly_wait(4)
# time.sleep(3)
#
# posting = driver.find_element_by_xpath('//*[@id="timezone-content"]/a[54]') #
# posting.click()
# driver.implicitly_wait(2)
# time.sleep(3)


def crawling(sports,country,league,season,page):
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')

    driver = webdriver.Chrome("/Users/Administrator/Downloads/chromedriver")
    url = "https://www.oddsportal.com/{}/{}/{}/results/".format(sports,country,league)


    driver.get(url)
    driver.implicitly_wait(4)

    posting = driver.find_element_by_xpath('//*[@id="user-header-timezone-expander"]')  # 야구 나라 선택창 클릭
    posting.click()
    driver.implicitly_wait(4)
    time.sleep(3)

    posting = driver.find_element_by_xpath('//*[@id="timezone-content"]/a[54]')  # 한국 시간 클릭
    posting.click()
    driver.implicitly_wait(2)
    time.sleep(3)
    for i in range(1, page+1):
        url = "https://www.oddsportal.com/{}/{}/{}-{}/results/#/page/{}/".format(sports, country, league, season, i)
        #url = "https://www.oddsportal.com/{}/{}/{}/results/#/page/{}/".format(sports, country, league,i)  # 모든리그 21년 데이터 들고올때 url
        driver.get(url)
        driver.implicitly_wait(2)

        time.sleep(2)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('#tournamentTable > tbody > tr')

        bucket = []
        for i in tr:
            if i.select_one('.first2') is None and i.select_one('.name') is not None:
                team = i.select_one('.name').select_one('a').text.split('-')
                home_team = team[0].rstrip()
                away_team = team[1].lstrip()
                if i.select_one('.table-score').text != 'canc.' and i.select_one('.table-score').text != 'abn.':
                    score = i.select_one('.table-score').text.split(':')
                else:
                    score = [None, None]
                home_score = int(score[0].rstrip()) if score[0] is not None else None
                away_score = int(score[1].lstrip()) if score[1] is not None else None
                home_odds = float(i.select('.odds-nowrp')[0].text) if i.select('.odds-nowrp')[0].text != '-' else 0
                draw_odds = float(i.select('.odds-nowrp')[1].text) if i.select('.odds-nowrp')[1].text != '-' else 0
                away_odds = float(i.select('.odds-nowrp')[2].text) if i.select('.odds-nowrp')[2].text != '-' else 0
                print(home_odds)
                print(draw_odds)
                print(away_odds)
                result = {'home_team': home_team,
                          'away_team': away_team,
                          'home_score': home_score,
                          'away_score': away_score,
                          'home_odds': home_odds,
                          'draw_odds': draw_odds,
                          'away_odds': away_odds,
                          'date': date,
                          'special': special,
                          'league':league}
                bucket.append(result)
                print(bucket)
                # 데이터베이스 INSERT
                insert_soccer(result['home_team'],
                                     result['away_team'],
                                     result['home_score'],
                                     result['away_score'],
                                     result['home_odds'],
                                     result['draw_odds'],
                                     result['away_odds'],
                                     result['date'],
                                     result['special'],
                                     result['league'])
            elif i.select_one('.first2') and i.select_one('.first2').attrs.get('colspan') == '3':
                before_date = i.select_one('.first2').text
                date = before_date.split('-')[0].rstrip()
                date = datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')
                if len(before_date.split('-')) > 1:
                    special = before_date.split('-')[1].lstrip()
                else:
                    special = None

    # print(bucket)
    driver.close()


# crawling("soccer","england","premier-league","2020-2021",8)
# crawling("soccer","england","premier-league","2019-2020",8)
# crawling("soccer","england","premier-league","2018-2019",8)
#
# crawling("soccer","germany","bundesliga","2020-2021",7)
# crawling("soccer","germany","bundesliga","2019-2020",7)
# crawling("soccer","germany","bundesliga","2018-2019",7)
#
#
# crawling("soccer","france","ligue-1","2020-2021",8)
# crawling("soccer","france","ligue-1","2019-2020",6)
# crawling("soccer","france","ligue-1","2018-2019",8)


# crawling("soccer","spain","laliga","2020-2021",8)
# crawling("soccer","spain","laliga","2019-2020",8)
# crawling("soccer","spain","laliga","2018-2019",8)


# crawling("soccer","italy","serie-a","2020-2021",8)
crawling("soccer","italy","serie-a","2019-2020",8)
crawling("soccer","italy","serie-a","2018-2019",8)








# 21년 데이터 프랑스만 있음

#crawling("soccer","england","ligue-1",8) # 프랑스
