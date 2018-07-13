# Adding comments later

from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2, sqlite3, os

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'OSRS CC Rank Tracker'
home_dir = os.path.expanduser('~')

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    ranks = ('Friend', 'Recruit', 'Corporal', 'Sergeant', 
            'Lieutenant', 'Captain', 'General')

    sheet_id = '1C3Hz78SaDe2F0w0NRfmbEWS_lUjtko6Lv4P4-bpNQzI'

    cxn = sqlite3.connect('{}/databases/main.sqlite'.format(home_dir))
    c = cxn.cursor()
    count = len(ranks)

    for notes in range(0, count):
        range_notes = [ '{}s!A2:A'.format(ranks[notes]),
            '{}s!D2:D'.format(ranks[notes])
        ]

        try:
            resp_notes = service.spreadsheets().values().batchGet(spreadsheetId=sheet_id,
                ranges=range_notes).execute()
        
            get_leng = len(resp_notes['valueRanges'][0]['values'])

            while get_leng >= 1:
                get_leng -= 1

                c.execute("UPDATE {} SET notes=? WHERE name=?".format('member'),
                    (resp_notes['valueRanges'][1]['values'][get_leng][0],
                    resp_notes['valueRanges'][0]['values'][get_leng][0]))

            cxn.commit()
        
        except IndexError:
            pass

    for each in range(0, count):
        range_clear = [ '{}s!A2:A'.format(ranks[each]),
            '{}s!B2:B'.format(ranks[each]),
            '{}s!C2:C'.format(ranks[each]),
            '{}s!D2:D'.format(ranks[each])
        ]
        
        clear_body = {'ranges': [clear[0:] for clear in range_clear]}

        service.spreadsheets().values().batchClear(spreadsheetId=sheet_id,
                body=clear_body).execute()
        
    for cc in range(0, count):
        stored = c.execute("SELECT {} FROM member WHERE {}'{}' ORDER BY name COLLATE NOCASE".format(
            'name, last_seen, date_rank, notes', 'rank_id=', cc + 1)).fetchall()

        dater = {'values': [info[:4] for info in stored]}
    
        service.spreadsheets().values().update(spreadsheetId=sheet_id,
            range='{}s!A2'.format(ranks[cc]), body=dater, valueInputOption='RAW').execute()

if __name__ == '__main__':
    main()
