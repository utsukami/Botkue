import sql_cmds
from datetime import datetime
from os.path import expanduser
from rank_logger import rank_logger
from sqlite3 import connect
from sys import argv

home = expanduser('~')
format_date = datetime.utcnow().strftime("%Y-%m-%d")

conn_main = connect('{}/tmp/main.sqlite'.format(home))
conn_lost = connect("{}/tmp/lost.sqlite".format(home))
cdb = conn_main.cursor()


def check_exists(name, database):
    sql_cmds.select_membs(name, database)

    try:
        return database.fetchall()[0]

    except IndexError:
        return False


def rank_tracker(name, rank_num):
    data = check_exists(name, cdb)

    if data:
        current_rank = int(data[1]) - 1

        if 0 <= rank_num <= 6:
            if rank_num < current_rank:
                rank_logger(data[0], rank_num, "Decrease")
                sql_cmds.change_curr(data[0], rank_num, format_date, cdb)

            elif rank_num > current_rank:
                rank_logger(data[0], rank_num, "Increase")
                sql_cmds.change_curr(data[0], rank_num, format_date, cdb)

            elif rank_num == current_rank:
                sql_cmds.keep_curr(data[0], format_date, cdb)

    elif not data:
        ldb = conn_lost.cursor()
        check_lost = check_exists(name, ldb)

        if not check_lost:
            if 0 <= rank_num <= 6:
                rank_logger(name, rank_num, "Append")
                sql_cmds.append_new(name, rank_num, format_date, cdb)

        elif check_lost:
            if 0 <= rank_num <= 6:
                rank_logger(name, rank_num, "Restore")
                sql_cmds.append_old(
                    name, rank_num, format_date, check_lost[3], cdb
                )

                sql_cmds.delete_rank(name, ldb)
                conn_lost.commit()

    conn_main.commit()


rank_tracker(str(argv[1]), int(argv[2]))
