from bs4 import BeautifulSoup
import requests
import pyodbc
import pymysql
from pymysql.constants import CLIENT
from sql_setup import *
from dateutil import parser
'''
Constants
'''
season_start_2018 = 0
season_end_2019 = 0
season_start_2019 = 0
season_end_2020 = 0
cur_season = 2018

'''
Season Dates (for convenience)
'''
start_year = 2015
start_month = 9
start_day = 1
end_year = 2022

'''
Set up sql
If already have tables set up then can comment out this section.
'''
# connection = pymysql.connect(host='nba-analytics.cyp7gxsmmebm.us-east-2.rds.amazonaws.com', user='admin', password='AJ19vddc4982p', client_flag = CLIENT.MULTI_STATEMENTS)
# cursor = connection.cursor()
# database_names = cursor.execute("SHOW DATABASES;")
# print(cursor.fetchall())

'''
Scrape Helper Functions
'''
def shot(row_string, shot_result):
    if shot_result == 1:
        split_str = row_string.split("makes")
        if "assist" in split_str[1]:
            assister = split_str[1].split("by ")[1][0:-1]
        else:
            assister = "none"
    else:
        split_str = row_string.split("misses")
        assister = "none"

    player = split_str[0]

    # find shot type
    if "2-pt jump shot" in split_str[1]:
        shot_type = 0
    elif "layup" in split_str[1]:
        shot_type = 1
    elif "3-pt jump shot" in split_str[1]:
        shot_type = 2
    elif "dunk" in split_str[1]:
        shot_type = 3
    elif "hook" in split_str[1]:
        shot_type = 4
    elif "free throw" in split_str[1]:
        shot_type = 5

    # find shot distance
    if "at rim" in split_str[1]:
        distance = 0
    elif "free throw" not in split_str[1]:
        distance = int(split_str[1].split("from ")[1].split(" ft")[0])
    else:
        distance = 15

    return [player, shot_type, assister, distance]

'''
Web Scrape
'''
# Loop through htmls
# TO DO - loop through dates to create a string to webscrape

html_url = "https://www.basketball-reference.com/boxscores/?month=2&day=13&year=2021"
page = requests.get(html_url)
soup = BeautifulSoup(page.text, 'html.parser')
# Print page to verify.
#print(soup.prettify())

# Store urls of games on that given day
urls = []
for line in soup.find_all("td", {"class": "right gamelink"}):
    urls.append(line.a.get('href'))

pbp_url = 'https://www.basketball-reference.com/boxscores/pbp/202206020GSW.html'

game_number = 0

# get html of individual page
pbp_req = requests.get(pbp_url)
pbp_soup = BeautifulSoup(pbp_req.text, 'html.parser')
'''
Individual game data
game_number - 
date - 
time_start -
arena - 
home_team -
away_team -
home_city -
away_city -
reg_season - 
jump_ball_player_home - 
jump_ball_player_away - 
jump_ball_winning_team -
'''
# scrape date
date = ' '.join(pbp_soup.find('div', class_='scorebox').find('div',class_='scorebox_meta').find('div').get_text().split(', ')[1:]).replace(',','')
date = parser.parse(date)
date = date.strftime('%Y-%m-%d %H:%M:%S')
# scrape time_start
time_start = pbp_soup.find('div',class_='scorebox').find('div',class_='scorebox_meta').find('div').get_text().split(',')[0]
# scrape arena
arena = pbp_soup.find('div',class_='scorebox').find('div',class_='scorebox_meta').find_all('div')[1].get_text().replace(',','')
# scrape home and away teams
teams_text = pbp_soup.find('div',class_='breadcrumbs').find('div',class_='crumbs').get_text()
if ":" in teams_text:
    str_to_split = teams_text[teams_text.index(":") + 2:]
    teams_text_split = str_to_split.split(" ")
else:
    teams_text_split = teams_text.split(" ")[9:-4]

# print(teams_text_split)
at_index = teams_text_split.index('at')
away_team = " ".join(teams_text_split[0:at_index])
home_team = " ".join(teams_text_split[at_index + 1:])
# scrape end score
score_text = pbp_soup.find("title").find_next("meta").get_attribute_list("content")[0].split(" vs ")
away_end_score = int(score_text[0].split("(")[1].split(")")[0])
home_end_score = int(score_text[1].split("(")[1].split(")")[0])
if home_end_score > away_end_score:
    winner = 1
else:
    winner = 0
# scrape home and away cities
home_city = pbp_soup.find('table',id='pbp').find_all("tr", {"class":"thead"})[1].find_all("th")[-1].get_text()
away_city = pbp_soup.find('table',id='pbp').find_all("tr", {"class":"thead"})[1].find_all("th")[1].get_text()

# scrape reg_season
title = pbp_soup.find('title').get_text()
if "NBA Finals" in title:
    season = 5
