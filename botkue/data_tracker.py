import logging
from datetime import datetime
from os.path import expanduser
from sqlite3 import connect
from sys import argv

home = expanduser('~')
log_file = '{}/tmp/main.log'.format(home)
format_date = datetime.utcnow().strftime("%Y-%m-%d")

conn = connect('{}/tmp/main.sqlite'.format(home))
c = conn.cursor()

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='{}'.format('[%(asctime)s] %(message)s'),
    datefmt='{}'.format('%Y-%m-%d %H:%M:%S')
)


def rank_logger(name, rank, action):
    ranks = (
        "Smiley", "Recruit", "Corporal", "Sergeant",
        "Lieutenant", "Captain", "General"
    )

    logging.info(
        "ACTION: {} | NAME: {} | STATUS: {}"
        .format(action, name, ranks[rank])
    )


def alter_ranks(name, rank, date, method):
    if method == 1:
        c.execute(
            "UPDATE member SET "
            "rank_id=?, last_seen=?, date_rank=? WHERE name=?",
            (rank + 1, date, date, name,)
        )

    elif method == 2:
        c.execute(
            "UPDATE member SET last_seen=? WHERE name=?", (date, name,)
        )

    elif method == 3:
        c.execute(
            "INSERT OR IGNORE INTO member (name, rank_id, last_seen) "
            "VALUES(?,?,?)", (name, rank + 1, date,)
        )

    conn.commit()


def rank_tracker(name, rank_num):
    c.execute(
        "SELECT name, rank_id FROM member WHERE name=?", (name,)
    )

    try:
        data = c.fetchall()[0]

        if name in data[0]:
            current_rank = int(data[1]) - 1

            if 0 <= rank_num <= 6:
                if rank_num < current_rank:
                    rank_logger(data[0], rank_num, "Decrease")
                    alter_ranks(data[0], rank_num, format_date, 1)

                elif rank_num > current_rank:
                    rank_logger(data[0], rank_num, "Increase")
                    alter_ranks(data[0], rank_num, format_date, 1)

                elif rank_num == current_rank:
                    alter_ranks(data[0], '', format_date, 2)

    except IndexError:
        if 0 <= rank_num <= 6:
            rank_logger(name, rank_num, "Append")
            alter_ranks(name, rank_num, format_date, 3)
        else:
            pass


rank_tracker(str(argv[1]), int(argv[2]))
