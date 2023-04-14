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
print(soup1.find_all("strong")[1].getText())

def get_urls(start_year, start_month, end_year, end_month):
    number_of_years = end_year - start_year
    urls = []
    for month_add in range(number_of_years * 12):
        curr_year = month_add // 12 + start_year
        curr_month = (month_add + start_month) % 12
        if curr_year == end_year and curr_month == end_month:
            return urls
        for day in range(1, month_day_dictionary[curr_month] + 1):
            html_url = "https://www.basketball-reference.com/boxscores" \
                       "/?month="+ str(curr_month) + "&day="+ str(day) \
                       + "&year=" + str(curr_year)

            page = requests.get(html_url)
            soup = BeautifulSoup(page.text, 'html.parser')
            if "No games played on this date" != soup.find_all("strong")[1].getText():

                for line in soup.find_all("td", {"class": "right gamelink"}):
                    urls.append(
                        'https://www.basketball-reference.com/boxscores/pbp/'
                        + line.a.get('href').split('/')[-1])

    return urls