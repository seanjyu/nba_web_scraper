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
play_team - text - Team of player that committed the play<br>
shot_type - int - Type of shot<br>
- 0 - 2-pt Jump shot 
- 1 - Layup
- 2 - 3-put Jump shot
- 3 - Dunk
- 4 - Hook shot
- 5 - Free throw

make - int - Whether the shot was made<br>
- 0 - Miss
- 1 - Make

distance - int - Distance of shot<br>
assist_player - text - Player who assisted shot, if no assist then the string "none" is entered<br>
away_score - int - Away score after play<br>
home_score - int - Home score after play<br>

<ins>Rebound Stats</ins><br>
game_number - integer - Number of game in scraping session<br>
away_team - text - Name of away team<br>
home_team - text - Name of home team<br>
min_in_game - integer - Minute in game play is made<br>
sec_in_game - float - Second of minute in game play is made<br>
rebounder - text - Player who obtained rebound<br>
play_team - text - Team of player that committed the play<br>
shot_type - int - Type of shot that was rebounded (Same as offensive stats)<br>
- 0 - 2-pt Jump shot 
- 1 - Layup
- 2 - 3-put Jump shot
- 3 - Dunk
- 4 - Hook shot
- 5 - Free throw

distance - int - Distance of shot that was rebounded<br>
rebound_type - int - Type of rebound
- 0 - Defensive 
- 1 - Offensive

<ins>Turnover Stats</ins><br>
game_number - integer - Number of game in scraping session<br>
away_team - text - Name of away team<br>
home_team - text - Name of home team<br>
min_in_game - integer - Minute in game play is made<br>
sec_in_game - float - Second of minute in game play is made<br>
turnover_player - text - Player who committed turnover<br>
player_team - text - Team of player that committed the play<br>
turnover_type - int - Type of turnover<br>
- 0 - Steal
- 1 - Double dribble
- 2 - Shot clock
- 3 - Offensive foul
- 4 - Out of bounds
- 5 - Palming
- 6 - Traveling
- 7 - Back court

steal_player - text - Player who stole the ball, if no player stole ball then the string "none" is entered<br>

<ins>Foul Stats</ins><br>
game_number - integer - Number of game in scraping session<br>
away_team - text - Name of away team<br>
home_team - text - Name of home team<br>
min_in_game - integer - Minute in game play is made<br>
sec_in_game - float - Second of minute in game play is made<br>
fouled_player - text - Player who was fouled<br>
play_team - text - Team whose player was fouled<br>
foul_committer - text - Player who committed the foul<br>
foul_type - int - Type of foul
- 0 - Shooting
- 1 - Personal take
- 2 - Loose ball
- 3 - Technical
- 4 - Defensive 3 seconds
- 5 - Offensive
- 6 - Flagrant
- 7 - Personal

<ins>Miscellaneous Stats</ins><br>
game_number - integer - Number of game in scraping session<br>
away_team - text - Name of away team<br>
home_team - text - Name of home team<br>
min_in_game - integer - Minute in game play is made<br>
sec_in_game - float - Second of minute in game play is made<br>
misc_type - integer - Type of miscellaneous stat<br>
- 0 - Player entering game
- 1 - Time out
- 2 - Violation
- 3 - Instant Reply

play_team - text - Team whose player was fouled<br>
NOTE - for the following columns if the type does not apply then the string "none" will be entered<br>
player_in - text - Player entering game<br>
player_out - text - Player exiting game<br> 
time_out_team - text - Team that called timeout<br>
violation - text - Type of violation<br>
replay_request - text - Description of replay request<br>
jump_ball_player_home - text - Player from home team participating in first jump ball<br>
jump_ball_player_away - text - Player from away team participating in first jump ball<br>