elif "Conference Finals" in title:
    season = 4
elif "Conference Semifinals" in title:
    season = 3
elif "First Round" in title:
    season = 2
elif "Play-In" in title:
    season = 1
else:
    season = 0

# scrape jump ball home and away players and winning team
# find line with first jump ball
jump_ball_line = pbp_soup.find('table', id='pbp').find("td", {"class": "center"})
jump_ball_player_home = jump_ball_line.get_text().split("Jump ball: ")[1].split(" vs.")[0]
jump_ball_player_away = jump_ball_line.get_text().split("Jump ball: ")[1].split(" vs.")[1].split(" (")[0]
# need to analyze line after jump ball to see who won
line_after_jump = jump_ball_line.find_next("tr").find_all("td")
# determine which column is empty and assign variable non_empty_str
if line_after_jump[1].get_text().isspace():
    # left column is empty, therefore need to analyze right column
    non_empty_str = line_after_jump[5].get_text()
    if 'shot' in non_empty_str \
            or 'Offensive foul' in non_empty_str \
            or 'Turnover' in non_empty_str \
            or 'dunk' in non_empty_str \
            or 'layup' in non_empty_str \
            or 'hook' in non_empty_str:
        jump_ball_winning_team = home_team
    elif 'foul' in non_empty_str:
        jump_ball_winning_team = away_team

else:
    # right column is empty, therefore need to analyze left column
    non_empty_str = line_after_jump[1].get_text()
    if 'shot' in non_empty_str \
            or 'Offensive foul' in non_empty_str \
            or 'Turnover' in non_empty_str \
            or 'dunk' in non_empty_str \
            or 'layup' in non_empty_str \
            or 'hook' in non_empty_str:
        jump_ball_winning_team = away_team
    elif 'foul' in non_empty_str:
        jump_ball_winning_team = home_team

data_individual_game = [game_number, date, time_start, arena, away_team,
                        home_team, away_city, home_city, season,
                        jump_ball_player_away, jump_ball_player_home,
                        jump_ball_winning_team, away_end_score,
                        home_end_score, winner]
print(data_individual_game)
connection, cursor = start_connection()
add_single_row(cursor, connection, "NBA_data", "individual_game_stats",
              data_individual_game)
# end_cursor_connection(connection, cursor)


