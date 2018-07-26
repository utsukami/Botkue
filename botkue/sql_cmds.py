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


def append_old(name, rank, date, notes, database):
    database.execute(
        "INSERT OR IGNORE INTO member "
        "(name, rank_id, last_seen, date_rank, notes) VALUES(?,?,?,?,?)",
        (name, rank + 1, date, date, notes)
    )


def append_new(name, rank, date, database):
    database.execute(
        "INSERT OR IGNORE INTO member "
        "(name, rank_id, last_seen, date_rank) VALUES(?,?,?,?)",
        (name, rank + 1, date, date)
    )


def delete_rank(name, database):
    database.execute(
        "DELETE FROM member WHERE name=?", (name,)
    )


def select_membs(name, database):
    database.execute(
        "SELECT name, rank_id, last_seen, notes FROM member "
        "WHERE name=?", (name,)
    )
