'''
WORK IN PROGRESS

'''

from bs4 import BeautifulSoup
import requests


html_url = "https://www.basketball-reference.com/boxscores/?month=2&day=13&year=2021"
page = requests.get(html_url)
soup = BeautifulSoup(page.text, 'html.parser')

urls = []
for line in soup.find_all("td", {"class": "right gamelink"}):
    urls.append('https://www.basketball-reference.com/boxscores/pbp/'
                + line.a.get('href').split('/')[-1])


month_day_dictionary = {1: 31, 2: 28, 3: 30, 4: 30, 5: 31, 6: 30, 7: 31,
                        8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


# test day with no games
html_url_1 = 'https://www.basketball-reference.com/boxscores/?month=7&day=13&year=2021'
page1 = requests.get(html_url_1)
soup1 = BeautifulSoup(page1.text, 'html.parser')

def get_url_date(year, month, day, urls):
    html_url = "https://www.basketball-reference.com/boxscores" \
               "/?month=" + str(month) + "&day=" + str(day) \
               + "&year=" + str(year)
    print(html_url)
    page = requests.get(html_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(soup.find_all("strong")[1].getText())
    if "No games played on this date" != soup.find_all("strong")[
        1].getText():

        for line in soup.find_all("td", {"class": "right gamelink"}):
            urls.append(
                'https://www.basketball-reference.com/boxscores/pbp/'
                + line.a.get('href').split('/')[-1])
    elif "Pourly Formed Request (400 error)" == soup.find_all("strong")[1].getText():
        print(soup.get_text)

def get_urls(start_year, start_month, end_year, end_month):

    urls = []
    current_year = start_year
    current_month = start_month
    while current_year <= end_year:

        while current_month <= 12:

            print(current_year, current_month)
            for day in range(1, month_day_dictionary[current_month] + 1):
                print(current_year, current_month, day)
                html_url = "https://www.basketball-reference.com/boxscores" \
                           "/?month="+ str(current_month) + "&day="+ str(day) \
                           + "&year=" + str(current_year)
                print(html_url)
                page = requests.get(html_url)
                soup = BeautifulSoup(page.text, 'html.parser')
                print(soup.find_all("strong")[1].getText())
                if "No games played on this date" != soup.find_all("strong")[1].getText():

                    for line in soup.find_all("td", {"class": "right gamelink"}):
                        urls.append(
                            'https://www.basketball-reference.com/boxscores/pbp/'
                            + line.a.get('href').split('/')[-1])

            current_month += 1
            if current_year == end_year and current_month == end_month + 1:
                break
        current_month = 1
        current_year += 1

    return urls
# a = get_urls(2022,11,2022,11)