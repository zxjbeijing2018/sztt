import pymysql

mysqlconf = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'zb@1030475',
    'db': 'mysql',
    'charset': 'utf8',
}

udb = 'szttdb'

connection = pymysql.connect(**mysqlconf)


def init():
    with connection.cursor() as cursor:
        dropsql = f"DROP DATABASE {udb}"
        initsql = f"CREATE DATABASE {udb}"
        try:
            cursor.execute(dropsql)
            cursor.execute(initsql)
        except Exception:
            cursor.execute(initsql)
        connection.commit()


init()
