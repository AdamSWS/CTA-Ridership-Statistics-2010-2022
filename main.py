#
# Project 01 : Analyzing CTA2 L data in Python
# Calls SQL3 queries in python and manipulates data based on user input
# By: Adam Shaar
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  dbCursor = dbConn.cursor()
  print("General stats:")
  dbCursor.execute("Select count(*) From Stations;")
  row = dbCursor.fetchone()
  print("  # of stations:", f"{row[0]:,}")
  dbCursor.execute("Select count(*) From Stops;")
  row = dbCursor.fetchone()
  print("  # of stops:", f"{row[0]:,}")
  dbCursor.execute("Select count(*) From Ridership;")
  row = dbCursor.fetchone()
  print("  # of ride entries:", f"{row[0]:,}")
  dbCursor.execute(
    "Select min(date(Ride_Date)), max(date(Ride_Date)) From Ridership;")
  row = dbCursor.fetchone()
  print("  date range:", f"{row[0]} - {row[1]}")
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row = dbCursor.fetchone()
  total = row[0]
  print("  Total ridership:", f"{row[0]:,}")
  dbCursor.execute(
    "Select sum(Num_Riders) From Ridership Where Type_of_Day == 'W';")
  row = dbCursor.fetchone()
  pct = "{:.2f}".format((row[0] / total) * 100)
  print("  Weekday ridership:", f"{row[0]:,}", f"({pct}%)")
  dbCursor.execute(
    "Select sum(Num_Riders) From Ridership Where Type_of_Day == 'A';")
  row = dbCursor.fetchone()
  pct = "{:.2f}".format((row[0] / total) * 100)
  print("  Saturday ridership:", f"{row[0]:,}", f"({pct}%)")
  dbCursor.execute(
    "Select sum(Num_Riders) From Ridership Where Type_of_Day == 'U';")
  row = dbCursor.fetchone()
  pct = "{:.2f}".format((row[0] / total) * 100)
  print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({pct}%)")
  dbCursor.close()


def cmd1():
  print()
  # user input station name
  user_input2 = input(
    "Enter partial station name (wildcards _ and %): ").strip()
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select Station_ID, Station_Name from Stations where Station_Name like ? order by Station_Name asc;",
    ('' + user_input2 + '', ))
  rows = dbCursor.fetchall()
  # if user had a valid input
  if rows:
    for row in rows:
      print(f"{row[0]}", ":", f"{row[1]}")
  else:
    # if no stations were found
    print("**No stations found...")


def cmd2():
  print("** ridership all stations **")
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select Station_Name, sum(Num_Riders) from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID group by Station_Name order by Station_Name asc"
  )
  total_ridership = 0
  rows = dbCursor.fetchall()
  for row in rows:
    # getting the total num riders for the pct
    total_ridership += row[1]
  for row in rows:
    # setting up pct
    pct = "{:.2f}".format((row[1] / total_ridership) * 100)
    print(f"{row[0]}", ":", f"{row[1]:,}", f"({pct}%)")


def cmd3():
  print("** top-10 stations **")
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select Station_Name, sum(Num_Riders) from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID group by Station_Name order by sum(Num_Riders) desc limit 10"
  )
  rows = dbCursor.fetchall()
  # getting the total num riders for the pct
  total_ridership = dbCursor.execute("select sum(Num_Riders) from Ridership;")
  total_ridership = total_ridership.fetchone()[0]
  for row in rows:
    # setting up pct
    pct = "{:.2f}".format((row[1] / total_ridership) * 100)
    print(f"{row[0]}", ":", f"{row[1]:,}", f"({pct}%)")


def cmd4():
  print("** least-10 stations **")
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select Station_Name, sum(Num_Riders) from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID group by Station_Name order by sum(Num_Riders) asc limit 10"
  )
  rows = dbCursor.fetchall()
  # getting the total num riders for the pct
  total_ridership = dbCursor.execute("select sum(Num_Riders) from Ridership;")
  total_ridership = total_ridership.fetchone()[0]
  for row in rows:
    # setting up pct
    pct = "{:.2f}".format((row[1] / total_ridership) * 100)
    print(f"{row[0]}", ":", f"{row[1]:,}", f"({pct}%)")


