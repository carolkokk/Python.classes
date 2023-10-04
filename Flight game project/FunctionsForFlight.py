import random
import
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='spy_plane',
    user='root',
    password='Mariaroot6',
    autocommit=True
)


# fetch airports from different continents
def get_eu_airports():
    sql = """select iso_country, ident, name, type, latitude_deg, longitude_deg
from airport 
where iso_country in(select iso_country from airport where continent = "EU")
and ident in(select min(ident) from airport where continent = "EU" 
and not type = "closed" group by iso_country)
order by rand()
limit 50;"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_africa_airports():
    sql = """select iso_country, ident, name, type, latitude_deg, longitude_deg
    from airport 
    where iso_country in(select iso_country from airport where continent = "AF")
    and ident in(select min(ident) from airport where continent = "AF" 
    and not type = "closed" group by iso_country)
    order by rand()
    limit 50;"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_asia_airports():
    sql = """select iso_country, ident, name, type, latitude_deg, longitude_deg
    from airport 
    where iso_country in(select iso_country from airport where continent = "AS")
    and ident in(select min(ident) from airport where continent = "AS" 
    and not type = "closed" group by iso_country)
    order by rand()
    limit 50;"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# Maybe exclude this one
def get_north_am_airports():
    sql = """select iso_country, ident, name, type, latitude_deg, longitude_deg
    from airport 
    where iso_country in(select iso_country from airport where continent = "NA")
    and ident in(select min(ident) from airport where continent = "NA"
    and not type = "closed" group by iso_country)
    order by rand()
    limit 40;"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# fetch goals
def get_goals():
    sql = "select * from goal;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def new_game(player_name, current_airport, battery_power, all_airports):
    sql = "insert into game(screen_name, location, battery_power, score) values (%s, %s, %s, %s);"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (player_name, current_airport, battery_power))
    game_id = cursor.lastrowid

    # Excluding starting airport
    game_airport = all_airports[1:].copy()
    random.shuffle(game_airport)

    # Adding goals
    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    for i, goal_id in enumerate(goal_list):
        sql = "insert into spying_location (game, goal, airport) values (%s, %s, %s);"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, (game_id, game_airport[i]['ident'], goal_id))

    return game_id


# Get airport information
def get_airport_info(icao):
    sql = (f"select country.name, ident, airport.name, latitude_deg, longitude_deg from airport, country "
           f"where airport.iso_country = country.iso_country and ident = %s;")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, icao)
    result = cursor.fetchall()
    return result


# Set airport as visited
def airport_visited(game, airport):
    sql = f"update spying_location set visited = 1 where game = %s and airport = %s;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (game, airport))


# What goal is in the location
def location_goal(game_id, location):
    sql = (f"select spying_location.id, goal, goal.id as goal, name, points from spying_location "
           f"inner join goal on goal.id = spying_location.goal where game = %s and airport = %s; ")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (game_id, location))
    result = cursor.fetchone()
    return result

# Distance between airports
def airport_distance
def location_update(icao, bat_power, score):
    sql = f"update game set location = %s, battery_power = %s, score = %s where id = %s;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, bat_power, score))


def path_game(path_choice):
    rand_path = random.randint(1, 5)
    if path_choice == rand_path:
        return "Oh no! You were not careful and got caught..."
    else:
        return "Path successful! You got 10% extra battery power and 15 points"
