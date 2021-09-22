from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time
from db import insert_baseball_func


years = {"2020":25}

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

    for i in range(2, page+1):
        #url = "https://www.oddsportal.com/{}/{}/{}-{}/results/#/page/{}/".format(sports, country, league, season, i) #21년 제외 모든 리그 데이터 들고올때 url
        url = "https://www.oddsportal.com/{}/{}/{}/results/#/page/{}/".format(sports, country, league, i) #모든리그 21년 데이터 들고올때 url
            #https: // www.oddsportal.com / baseball / japan / npb / results /
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
                if i.select_one('.table-score').text != 'canc.' and i.select_one('.table-score').text != 'abn.' and i.select_one('.table-score').text != 'postp.':
                    score = i.select_one('.table-score').text.split(':')
                else:
                    score = [None, None]
                home_score = int(score[0].rstrip()) if score[0] is not None else None
                away_score = int(score[1].lstrip()) if score[1] is not None else None
                home_odds = float(i.select('.odds-nowrp')[0].text) if i.select('.odds-nowrp')[0].text != '-' else 0
                away_odds = float(i.select('.odds-nowrp')[1].text) if i.select('.odds-nowrp')[1].text != '-' else 0
                result = {'home_team': home_team,
                                'away_team': away_team,
                                'home_score': home_score,
                                'away_score': away_score,
                                'home_odds': home_odds,
                                'away_odds': away_odds,
                                'date': date,
                                'special': special,
                                'league':league}
                bucket.append(result)
                print(bucket)
                    # 데이터베이스 INSERT
                insert_baseball_func(result['home_team'],
                                         result['away_team'],
                                         result['home_score'],
                                         result['away_score'],
                                         result['home_odds'],
                                         result['away_odds'],
                                         result['date'],
                                         result['special'],
                                         result['league'])

            elif i.select_one('.first2') and i.select_one('.first2').attrs.get('colspan') == '4':
                before_date = i.select_one('.first2').text
                date = before_date.split('-')[0].rstrip()
                print(date)
                date = datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')
                if len(before_date.split('-')) > 1:
                    special = before_date.split('-')[1].lstrip()
                else:
                    special = None

        # print(bucket)
    driver.close()


# crawling("baseball","usa","mlb","2021",53)
# crawling("baseball","usa","mlb","2020",25)
# crawling("baseball","usa","mlb","2019",58)

#crawling("baseball","japan","npb","2021",16)
#crawling("baseball","japan","npb","2020",17)
#crawling("baseball","japan","npb","2019",20)

crawling("baseball","south-korea","kbo","2021",13)
#crawling("baseball","south-korea","kbo","2020",16)
#crawling("baseball","south-korea","kbo","2019",16)

#https://www.oddsportal.com/baseball/south-korea/kbo/results/#/page/2/