def cmd5():
  print()
  user_input2 = input("Enter a line color (e.g. Red or Yellow): ").strip()
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select Stop_Name, Direction, ADA from Lines inner join StopDetails inner join Stops inner join Stations where Lines.Line_ID = StopDetails.Line_ID and StopDetails.Stop_ID = Stops.Stop_ID and Stops.Station_ID = Stations.Station_ID and Color like ? order by Stop_Name asc;",
    ('' + user_input2 + '', ))
  rows = dbCursor.fetchall()
  if rows:
    # if the user input was valid
    for row in rows:
      if (row[2] == 1):
        # accessability string
        acc = "yes"
      else:
        acc = "no"
      print(f"{row[0]}", ":", f"direction = {row[1]}", f"(accessible? {acc})")
  else:
    print("**No such line...")


def cmd6():
  print("** ridership by month **")
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select strftime('%m', Ride_Date) as month, sum(Num_Riders) from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID Group by month Order by month asc;"
  )
  rows = dbCursor.fetchall()
  for row in rows:
    print(f"{row[0]}", ":", f"{row[1]:,}")
  user_input2 = input("Plot? (y/n) ").strip()
  if user_input2 == 'y':
    # if user wants to plot answer
    months = []
    num_riders = []
    for row in rows:
      # setting up graph
      months.append(row[0])
      num_riders.append(row[1])
    plt.xlabel('month')
    plt.ylabel('number of riders (x * 10^8)')
    plt.title('monthly ridership')
    plt.plot(months, num_riders)
    plt.show()


def cmd7():
  print("** ridership by year **")
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select strftime('%Y', Ride_Date) as Year, sum(Num_Riders) from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID Group by Year Order by Year asc;"
  )
  rows = dbCursor.fetchall()
  for row in rows:
    print(f"{row[0]}", ":", f"{row[1]:,}")
  user_input2 = input("Plot? (y/n) ").strip()
  if user_input2 == 'y':
    # if user wants to plot answer
    years = []
    num_riders = []
    for row in rows:
      # setting up graph
      years.append(row[0][2:])
      num_riders.append(row[1])
    plt.xlabel('years')
    plt.ylabel('number of riders (x * 10^8)')
    plt.title('yearly ridership')
    plt.plot(years, num_riders)
    plt.show()


def cmd8():
  print()
  user_input2 = input("Year to compare against? \n").strip()
  user_input3 = input("Enter station 1 (wildcards _ and %): ").strip()
  dbCursor = dbConn.cursor()
  query = "select date(Ride_Date), Num_Riders, Station_Name, Ridership.Station_ID, strftime('%j', Ride_Date) as day from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID Where Station_Name like ? and strftime('%Y', Ride_Date) = ? order by day asc;"
  dbCursor.execute(query, ('' + user_input3 + '', user_input2))
  rows1 = dbCursor.fetchall()
  query = "select distinct Station_Name from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID Where Station_Name like ? and strftime('%Y', Ride_Date) = ?;"
  dbCursor.execute(query, ('' + user_input3 + '', user_input2))
  check = dbCursor.fetchall()
  if len(check) == 0:
    # making sure the query found a station
    print("**No station found...")
    return
  if len(check) > 1:
    # making sure the query didn't find multiple stations
    print("**Multiple stations found...")
    return
  print()
  user_input4 = input("Enter station 2 (wildcards _ and %): ").strip()
  dbCursor = dbConn.cursor()
  query = "select date(Ride_Date), Num_Riders, Station_Name, Ridership.Station_ID, strftime('%j', Ride_Date) as day from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID Where Station_Name like ? and strftime('%Y', Ride_Date) = ? order by day asc;"
  dbCursor.execute(query, ('' + user_input4 + '', user_input2))
  rows2 = dbCursor.fetchall()
  query = "select distinct Station_Name from Ridership inner join Stations on Ridership.Station_ID = Stations.Station_ID Where Station_Name like ? and strftime('%Y', Ride_Date) = ?;"
  dbCursor.execute(query, ('' + user_input4 + '', user_input2))
  check = dbCursor.fetchall()
  if len(check) == 0:
    # making sure the query found a station
    print("**No station found...")
    return
  if len(check) > 1:
    # making sure the query didn't find multiple stations
    print("**Multiple stations found...")
    return
  print(f"Station 1: {rows1[0][3]}", f"{rows1[0][2]}")
  for row in rows1[:5]:
    print(f"{row[0]}", f"{row[1]}")
  for row in rows1[-5:]:
    print(f"{row[0]}", f"{row[1]}")
  print(f"Station 2: {rows2[0][3]}", f"{rows2[0][2]}")
  for row in rows2[:5]:
    print(f"{row[0]}", f"{row[1]}")
  for row in rows2[-5:]:
    print(f"{row[0]}", f"{row[1]}")
  print()
  user_input5 = input("Plot? (y/n) ").strip()
  if user_input5 == 'y':
    # if user wants to plot answer
    days1 = []
    num_riders1 = []
    num_riders2 = []
    for index, row in enumerate(rows1):
      # setting up graph
      days1.append(index)
      num_riders1.append(row[1])
    for row in rows2:
      # setting up graph
      num_riders2.append(row[1])
    plt.xlabel('day')
    plt.ylabel('number of riders (x * 10^8)')
    plt.title('riders each day of ' + user_input2)
    plt.plot(days1, num_riders1, label=rows1[0][2])
    plt.plot(days1, num_riders2, label=rows2[0][2])
    plt.legend(loc="upper right")
    plt.show()


