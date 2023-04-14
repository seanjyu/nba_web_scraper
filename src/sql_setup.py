import requests
import pymysql
from pymysql.constants import CLIENT

'''

'''
table_columns = {
    "individual_game_stats": "(game_number, date, time_start, arena, "
                             "away_team, home_team, away_city,"
                             " home_city, reg_season,"
                             " jump_ball_player_away,"
                             " jump_ball_player_home,"
                             " jump_ball_winning_team,"
                             " home_score, away_score, winner)",

    "offensive_stats": "(game_number, away_team, home_team,"
                       " min_in_game, sec_in_game, player, play_team,"
                       " shot_type, make, distance, assist_player,"
                       " away_score, home_score)",

    "rebound_stats": "(game_number, away_team, home_team,"
                     " min_in_game, sec_in_game, rebounder,"
                     " play_team, shot_type, distance, rebound_type)",

    "turnover_stats": "(game_number, away_team, home_team,"
                      " min_in_game, sec_in_game, turnover_player,"
                      " player_team, turnover_type, steal_player)",

    "foul_stats": "(game_number, away_team, home_team, min_in_game,"
                  " sec_in_game, fouled_player, play_team,"
                  " foul_committer, foul_type)",

    "misc_stats": "(game_number, away_team, home_team, min_in_game,"
                  " sec_in_game, misc_type, play_team, player_in,"
                  " player_out, violation, time_out_team, replay_request,"
                  " jump_ball_player_away, jump_ball_player_home)"
    }


'''
Set up sql
If already have tables set up then can comment out this section.
'''
def start_connection():
    connection = pymysql.connect() # update with unique connection information.
    cursor = connection.cursor()
    return connection, cursor

def end_cursor_connection(connection, cursor):
    cursor.close()
    connection.close()

def create_tables(cursor):
    # create tables to store data
    cursor.execute("CREATE DATABASE NBA_data;")
    cursor.execute("USE NBA_data;")
    cursor.nextset()
    sql_create_table_0 = '''
    create table individual_game_stats (
    id int not null auto_increment,
    game_number int,
    date date,
    time_start text,
    arena text,
    away_team text,
    home_team text,
    away_city text,
    home_city text,
    reg_season text,
    jump_ball_player_away text,
    jump_ball_player_home text,
    jump_ball_winning_team text,
    home_score text,
    away_score text,
    winner text,
    primary key (id)
    )
    '''
    cursor.execute(sql_create_table_0)

    # Create table 1
    sql_create_table_1 = '''
    create table offensive_stats (
    id int not null auto_increment,
    game_number int,
    away_team text,
    home_team text,
    min_in_game int,
    sec_in_game float, 
    player text,
    play_team text,
    shot_type int,
    make int,
    distance int,
    assist_player text,
    away_score int,
    home_score int,
    primary key (id)
    )
    '''
    cursor.execute(sql_create_table_1)

    # Create table 2
    sql_create_table_2 = '''
    create table rebound_stats (
    id int not null auto_increment,
    game_number int,
    away_team text,
    home_team text,
    min_in_game int,
    sec_in_game float, 
    rebounder text,
    play_team	text,
    shot_type int,
    distance int,
    rebound_type int,
    primary key (id)
    )
    '''
    cursor.execute(sql_create_table_2)

    # Create table 3
    sql_create_table_3 = '''
    create table turnover_stats (
    id int not null auto_increment,
    game_number int,
    away_team text,
    home_team text,
    min_in_game int,
    sec_in_game float, 
    turnover_player text,
    player_team	text,
    turnover_type int,
    steal_player text,
    primary key (id)
    )
    '''
    cursor.execute(sql_create_table_3)

    # Create table 4
    sql_create_table_4 = '''
    create table foul_stats (
    id int not null auto_increment,
    game_number int,
    away_team text,
    home_team text,
    min_in_game int,
    sec_in_game float, 
    fouled_player text,
    play_team text,
    foul_committer text,
    foul_type int,
    primary key (id)
    )
    '''
    cursor.execute(sql_create_table_4)

    # Create table 4
    sql_create_table_5 = '''
    create table misc_stats (
    id int not null auto_increment,
    game_number int,
    away_team text,
    home_team text,
    min_in_game int,
    sec_in_game float, 
    misc_type int,
    play_team text,
    player_in text,
    player_out text,
    time_out_team text,
    violation text,
    replay_request text,
    jump_ball_player_away text,
    jump_ball_player_home text,
    primary key (id)
    )
    '''
    cursor.execute(sql_create_table_5)

def reset_tables(cursor, connection, database, tables):
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor.execute("USE " + database + ";")
    for table in tables:
        table_delete = "DELETE FROM " + table + ";"
        print(table_delete)
        cursor.execute(table_delete)
        connection.commit()

def add_single_row(cursor, connection, data_base, table, data):
    # print(len(data), len(table_columns[table].split(" ")))

    if len(table_columns[table].split(" ")) != len(data):
        print(table)
        raise Exception("Number of data values must be the same as the "
                        "number of columns")

    cursor.execute("USE " + data_base + ";")
    cursor.nextset()

    str_add = "INSERT INTO " + table + " " + table_columns[table] \
              + " VALUES ("
    for value in data:
        if type(value) == str:
            str_add += "'" + value + "',"
        else:
            str_add += str(value) + ","
    str_add = str_add[0:-1]
    str_add += ");"
    cursor.execute(str_add)
    connection.commit()

def view_all_rows(cursor, data_base, table):
    cursor.execute("USE " + data_base + ";")
    cursor.nextset()
    cursor.execute("SELECT * FROM " + table + ";")
    print(cursor.fetchall())

# test values
a = 1
b = 1.1
c = "test"
test_add_data = [3, 'test', 'test', 1, 0.0, 'test', 'test', 'test', 10]
connection, cursor = start_connection()