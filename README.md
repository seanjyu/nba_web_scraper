# NBA Web Scraper

<ins>Scraper.py</ins>

This script is designed to scrape data from basketball-reference.com for a particular day, specifically the play-by-play data for each game played that day. The script uses Python 3 and the following libraries: BeautifulSoup, requests, pyodbc, pymysql, and dateutil.

To use this script, the user must specify the day they want to scrape in the 'html_url' variable. The script then pulls all game URLs for that day, and for each game URL, pulls data such as date, time start, arena, home team, away team, end score, and player shot data (including the player name, shot type, assister, and distance).

The script is also designed to set up an SQL connection and create tables, but this functionality can be commented out if the tables are already set up.

Note that the script only scrapes data for one day at a time, and the user must modify the script to scrape data for additional days.

The stats are split into 6 tables with some overlapping columns. Below is a description of the columns in each table.

<ins>Game Stats</ins><br>
game_number - integer - Number of game in scraping session<br>
date - date - Date the game is played<br>
time_start - text - Time game started <br> 
arena - text - Name of arena <br>
away_team - text - Name of away team<br>
home_team - text - Name of home team<br>
home_city - text - City of home team<br>
away_city - text - City of away team<br>
reg_season - int - Indicates which stage of the season the game is played
- 0 - Regular season
- 1 - Play-in
- 2 - First round
- 3 - Conference semi-finals
- 4 - Conference finals
- 5 - NBA finals

jump_ball_player_home - text - Player from home team participating in first jump ball<br>
jump_ball_player_away - text - Player from away team participating in first jump ball<br>
jump_ball_winning_team - text - Winning team of jump ball<br>
home_end_score - int - Score of home team<br>
away_end_score - int - Score of away team<br>
winner - int - Winning team<br>

<ins>Offensive Stats</ins><br>
game_number - integer - Number of game in scraping session<br>
away_team - text - Name of away team<br>
home_team - text - Name of home team<br>
min_in_game - integer - Minute in game play is made<br>
sec_in_game - float - Second of minute in game play is made<br>
player - text - Name of player<br>
play_team - text - Team of player that commited the play<br>
shot_type - int - Type of shot<br>
make - int - Whether the shot was made<br>
- 0 - Miss
- 1 - Make

distance - int - Distance of shot<br>
assist_player - text - Player who assisted shot<br>
away_score - int - Away score after play<br>
home_score - int - Home score after play<br>