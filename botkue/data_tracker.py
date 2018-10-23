
import sql_cmds
from datetime import datetime
from os.path import expanduser
from rank_logger import rank_logger
from sqlite3 import connect
from sys import argv

home = expanduser("~")
format_date = datetime.utcnow().strftime("%Y-%m-%d")

conn_main = connect("{}/databases/main.sqlite".format(home))
conn_lost = connect("{}/databases/lost.sqlite".format(home))
cdb = conn_main.cursor()


def check_exists(name, database):
    sql_cmds.select_mem(name, database)

    try:
        return database.fetchall()[0]

    except IndexError:
        return False


def rank_tracker(name, rank_num):
    name = name.replace(u"\xa0", u" ")
    data = check_exists(name, cdb)

    if 0 <= rank_num <= 6:
        if data:
            needs_update = sql_cmds.verify_date(data)
            current_rank = int(data[2]) - 1

            if (rank_num < current_rank
                    or rank_num > current_rank):

                if rank_num < current_rank:
                    rank_logger(data[1], rank_num, "Decrease")

                else:
                    rank_logger(data[1], rank_num, "Increase")

                sql_cmds.change_curr(data[1], rank_num, format_date, cdb)

            elif needs_update > 0:
                sql_cmds.keep_curr(data[1], format_date, cdb)
                rank_logger(data[1], rank_num, "Active")

        else:
            ldb = conn_lost.cursor()
            check_lost = check_exists(name, ldb)

            if check_lost:
                rank_logger(name, rank_num, "Restore")
                sql_cmds.restore_old(
                    name, rank_num, format_date, check_lost[4], check_lost[5],
                    check_lost[6], check_lost[7], cdb
                )

                sql_cmds.delete_rank(name, ldb)
                conn_lost.commit()

            else:
                if rank_num >= 1:
                    rank_logger(name, rank_num, "Append")
                    sql_cmds.append_unt(name, rank_num, format_date, cdb)

                else:
                    rank_logger(name, rank_num, "Addition")
                    sql_cmds.append_new(name, rank_num, format_date, cdb)

    conn_main.commit()

rank_tracker(str(argv[1]), int(argv[2]))