'''
Scrape Game Statistics
'''
game_time_min_counter = 0
count = 0
home_score = 0
away_score = 0
for item in pbp_soup.find('table',id='pbp').find_all('tr'):
    # initialize list for data to be appended
    database_data = []

    # analyze text of row
    row_text = item.get_text()
    # if row contains any of these strings then no need to analyze
    if home_city in row_text \
            or "Start of" in row_text \
            or "End of" in row_text \
            or "1st Q" in row_text:
        continue

    # keep track of time
    if "2nd Q" in row_text \
            or "3rd Q" in row_text \
            or "4th Q" in row_text \
            or "OT" in row_text:
        game_time_min_counter += 12
        continue

    # find all div td here since rows with quarters dont have any div td
    row_divs = item.find_all("td")

    # if row divs empty skip row
    if len(row_divs) == 0:
        continue


    row_time = row_divs[0].get_text().split(":")
    # Need different time calculations for overtime and regular time.
    if row_time[0] == "5" and "OT" in row_text:
        if row_time[0] == "5":
            minute = 5
            second = 0
        else:
            minute = 4 - int(row_time[0])
            second = 60 - float(row_time[1])
    else:
        if row_time[0] == "12":
            minute = 0
            second = 0
        else:
            minute = 11 - int(row_time[0])
            second = 60 - float(row_time[1])
    cur_minute = game_time_min_counter + minute
    cur_second = second

    # first keep track of jump balls since only 2 divs
    if "Jump ball" in row_divs[1].get_text():
        table = 5
        player_in = "none"
        player_out = "none"
        time_out_team = "none"
        violation = "none"
        replay_request = "none"
        play_team = "none"
        misc_type = 5
        jump_ball_away_player_1 = row_divs[1].get_text().split("Jump ball: ")[1].split(" vs.")[0]
        jump_ball_home_player_2 = row_divs[1].get_text().split("Jump ball: ")[1].split(" vs.")[1].split(" (")[0]

        # TODO add to sql
        # print(game_number, away_team, home_team, cur_minute, cur_second, misc_type, player_in, player_out, time_out_team, violation, jump_ball_away_player_1, jump_ball_home_player_1)
        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, misc_type, play_team, player_in, player_out,
                    time_out_team, violation, replay_request,
                    jump_ball_away_player_1,
                    jump_ball_home_player_2]
        continue

    # keep track of score
    score_div = row_divs[3]
    score_text = score_div.get_text().split("-")
    home_score = score_text[1]
    away_score = score_text[0]

    # if left column is empty, then need to analyze right column
    if row_divs[1].get_text().isspace():
        non_empty_col = row_divs[5].get_text()
        play_team = home_team
        opposing_team = away_team
    else:
        non_empty_col = row_divs[1].get_text()
        play_team = away_team
        opposing_team = home_team

    if "make" in non_empty_col:
        # output variables
        table = "offensive_stats"
        make = 1
        player, shot_type, assister, distance = shot(non_empty_col, 1)
        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, player, play_team, shot_type, 1, distance,
                    assister, away_score, home_score]
    elif "miss" in non_empty_col:
        table = "offensive_stats"
        make = 0
        player, shot_type, assister, distance = shot(non_empty_col, 0)
        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, player, play_team, shot_type, 0, distance,
                    assister, away_score, home_score]
    elif "rebound" in non_empty_col:
        table = "rebound_stats"
        rebounder = non_empty_col.split("by ")[1]
        if "Defensive" in non_empty_col:
            rebound_type = 0
        else:
            rebound_type = 1
        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, rebounder, play_team, shot_type, distance,
                    rebound_type]
    elif "Turnover" in non_empty_col:
        table = "turnover_stats"
        turnover_split = non_empty_col.split("by ")
        turnover_player = turnover_split[1].split(" (")[0]
        steal_player = "none"
        turnover_type = 0
        if "steal" in turnover_split[1]:
            steal_player = turnover_split[2][0:-1]
            turnover_type = 1
        elif "double dribble" in turnover_split[1]:
            turnover_type = 2
        elif "shot clock" in turnover_split[1]:
            turnover_type = 3
        elif "offensive foul" in turnover_split[1]:
            turnover_type = 4
        elif "out of bounds" in turnover_split[1]:
            turnover_type = 5
        elif "palming" in turnover_split[1]:
            turnover_type = 6
        elif "traveling" in turnover_split[1]:
            turnover_type = 7
        elif "back court" in turnover_split[1]:
            turnover_type = 8
        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, turnover_player, play_team, turnover_type,
                    steal_player]

    elif "foul" in non_empty_col:
        table = "foul_stats"
        foul_split = non_empty_col.split("foul")

        # get fouled player and player who committed foul
        if " (drawn" in foul_split[1]:
            # if foul is drawn by another player
            foul_split_1 = foul_split[1].split("(drawn by ")
            foul_committer = foul_split_1[0].split("by ")[1]
            fouled_player = foul_split_1[1][0:-1]
        else:
            # if is not drawn by another player (i.e. technical fouls)
            if "by " in foul_split[1]:
                fouled_player = "none"
                foul_committer = foul_split[1].split("by ")[1]
            else:
                foul_committer = foul_split[1]
                fouled_player = "none"

        if "Shooting" in foul_split[0]:
            foul_type = 0
        elif "Personal take" in foul_split[0]:
            foul_type = 1
        elif "Loose ball" in foul_split[0]:
            foul_type = 2
        elif "Technical" in foul_split[0]:
            foul_type = 3
            # switch play team since opposing team committed technical foul
            play_team, opposing_team = opposing_team, play_team
        elif "Def 3 sec" in foul_split[0]:
            foul_type = 4
            # switch play team since opposing team committed technical foul
            play_team, opposing_team = opposing_team, play_team
        elif "Offensive" in foul_split[0]:
            foul_type = 5
        elif "Flagrant" in foul_split[0]:
            foul_type = 6
        else:
            foul_type = 7
        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, fouled_player, play_team,
                    foul_committer, foul_type]
    else:
        table = "misc_stats"
        player_in = "none"
        player_out = "none"
        time_out_team = "none"
        violation = "none"
        replay_request = "none"
        jump_ball_away_player_1 = "none"
        jump_ball_home_player_2 = "none"
        if "enters" in non_empty_col:
            misc_type = 1
            col_split = non_empty_col.split(" enters the game for")
            player_in = col_split[0]
            player_out = col_split[1]
        elif "timeout" in non_empty_col:
            misc_type = 2
            time_out_team = non_empty_col.split(" full timeout")[0]
        elif "Violation" in non_empty_col:
            misc_type = 3
            violation = non_empty_col.split("(")[1][0:-1]
        elif "Instant Replay" in non_empty_col:
            misc_type = 4
            replay_request = non_empty_col.split("(")[0:-1]

        data_row = [game_number, away_team, home_team, cur_minute,
                    cur_second, misc_type, play_team, player_in, player_out,
                    time_out_team, violation, replay_request,
                    jump_ball_away_player_1,
                    jump_ball_home_player_2]

    # input into sql
    add_single_row(cursor, connection, "NBA_data", table,
                  data_row)


end_cursor_connection(connection, cursor)