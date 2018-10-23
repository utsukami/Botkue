import sql_cmds
from datetime import datetime
from os.path import expanduser
from rank_logger import rank_logger
from sqlite3 import connect

home = expanduser("~")
curr_utc = datetime.utcnow()

conn_main = connect("{}/main.sqlite".format(home))
conn_lost = connect("{}/lost.sqlite".format(home))
cdb = conn_main.cursor()


def remove_ranks(limiter, rank):
    cdb.execute("SELECT * FROM member")
    data = cdb.fetchall()

    for names in data:
        full_afk = sql_cmds.verify_date(names)

        if (full_afk >= limiter
                and names[2] <= rank):

            ldb = conn_lost.cursor()

            rank_logger(names[1], names[2], "Inactive")
            sql_cmds.restore_old(
                    names[1], names[2], names[3], names[4],
                    names[5], names[6], names[7], ldb
            )
            sql_cmds.delete_rank(names[1], cdb)

            conn_lost.commit()
            conn_main.commit()


remove_ranks(int(30), int(3))
remove_ranks(int(60), int(4))