def cmd9():
  print()
  user_input2 = input("Enter a line color (e.g. Red or Yellow): ").strip()
  dbCursor = dbConn.cursor()
  dbCursor.execute(
    "select distinct Station_Name, Latitude, Longitude from Lines inner join StopDetails inner join Stops inner join Stations where Lines.Line_ID = StopDetails.Line_ID and StopDetails.Stop_ID = Stops.Stop_ID and Stops.Station_ID = Stations.Station_ID and Color like ? order by Station_Name asc;",
    ('' + user_input2 + '', ))
  rows = dbCursor.fetchall()
  if rows:
    # if the user's input was valid
    for row in rows:
      print(f"{row[0]}", ":", f"({row[1]}, {row[2]})")
  else:
    # if the users input was not valid
    print("**No such line...")
    return
  print()
  user_input5 = input("Plot? (y/n) ").strip()
  if user_input5 == 'y':
    # if user wants to plot answer
    lat = []
    lon = []
    for row in rows:
      # setting up graph
      lat.append(row[1])
      lon.append(row[2])
    image = plt.imread("chicago.png")
    # setting the background as a picture of chicago
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    plt.imshow(image, extent=xydims)
    plt.title(user_input2 + " line")
    # setting up the color of the pnts
    if user_input2.lower() == "red":
      color = "Red"
    elif user_input2.lower() == "blue":
      color = "Blue"
    elif user_input2.lower() == "brown":
      color = "Brown"
    elif user_input2.lower() == "green":
      color = "Green"
    elif user_input2.lower() == "orange":
      color = "Orange"
    elif user_input2.lower() == "purple":
      color = "Purple"
    elif user_input2.lower() == "pink":
      color = "Pink"
    else:
      color = "Yellow"
    plt.plot(lon, lat, "o", c=color)
    for row in rows:
      plt.annotate(row[0], (row[2], row[1]))
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show()


##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

while True:
  # while loop for user to input commands
  print()
  user_input = input("Please enter a command (1-9, x to exit): ").strip()
  if user_input == 'x':
    break
  elif user_input == '1':
    cmd1()
  elif user_input == '2':
    cmd2()
  elif user_input == '3':
    cmd3()
  elif user_input == '4':
    cmd4()
  elif user_input == '5':
    cmd5()
  elif user_input == '6':
    cmd6()
  elif user_input == '7':
    cmd7()
  elif user_input == '8':
    cmd8()
  elif user_input == '9':
    cmd9()
  else:
    # invalid command input
    print("**Error, unknown command, try again...")
dbConn.close()
#
# done
#
