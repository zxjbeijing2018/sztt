import os
import shutil

import pymysql

fileroot = os.path.dirname(os.path.abspath(__file__))
migrations_dir = os.path.join(fileroot, 'api', 'migrations')

mysqlconf = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '1030475',
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

    try:
        print('del {}'.format(migrations_dir))
        shutil.rmtree(migrations_dir)
    except Exception:
        pass


init()
