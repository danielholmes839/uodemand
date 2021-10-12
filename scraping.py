from typing import List
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup


def request_cookies():
    SESSION_ENDPOINT = "https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316"
    session = requests.Session()
    session.get(SESSION_ENDPOINT)
    return session.cookies.get_dict()


COOKIES = request_cookies()


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
    start_time = datetime.strptime(
        f'{year}-{month}-{day} {start}', '%Y-%b-%d %I:%M%p').replace(tzinfo=timezone(offset=timedelta(hours=-4)))

    end_time = datetime.strptime(
        f'{year}-{month}-{day} {end}', '%Y-%b-%d %I:%M%p').replace(tzinfo=timezone(offset=timedelta(hours=-4)))

    duration = int((end_time - start_time).total_seconds()/60)

    return start_time, duration


def scrape_page(page: int) -> List[dict]:
    response = requests.get(
        f'https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?GetPagingData=true&aid=316&sEcho=6&iColumns=9&sColumns=&iDisplayStart={page*10}&iDisplayLength=10&ajax=true',
        cookies=COOKIES,
    )
    timestamp = datetime.now().timestamp()
    tree = ET.fromstring(response.text)

    html = tree.findtext('data')
    soup = BeautifulSoup(html, 'html.parser')

    session_data = []
    sessions = soup.find_all(attrs={'id': 'activity-course-row'})

    for session in sessions:
        barcode = int(session.find("td", {'headers': 'Barcode'}).text)
        available = int(session.find("td", {'headers': 'Available'}).text)
        title = str(session.find("td", {'headers': 'Course'}).find('div').text)
        location = str(session.find(
            "td", {'headers': 'Complex'}).find('a').text).strip(" \n")

        # Date / time information
        date_info = str(session.find(
            "td", {'headers': 'Dates'}).text).split('-')

        year, month, day = parse_date(date_info)

        time_info = str(session.find(
            "td", {'headers': 'Times'}).text).split('-')

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


def scrape() -> List[dict]:
    data = []
    for i in range(20):
        sessions = scrape_page(i)

        if len(sessions) == 0:
            break

        data.extend(sessions)

    return sessions


if __name__ == '__main__':
    scrape()
