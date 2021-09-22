from db import baseball_select
import datetime
import pandas as pd
from xlsxwriter import Workbook
import numpy

success = []
bucket = []

gamelist = []  # 모든경기수
japan = "npb"
korea = "kbo"
mlb = "mlb"

su_c = 0
utd_c = 0



# date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
# year_date_generated = [one_year_start + datetime.timedelta(days=x) for x in range(0, (end - one_year_start).days + 1)]
# month_date_generated = [one_month_start + datetime.timedelta(days=x) for x in range(0, (end - one_month_start).days + 1)]
# week_date_generated = [one_week_start + datetime.timedelta(days=x) for x in range(0, (end - one_week_start).days + 1)]

def select_f(date, league):
    results = baseball_select(date, league)
    return results


# 당일 + 정배 + 가 모두 승리 + 경기 수 2개 이상 // 모든경기들 하루 경기수 평균

def parser_from_date(start_date, end_date, su_c=0, utd_c=0):
    date_generated = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
    for var in date_generated:
        date = var.strftime("%Y-%m-%d")
        # results = baseball_select(date,mlb)
        results = select_f(date, japan)

        if len(results) != 0:
            gamelist.append(len(results))
            for result in results:
                if result['home_odds'] < result['away_odds']:
                    if result['home_score'] is not None and result['away_score'] is not None:
                        if result['home_score'] > result['away_score']:
                            su_c += 1
                        if result['home_score'] < result['away_score']:
                            utd_c += 1
                else:
                    if result['home_score'] is not None and result['away_score'] is not None:
                        if result['home_score'] < result['away_score']:
                            su_c += 1
                        if result['home_score'] > result['away_score']:
                            utd_c += 1
    return gamelist, su_c, utd_c



# 3 years
gamelist, su_c, utd_c = parser_from_date(datetime.datetime.strptime("2019-03-11", "%Y-%m-%d"), datetime.datetime.strptime("2021-09-11", "%Y-%m-%d"))

# 1 years

average = numpy.mean(gamelist)  # mlb 하루 평균 경기수 ( 3페이지 임시 )
game_n = sum(gamelist)
print(gamelist)  # 일마다 경기수
print(game_n)  # 전체 경기수
print(su_c)  # 정배뜬경기수
print(utd_c)  # 역배뜬경기수
print(average)  # 하루 평균 경기
su_percent = su_c / game_n * 100.0 # 정배
utd_percent = utd_c / game_n * 100.0 # 역배
print(su_percent)  # 정배평균
print(utd_percent)  # 역배평균













#
# for i in success:
#     print(i)
#     print(success)
#
# ordered_list = ["home", "away", "score", "home_odds", "away_odds",
#                 "date"]  # List object calls by index, but the dict object calls items randomly
#
# wb = Workbook("updateFile.xlsx")
# ws = wb.add_worksheet("New Sheet")  # Or leave it blank. The default name is "Sheet 1"
#
# first_row = 0
# for header in ordered_list:
#     col = ordered_list.index(header)  # We are keeping order.
#     ws.write(first_row, col, header)  # We have written first row which is the header of worksheet also.
#
# row = 1
# for i in success:
#     for player in i:
#         for _key, _value in player.items():
#             col = ordered_list.index(_key)
#             ws.write(row, col, _value)
#         row += 1  # enter the next row
# wb.close()
