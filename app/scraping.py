import requests
import pytz
from xml.etree import ElementTree
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup

SESSION_ENDPOINT = "https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316"


def request_cookies():
    session = requests.Session()
    session.get(SESSION_ENDPOINT)
    return session.cookies.get_dict()


def parse_date(date_info):
    year, month, day = (
        date_info[0].strip(" \n"),
        date_info[1].strip(" \n"),
        date_info[2].strip(" \n"),
    )
    return year, month, day


def parse_time(time_info):
    start, end = (
        time_info[0].strip(" \n"),
        time_info[1].strip(" \n"),
    )
    return start, end


def datetime_and_duration(year, month, day, start, end):
    est = pytz.timezone('Canada/Eastern')
    start_time = datetime.strptime(
        f'{year}-{month}-{day} {start}', '%Y-%b-%d %I:%M%p')

    end_time = datetime.strptime(
        f'{year}-{month}-{day} {end}', '%Y-%b-%d %I:%M%p')

    duration = int((end_time - start_time).total_seconds()/60)

    return est.localize(start_time), duration


def scrape_page(page: int, cookies: dict, timestamp: str) -> List[dict]:
    response = requests.get(
        f'https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?GetPagingData=true&aid=316&sEcho=6&iColumns=9&sColumns=&iDisplayStart={page*10}&iDisplayLength=10&ajax=true',
        cookies=cookies,
    )

    # Find HTML in the XML response
    tree = ElementTree.fromstring(response.text)
    html = tree.findtext('data')
    soup = BeautifulSoup(html, 'html.parser')

    session_data = []
    sessions = soup.find_all(attrs={'id': 'activity-course-row'})

    for session in sessions:
        barcode = int(session.find("td", {'headers': 'Barcode'}).text)
        available = int(session.find("td", {'headers': 'Available'}).text)
        title = str(session.find("td", {'headers': 'Course'}).find('div').text)
        location = str(session.find(
            'td', {'headers': 'Complex'}).find('a').text).strip(" \n")

        # Date / time information
        date_info = str(session.find(
            'td', {'headers': 'Dates'}).text).split('-')

        year, month, day = parse_date(date_info)

        time_info = str(session.find(
            'td', {'headers': 'Times'}).text).split('-')

        start, end = parse_time(time_info)

        time, duration = datetime_and_duration(year, month, day, start, end)

        data = {
            'id': barcode,
            'title': title,
            'location': location,
            'time': time.isoformat(),
            'duration': duration,
            'available': available,
            'timestamp': timestamp
        }

        session_data.append(data)

    return session_data


def scrape() -> (List[dict], str):
    """ Returns workout dictionaries, and the iso format timestamp string """
    data = []

    cookies = request_cookies()
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

    for i in range(20):
        try:
            sessions = scrape_page(i, cookies, timestamp)
        except Exception as e:
            print(f'ERROR "scrape": {e}')
            break

        if len(sessions) == 0:
            break

        data.extend(sessions)

    return data, timestamp
