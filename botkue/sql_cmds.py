from datetime import datetime

def change_curr(name, rank, date, database):
    database.execute(
        "UPDATE member SET "
        "rank_id=?, last_seen=?, date_rank=? WHERE name=?",
        (rank + 1, date, date, name,)
    )


def keep_curr(name, date, database):
    database.execute(
        "UPDATE member SET last_seen=? WHERE name=?", (date, name,)
    )


def restore_old(name, rank, seen, date, notes, ally, prev, database):
    database.execute(
        "INSERT OR IGNORE INTO member "
        "(name, rank_id, last_seen, date_rank, notes, is_added, prev_name) "
        "VALUES(?,?,?,?,?,?,?)", (name, rank + 1, seen, date, notes, ally, prev,)
    )


def append_new(name, rank, date, database):
    database.execute(
        "INSERT OR IGNORE INTO member "
        "(name, rank_id, last_seen, date_rank) VALUES(?,?,?,?)",
        (name, rank + 1, date, date)
    )


def append_unt(name, rank, date, database):
    database.execute(
        "INSERT OR IGNORE INTO member "
        "(name, rank_id, last_seen) VALUES(?,?,?)",
        (name, rank + 1, date)
    )


def delete_rank(name, database):
    database.execute(
        "DELETE FROM member WHERE name=?", (name,)
    )


def select_mem(name, database):
    database.execute(
        "SELECT * FROM member WHERE name=?", (name,)
    )


def verify_date(check):
    find_year = check[3].index("-")
    find_day = check[3].rindex("-")

    get_year = check[3][:find_year]
    get_day = check[3][int(find_day + 1):]
    get_month = check[3][int(find_year + 1):find_day]

    return (datetime.utcnow() - datetime(
        int(get_year), int(get_month), int(get_day))
    ).days
