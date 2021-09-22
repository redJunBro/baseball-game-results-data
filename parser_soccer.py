from db import soccer_select
import datetime
import pandas as pd
from xlsxwriter import Workbook
import numpy

# 모든경기수

three_years_list = []
one_years_list = []
three_months_list = []
one_months_list = []


def calculator(game_list, su_c, utd_c, draw_c, league):
    # del game_list[-1]
    #print(game_list)
    game_n = sum(game_list)
    return {
        'league': league,
        'avg_game_n': numpy.mean(game_list),
        'total_game_n': sum(game_list),
        'suc': su_c,
        'utd_c': utd_c,
        'draw_c': draw_c,
        'su_percent': su_c / game_n * 100,
        'utd_percent': utd_c / game_n * 100,
        'draw_percent': draw_c / game_n * 100,
    }


def date_caculator(term): # 합격
    start = datetime.datetime.strptime("2018-09-11", "%Y-%m-%d")
    end = datetime.datetime.strptime("2021-09-11", "%Y-%m-%d")
    date_list = []
    start_date = datetime.datetime.strptime("2018-09-11", "%Y-%m-%d")
    for i in range(0, (end - start).days + 1, term + 1):
        end_date = start + datetime.timedelta(days=i + term)
        if end_date > datetime.datetime.strptime("2021-09-11", "%Y-%m-%d"):
            break
        date_list.append({'start_date': start_date, 'end_date': end_date})
        # print(start_date)
        start_date = end_date + datetime.timedelta(days=1)
        # print(1)
        # print(date_list)
    return date_list


def parser(start_date, end_date):
    leagues = ['ligue-1', 'laliga', 'premier-league', 'serie-a', 'bundesliga']
    date_generated = [start_date + datetime.timedelta(days=x) for x in
                      range(0, (end_date - start_date).days + 1)]
    # print(date_generated)
    leagues_results = []
    for league in leagues:
        game_list = []

        su_c = 0
        utd_c = 0
        draw_c = 0
        for var in date_generated:
            date = var.strftime("%Y-%m-%d")
            results = soccer_select(date, league)
            print(results)

            if len(results) != 0:
                game_list.append(len(results))
                for result in results:
                    if result['home_score'] is not None and result['away_score'] is not None:
                        if result['home_odds'] < result['away_odds']:
                            if result['home_score'] > result['away_score']:
                                su_c += 1
                            if result['home_score'] < result['away_score']:
                                utd_c += 1
                            if result['home_score'] == result['away_score']:
                                draw_c += 1
                        elif result['home_odds'] > result['away_odds']:
                            if result['home_score'] < result['away_score']:
                                su_c += 1
                            if result['home_score'] > result['away_score']:
                                utd_c += 1
                            if result['home_score'] == result['away_score']:
                                draw_c += 1
        leagues_results.append({'league': league, 'content': {'game_list': game_list, 'su_c': su_c, 'utd_c': utd_c, 'draw_c': draw_c}})
    return leagues_results  # [{},{},{},{},{}]


def status(term):
    total_status = []
    status_list = []
    dates = date_caculator(int(term))
    for date in dates:
        results = parser(date['start_date'], date['end_date'])
        for result in results:
            if result is not None:
                status_list.append(
                    calculator(result['content']['game_list'],
                            result['content']['su_c'], result['content']['utd_c'],
                            result['content']['draw_c'], result['league']))
                total_status.append(status_list)

            print(total_status)

    return total_status  # [[{},{},{},{},{}, ...]]


finish = status(30)
print(finish)

#print(finish)



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

# date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
# year_date_generated = [one_year_start + datetime.timedelta(days=x) for x in range(0, (end - one_year_start).days + 1)]
# month_date_generated = [one_month_start + datetime.timedelta(days=x) for x in range(0, (end - one_month_start).days + 1)]
# week_date_generated = [one_week_start + datetime.timedelta(days=x) for x in range(0, (end - one_week_start).days + 1)]


# elif result['home_odds'] > result['away_odds']:
#     if result['home_score'] == result['away_score']:
#         draw_c += 1
# elif result['home_odds'] < result['away_odds']:
#     if result['home_score'] == result['away_score']:
#         draw_c += 1
