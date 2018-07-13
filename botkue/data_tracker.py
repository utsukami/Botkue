# Adding comments later

import sys, sqlite3, logging, datetime
from os.path import expanduser as euser

ranks = ('Smiley', 'Recruit', 'Corporal', 'Sergeant', 'Lieutenant', 'Captain', 'General')
home = euser('~')

conn = sqlite3.connect('{}/databases/main.sqlite'.format(home))
c = conn.cursor()

fonn = sqlite3.connect('{}/databases/lost.sqlite'.format(home))
f = fonn.cursor()

arg_name = str(sys.argv[1])
arg_rank = int(sys.argv[2])

log_file = '{}/logs/main.log'.format(home)

logging.basicConfig(filename=log_file,level=logging.INFO,
        format='{}'.format(
            '[%(asctime)s] %(message)s'),
        datefmt='{}'.format(
            '%Y-%m-%d %H:%M:%S')
)

current_time_utc = datetime.datetime.utcnow()
format_time = current_time_utc.strftime("%Y-%m-%d")

def rank_tracker(name, rank_num):
    c.execute("SELECT {} FROM member WHERE name='{}'".format(
        'name, rank_id, last_seen', name))
    
    try:
        data = c.fetchall()[0]

        if name in data[0]:
            match_order = rank_num + 1
            
            if (match_order >= 1 
                    and match_order <= 7):
                
                if (match_order < int(data[1]) 
                        or match_order > int(data[1])):
                    
                    c.execute("UPDATE member SET {}'{}', {}'{}', {}'{}' WHERE {}'{}'".format(
                        'rank_id=', rank_num + 1, 'last_seen=', format_time,
                        'date_rank=', format_time, 'name=', data[0]))
                    
                    if (match_order < int(data[1]) 
                            and match_order >= 1):
                        
                        logging.info('ACTION: {} | NAME: {} | STATUS: {}'.format(
                            'Decrease', data[0], ranks[rank_num]))
                    
                    elif (match_order > int(data[1]) 
                            and match_order <= 7):
                        
                        logging.info('ACTION: {} | NAME: {} | STATUS: {}'.format(
                            'Increase', data[0], ranks[rank_num]))
                   
                    conn.commit()
                
                else:
                    c.execute("UPDATE member SET {}'{}' WHERE {}'{}'".format(
                        'last_seen=', format_time, 'name=', data[0]))
                    conn.commit()

            elif match_order == 0:
                logging.info('ACTION: {} | NAME: {} | STATUS: {}'.format(
                    'Removed', data[0], 'Inactive'))
                
                f.execute("INSERT INTO member ({}) VALUES('{}', '{}', '{}', '{}')".format(
                    'name, rank_id, last_seen, reason', data[0],
                    data[1], format_time, 'Removed'))
               
                c.execute("DELETE FROM member WHERE name='{}'".format(data[0]))
                
                fonn.commit()
                conn.commit()

    except IndexError:
        if rank_num >= 0 and rank_num <= 6:
            c.execute("INSERT OR IGNORE INTO member ({}) VALUES('{}', '{}', '{}')".format(
                "name, rank_id, last_seen", name, rank_num + 1, format_time))
            conn.commit()
            logging.info('ACTION: {} | NAME: {} | STATUS: {}'.format(
                'Append', name, ranks[rank_num]))
        else:
            pass

rank_tracker(arg_name, arg_rank)
