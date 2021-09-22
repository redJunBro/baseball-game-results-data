import pymysql


def insert_baseball_func(home_team, away_team, home_score, away_score, home_odds, away_odds, date, special, league):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="000516", db="sports", charset="utf8")
        curs = conn.cursor()
        sql = """insert into baseball(home_team, away_team, home_score, away_score, home_odds, away_odds, date, special, league)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (home_team, away_team, home_score, away_score, home_odds, away_odds, date, special, league)

        curs.execute(sql, data)
        baseball_id = curs.lastrowid
        conn.commit()
        conn.close()

        print('인설트 완료 :' + str(baseball_id))
        return baseball_id
    except pymysql.err as e:
        print(e)


def baseball_select(date,league):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="000516", db="sports", charset="utf8")
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = """select home_team, away_team, home_score, away_score, home_odds, away_odds, date, league from baseball where date=%s AND league=%s and special is null"""
        data = (date,league)
        curs.execute(sql, data)
        rows = curs.fetchall()
        return rows
    except pymysql.err as e:
        print(e)


def insert_soccer(home_team, away_team, home_score, away_score, home_odds, draw_odds, away_odds, date, special, league):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="000516", db="sports", charset="utf8")
        curs = conn.cursor()
        sql = """insert into soccer(home_team, away_team, home_score, away_score, home_odds,draw_odds, away_odds, date, special, league)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (home_team, away_team, home_score, away_score, home_odds,draw_odds, away_odds, date, special, league)

        curs.execute(sql, data)
        soccer_id = curs.lastrowid
        conn.commit()
        conn.close()

        print('인설트 완료 :' + str(soccer_id))
        return soccer_id
    except pymysql.err as e:
        print(e)

def soccer_select(date,league):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="000516", db="sports", charset="utf8")
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = """select home_team, away_team, home_score, away_score, home_odds, draw_odds, away_odds, date, league from soccer where date=%s AND league=%s and special is null"""
        data = (date,league)
        curs.execute(sql, data)
        rows = curs.fetchall()
        return rows
    except pymysql.err as e:
        print(e)
