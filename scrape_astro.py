import requests
from bs4 import BeautifulSoup
import datetime

def preprcessing():
	"""
	preprocessing is the function to be sued to parse through the event page
	It returns lists of the current events and its:
		links
		ids (html tag)
		titles
		dates
	"""
	masterurl = "https://astro.uchicago.edu/events/index.php"

	r = requests.get(masterurl)
	soup = BeautifulSoup(r.content, "lxml")

	talk_data = soup.find_all("div", {"class": "paragraph_third-text"})

	talk_page_index = 0 #0 is the current and future events; 1 is past

	current_future_dates = talk_data[talk_page_index].find_all("td", {"class": "width30"})
	talk_titles_links = talk_data[talk_page_index].find_all("a")

	links = []
	ids = []
	titles = []
	dates = []

	for link in talk_titles_links:
		links.append(masterurl[:-17]+link.get('href')[2:])
		idlocation = link.get('href').index('id')
		ids.append(link.get('href')[idlocation:])
		titles.append(link.text)

	for items in current_future_dates:
		dates.append(items.find_all("nobr")[0].text)

	return links, ids, titles, dates

def get_details(links, ids, TalkIndex):
	"""
	get_details gets all the time details of individual events into a list
	the list is formatted as [date, location, time]
	"""
	rIndividualTalk = requests.get(links[TalkIndex])
	soupIndividualTalk = BeautifulSoup(rIndividualTalk.content, "lxml")
	IndividualTalkPage = soupIndividualTalk.find_all("div", {"class":"paragraph_second"})

	for item in IndividualTalkPage:
	    if item.find_all("a", {"name":ids[TalkIndex]}):
	    	talkdate = item.find("b").text
	try:
		time_details = talkdate.split("|")
		time_details = [x.strip(' ') for x in time_details]
	except:
		time_details = []

	return time_details

def talk_details(links, ids):
	"""
	outputs a nested list, where each list inside the list is one talk event
	"""
	all_time_details = []
	for i in range(len(links)):
		all_time_details.append(get_details(links, ids, i))
	return all_time_details

def eventlist(talk_details, titles):
	"""
	Outputs an 'events' dictonary, that is needed for gcalendar API to read and add events

	Currently, it ignores events that don't have specific times
	So all day events are igonored
	"""
	events = []
	for i in range(len(talk_details)):
		try:
			date = talk_details[i][0]
			location = str(talk_details[i][1])
			time = talk_details[i][2]
			test_date_time = date.replace(',','')+' '+time.replace(' ','')
			testtitle = str(titles[i])
			datetime_object = datetime.datetime.strptime(test_date_time, '%B %d %Y %I:%M%p')
			endtime = datetime_object+datetime.timedelta(hours=1.5)
			test_start_time_iso = datetime_object.isoformat()
			test_end_time_iso = endtime.isoformat()
			event = {'summary': testtitle, 'location': location,'start': {'dateTime': test_start_time_iso, 'timeZone': 'America/Chicago',},'end': {'dateTime': test_end_time_iso,'timeZone': 'America/Chicago',}, 'reminders': {'useDefault': False,'overrides': [{'method': 'email', 'minutes': 24 * 60},{'method': 'popup', 'minutes': 10}]}}
			events.append(event)
		except:
			pass
	return events

if __name__ == "__main__":
	links, ids, titles, dates = preprcessing()
	all_time_details = talk_details(links, ids)

	TalkIndex = 1
	date = all_time_details[TalkIndex][0]
	print date
	location = str(all_time_details[TalkIndex][1])
	print location
	time = all_time_details[TalkIndex][2]
	print time
	test_date_time = date.replace(',','')+' '+time.replace(' ','') #delete the comma in "Month Day, Year" and make HH:MM PM into HH:MMPM
	print test_date_time
	testtitle = str(titles[TalkIndex])
	print testtitle

	datetime_object = datetime.datetime.strptime(test_date_time, '%B %d %Y %I:%M%p')
	endtime = datetime_object+datetime.timedelta(hours=1.5)
	test_start_time_iso = datetime_object.isoformat()
	test_end_time_iso = endtime.isoformat()

	print test_start_time_iso
	print test_end_time_iso
	event = {
  				'summary': testtitle,
  				'location': location,
  				#'description': 'A chance to hear more about Google\'s developer products.',
  				'start': {
  					'dateTime': test_start_time_iso,
    				'timeZone': 'America/Chicago',
  				},
  				'end': {
  					'dateTime': test_end_time_iso,
  					'timeZone': 'America/Chicago',
  				},
  				'reminders': {
  					'useDefault': False,
    				'overrides': [
      					{'method': 'email', 'minutes': 24 * 60},
      					{'method': 'popup', 'minutes': 10},
      					],
      			},
      		}
	print event


	events = eventlist(all_time_details, titles)
	print events