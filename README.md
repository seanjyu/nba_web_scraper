# NBA Web Scraper

<ins>Scraper.py</ins>

This script is designed to scrape data from basketball-reference.com for a particular day, specifically the play-by-play data for each game played that day. The script uses Python 3 and the following libraries: BeautifulSoup, requests, pyodbc, pymysql, and dateutil.

To use this script, the user must specify the day they want to scrape in the 'html_url' variable. The script then pulls all game URLs for that day, and for each game URL, pulls data such as date, time start, arena, home team, away team, end score, and player shot data (including the player name, shot type, assister, and distance).

The script includes a helper function called 'shot', which extracts data for each shot taken by a player during a game.

The script is also designed to set up an SQL connection and create tables, but this functionality can be commented out if the tables are already set up.

Note that the script only scrapes data for one day at a time, and the user must modify the script to scrape data for additional days.

