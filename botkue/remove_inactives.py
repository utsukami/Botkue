import sqlite3
from os.path import expanduser as euser
import datetime
home = euser('~')

conn = sqlite3.connect('{}/testing/aoeu.sqlite'.format(home))
c = conn.cursor()

fonn = sqlite3.connect('{}/testing/lost_ranks.sqlite'.format(home))
f = fonn.cursor()

current_time_utc = datetime.datetime.utcnow()
format_time = current_time_utc.strftime("%Y-%m-%d")

def remove_ranks():
    c.execute("SELECT name, rank_id, last_seen FROM member")
    
    for data in c.fetchall():
        find_year = data[2].index('-')
        find_day = data[2].rindex('-')

        get_year = data[2][:find_year]
        get_day = data[2][int(find_day + 1 ):]
        get_month = data[2][int(find_year + 1):find_day]
        
        is_inact = datetime.datetime(int(get_year), int(get_month), int(get_day))
        
        if (current_time_utc - is_inact).days > 20:
            f.execute("INSERT OR IGNORE INTO member (name, rank_id, last_seen, reason) VALUES('{}', '{}', '{}', '{}')".format(data[0], data[1], data[2], 'Inactive'))
            fonn.commit()
            c.execute("DELETE FROM member WHERE name='{}'".format(data[0]))
            conn.commit()
remove_ranks()
