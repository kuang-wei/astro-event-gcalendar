from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import requests
from bs4 import BeautifulSoup
import scrape_astro as sa

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
#CLIENT_SECRET_FILE = 'client_secret_518439832199-ppjegsqacmfrvjf0pqfijq1ibr1duaq4.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Google Calendar API Python Event Add'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def duplicate_check(allevents):
    """
    THIS FUNCTION FAILS IF THERE IS ANY
    ALL DAY EVENT ON THE SAME DAY AS THE
    TALK

    input allevents, this function gives us
    back a list that contains which specific
    event has been added to the calendar

    It's checked by matching the time and location

    In the output matchedlist, False corresponds to
    events that can just be updated. True corresponds
    to events that need to be newly added 
    """
    matchedlist = list()
    for i in range(len(allevents)):
        tstart = allevents[i]['start']['dateTime']
        tstart_d = datetime.datetime.strptime(tstart, "%Y-%m-%dT%H:%M:%S")
        tstart_d = tstart_d+datetime.timedelta(hours=6) #converting to UTC
        tstart = tstart_d.isoformat()
        pulledlocation = allevents[i]['location']
        eventsResult = service.events().list(
            calendarId='primary', timeMin=tstart+'Z', maxResults=1, singleEvents=True, #Z indicates UTC
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        currentlocation = events[0]['location']
        if currentlocation == pulledlocation:
            matchedlist.append(False)
        else:
            matchedlist.append(True)
    return matchedlist

#Scrape events
links, ids, titles, dates = sa.preprcessing()
all_time_details = sa.talk_details(links, ids)
allevents = sa.eventlist(all_time_details, titles)

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

#Print current date and time
print()
print()
print("Current date and time:")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print()
print()

for i in range(len(allevents)):
    tstart = allevents[i]['start']['dateTime']
    tstart_d = datetime.datetime.strptime(tstart, "%Y-%m-%dT%H:%M:%S")
    tstart_d = tstart_d+datetime.timedelta(hours=6) #converting to UTC
    tstart = tstart_d.isoformat()
    pulledlocation = allevents[i]['location']
    eventsResult = service.events().list(
        calendarId='primary', timeMin=tstart+'Z', maxResults=10, singleEvents=True, #Z indicates UTC
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    for event in events:
        try:
            len(event['end']['dateTime'])  #All day event doesn't have this field, so we go to except case
            try: #in case there are no events in the near future that has location tag
                currentlocation = event['location']
            except:
                currentlocation = ''
            if currentlocation == pulledlocation:
                print('------------------')
                print(allevents[i]['summary'])
                print(allevents[i]['start']['dateTime'])
                print(allevents[i]['location'])
                event['summary'] = allevents[i]['summary']
                updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
                print()
                print('existing event updated')
                print('Calendar event URL: %s'% (event.get('htmlLink')))
                print('------------------')
                print()
                print()
            else:
                print('------------------')
                print(allevents[i]['summary'])
                print(allevents[i]['start']['dateTime'])
                print(allevents[i]['location'])
                newevent = service.events().insert(calendarId='primary', body=allevents[i]).execute()
                print()
                print('new event added')
                print('Calendar event URL: %s'% (newevent.get('htmlLink')))
                print('------------------')
                print()
                print()
            break #stop going through events because there is not a single all day event in events
        except:
            pass #go to the next event in events, so we can find the first event that isn't an all day event