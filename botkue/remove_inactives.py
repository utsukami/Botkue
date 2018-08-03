import sql_cmds
from datetime import datetime
from os.path import expanduser
from rank_logger import rank_logger
from sqlite3 import connect

home = expanduser('~')
curr_utc = datetime.utcnow()

conn_main = connect('{}/tmp/main.sqlite'.format(home))
conn_lost = connect('{}/tmp/lost.sqlite'.format(home))
cdb = conn_main.cursor()


def remove_ranks(limiter, rank):
    cdb.execute("SELECT name, rank_id, last_seen, notes FROM member")

    for data in cdb.fetchall():
        find_year = data[2].index("-")
        find_day = data[2].rindex("-")

        get_year = data[2][:find_year]
        get_day = data[2][int(find_day + 1):]
        get_month = data[2][int(find_year + 1):find_day]

        full_afk = (curr_utc - datetime(
            int(get_year), int(get_month), int(get_day))
        ).days

        if (full_afk >= limiter
                and data[1] <= rank):
            ldb = conn_lost.cursor()

            rank_logger(data[0], data[1], "Inactive")
            sql_cmds.restore_old(data[0], data[1], data[2], data[3], ldb)
            sql_cmds.delete_rank(data[0], cdb)

            conn_lost.commit()
            conn_main.commit()


remove_ranks(int(30), int(3))
remove_ranks(int(60), int(4))
