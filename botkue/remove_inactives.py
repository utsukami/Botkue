import sql_cmds
from datetime import datetime
from os.path import expanduser
from rank_logger import rank_logger
from sqlite3 import connect

home = expanduser("~")
curr_utc = datetime.utcnow()

conn_main = connect("{}/databases/main.sqlite".format(home))
conn_lost = connect("{}/databases/lost.sqlite".format(home))
cdb = conn_main.cursor()


def remove_ranks(limiter, rank):
    cdb.execute("SELECT name, rank_id, last_seen, notes FROM member")
    data = cdb.fetchall()

    for names in data:
        full_afk = sql_cmds.verify_date(names)

        if (full_afk >= limiter
                and names[1] <= rank):

            ldb = conn_lost.cursor()

            rank_logger(names[0], names[1], "Inactive")
            sql_cmds.restore_old(names[0], names[1], names[2], names[3], ldb)
            sql_cmds.delete_rank(names[0], cdb)

            conn_lost.commit()
            conn_main.commit()


remove_ranks(int(30), int(3))
remove_ranks(int(60), int(4))
