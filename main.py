#
# header comment! Overview, name, etc.
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
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute("SELECT strftime('%Y-%m-%d', MIN(Ride_Date)) FROM Ridership;")
    row = dbCursor.fetchone();
    dbCursor.execute("SELECT strftime('%Y-%m-%d', MAX(Ride_Date)) FROM Ridership;")
    row2 = dbCursor.fetchone();
    print("  date range:", row[0], " - ", row2[0]);

    dbCursor.execute("Select SUM(Num_Riders) From Ridership;")
    row = dbCursor.fetchone();
    print("  Total ridership:", f"{row[0]:,}")

    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_of_Day = 'W';")
    row = dbCursor.fetchone();
    print("  Weekday ridership:", f"{row[0]:,}", "({:0.2f}%)".format((row[0]/3377404512) * 100))

    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_of_Day = 'A';")
    row = dbCursor.fetchone();
    print("  Saturday ridership:", f"{row[0]:,}", "({:0.2f}%)".format((row[0]/3377404512) * 100))

    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_of_Day = 'U';")
    row = dbCursor.fetchone();
    print("  Sunday/holiday ridership:", f"{row[0]:,}", "({:0.2f}%)".format((row[0]/3377404512) * 100))
  
    dbCursor.close()

def find_stations(dbConn):
  dbCursor = dbConn.cursor();
  stationName = input("Enter partial station name (wildcards _ and %): ");
  
  if '_' in stationName or '%' in stationName:
      # Execute SQL query with parameterized value
      sql = "SELECT * FROM Stations WHERE Station_Name LIKE ? ORDER BY Station_Name ASC;";
      dbCursor.execute(sql, [stationName]);
      # Output station names in ascending order
      for row in dbCursor.fetchall():
          print(row[0], ":", row[1]);
  else:
    print("**No stations found...");
    
  dbCursor.close()

def find_all_ridership(dbConn):
  dbCursor = dbConn.cursor();
  
  print("** ridership all stations **");
  sql = "SELECT Stations.Station_Name, SUM(Ridership.Num_Riders) FROM Ridership INNER JOIN Stations ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY Station_Name ASC;"
  dbCursor.execute(sql);
      # Output station names in ascending order
  for row in dbCursor.fetchall():
    percentage = (row[1]/3377404512) * 100;
    print(row[0], ":", "{:,}".format(row[1]), f"({percentage:.2f}%)");

  dbCursor.close()

def find_top_ridership(dbConn):
  dbCursor = dbConn.cursor();
  
  print("** top-10 stations **");
  sql = "SELECT Stations.Station_Name, SUM(Ridership.Num_Riders) FROM Ridership INNER JOIN Stations ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY SUM(Ridership.Num_Riders) DESC LIMIT 10;"
  dbCursor.execute(sql);
      
  for row in dbCursor.fetchall():
    percentage = (row[1]/3377404512) * 100;
    print(row[0], ":", "{:,}".format(row[1]), f"({percentage:.2f}%)");

  dbCursor.close()

def find_least_ridership(dbConn):
  dbCursor = dbConn.cursor();
  
  print("** least-10 stations **");
  sql = "SELECT Stations.Station_Name, SUM(Ridership.Num_Riders) FROM Ridership INNER JOIN Stations ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY SUM(Ridership.Num_Riders) ASC LIMIT 10;"
  dbCursor.execute(sql);
      
  for row in dbCursor.fetchall():
    percentage = (row[1]/3377404512) * 100;
    print(row[0], ":", "{:,}".format(row[1]), f"({percentage:.2f}%)");

  dbCursor.close()

def find_line_color(dbConn):
  dbCursor = dbConn.cursor();
  
  line_color = input("Enter a line color (e.g. Red or Yellow): ").lower().capitalize();
  sql = "SELECT Stops.Stop_Name, Stops.Direction, Stops.ADA FROM Stops INNER JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID INNER JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID WHERE Lines.Color = ? ORDER BY Stops.Stop_Name ASC;"
  dbCursor.execute(sql, [line_color]);
  rows = dbCursor.fetchall();
  
  if len(rows) > 0:
    for result in rows:
        stop_name = result[0]
        direction = result[1]
        ada = result[2]
        acc_str = 'yes' if ada else 'no'
        print(f"{stop_name} : direction = {direction} (accessible? {acc_str})")
  else:
    print("No such line...")

  dbCursor.close()

def find_ridership_month_plot(dbConn):
  dbCursor = dbConn.cursor();
  
  sql = "SELECT strftime('%m', Ride_Date) AS Month, SUM(Num_Riders) FROM Ridership GROUP BY Month ORDER BY Month ASC;"
  
  dbCursor.execute(sql);
  rows = dbCursor.fetchall();

  months = []
  riderships = []
  if len(rows) > 0:
      for result in rows:
          month = result[0]
          ridership = result[1]
          print(f"{month:02} : {ridership:,}")
          months.append(month)
          riderships.append(ridership)
        
  plot = input("Plot? (y/n): ").lower()
  # Plot results
  if plot == 'y':
      plt.xlabel("Month")
      plt.ylabel("Ridership (in Millions)")
      plt.title("Total Ridership by Month")
      plt.plot(months, riderships)
      plt.show()

  dbCursor.close()

def find_ridership_year_plot(dbConn):
  dbCursor = dbConn.cursor();
  
  sql = "SELECT strftime('%Y', Ride_Date) AS Year, SUM(Num_Riders) FROM Ridership GROUP BY Year ORDER BY Year ASC;"
  
  dbCursor.execute(sql);
  rows = dbCursor.fetchall();

  years = []
  riderships = []
  if len(rows) > 0:
      for result in rows:
          year = result[0]
          ridership = result[1]
          print(f"{year:02} : {ridership:,}")
          years.append(year)
          riderships.append(ridership)
        
  plot = input("Plot? (y/n): ").lower()
  # Plot results
  if plot == 'y':
    plt.xlabel("Year")
    plt.ylabel("Ridership (in Millions)")
    plt.title("Total Ridership by Year")
    plt.plot(years, riderships)
    plt.show()

  dbCursor.close()


def find_ridership_two_year_plot(dbConn):
  dbCursor = dbConn.cursor();
  year = input('Year to compare against? ');
  nyear = year;
  station1_name = input('Enter station 1 (wildcards _ and %): ')

  if '_' in station1_name or '%' in station1_name:
    query1 = "SELECT Ridership.Station_ID, Stations.Station_Name, strftime('%Y-%m-%d',Ride_Date), Num_Riders FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID WHERE strftime('%Y',Ride_Date) = ? and Station_Name LIKE ?";
    dbCursor.execute(query1, [year, station1_name])
    station1_data = dbCursor.fetchall()
  else:
    print("**No stations found...");

  station2_name = input('Enter station 2 (wildcards _ and %): ')
  
  if '_' in station2_name or '%' in station2_name:
    query2 = "SELECT Ridership.Station_ID, Stations.Station_Name, strftime('%Y-%m-%d',Ride_Date), Num_Riders FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID WHERE strftime('%Y',Ride_Date) = ? and Station_Name LIKE ?";
    dbCursor.execute(query2, [year, station2_name])
    station2_data = dbCursor.fetchall()
    # Print data for stations
    if len(station1_data) > 0:
      print('Station 1:', station1_data[0][0], station1_data[0][1])
      for row in station1_data[:5]:
          print(row[2], row[3])
      for row in station1_data[-5:]:
          print(row[2], row[3])

    if len(station2_data) > 0:
      print('Station 2:', station2_data[0][0], station2_data[0][1])
      for row in station2_data[:5]:
          print(row[2], row[3])
      for row in station2_data[-5:]:
          print(row[2], row[3])
    
    rYears = []
    riderships = []
    anum = 0;
    if len(station1_data) > 0:
      for result in station1_data:
          year = anum
          ridership = result[3]
          rYears.append(year)
          riderships.append(ridership)
          anum += 1

    rYears1 = []
    riderships1 = []
    anum = 0
    if len(station2_data) > 0:
      for result in station2_data:
          year1 = anum
          ridership1 = result[3]
          rYears1.append(year1)
          riderships1.append(ridership1)
          anum += 1
    
    # Check if user wants to plot
    plot = input('Plot? (y/n) ')
  
    if plot == 'y':
      plt.title('Daily Ridership at ' + station1_data[0][1] + ' and ' + station2_data[0][1] + ' for ' + nyear)
      plt.xlabel('Date')
      plt.ylabel('Ridership')
      plt.plot(rYears, riderships)
      plt.plot(rYears1, riderships1)
      plt.legend(['Ridership at ' + station1_data[0][1], 'Ridership at ' + station2_data[0][1]])
      plt.show()
  else:
    print("**No stations found...");
    
  dbCursor.close()

def find_station_location(dbConn):
  dbCursor = dbConn.cursor();
  line_color = input('Enter a line color (e.g. Red or Yellow): ').lower().capitalize();
  
  sql = "SELECT DISTINCT Stations.Station_Name, Stops.Latitude, Stops.Longitude FROM Stops INNER JOIN StopDetails ON StopDetails.Stop_ID = Stops.Stop_ID INNER JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID INNER JOIN Stations ON Stations.Station_ID = Stops.Station_ID WHERE Lines.Color = ? ORDER BY Stops.Stop_Name ASC;"
  
  dbCursor.execute(sql, [line_color]);
  rows = dbCursor.fetchall();

  x = []
  y = []
  
  if rows:
    for row in rows:
        station_name = row[0]
        latitude = row[1]
        longitude = row[2]
        x.append(row[2])
        y.append(row[1])
        print(f'{station_name} : ({latitude}, {longitude})')

          
    plot = input("Plot? (y/n): ").lower()
    # Plot results
    if plot == 'y':
      image = plt.imread("chicago.png")
      xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map:
      plt.imshow(image, extent=xydims)
      
      plt.title(line_color + " line")
      #
      # color is the value input by user, we can use that to plot the
      # figure *except* we need to map Purple-Express to Purple:
      #
      if (line_color.lower() == "purple-express"):
       line_color="Purple" # color="#800080"
      
      plt.plot(x, y, "o", c=line_color)
      #
      # annotate each (x, y) coordinate with its station name:
      #
      for row in rows:
       plt.annotate(row[0], (row[1], row[2]))
      
      plt.xlim([-87.9277, -87.5569])
      plt.ylim([41.7012, 42.0868])
      
      plt.show()
            
  else:
    print(f'No such line "{line_color}"...')

  dbCursor.close()
##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

while True:
    command = input("Please enter a command (1-9, x to exit): ");
    if command == '1':
      find_stations(dbConn);
    elif command == '2':
      find_all_ridership(dbConn);
    elif command == '3':
      find_top_ridership(dbConn);
    elif command == '4':
      find_least_ridership(dbConn);
    elif command == '5':
      find_line_color(dbConn);
    elif command == '6':
      find_ridership_month_plot(dbConn);
    elif command == '7':
      find_ridership_year_plot(dbConn);
    elif command == '8':
      find_ridership_two_year_plot(dbConn);
    elif command == '9':
      find_station_location(dbConn);
    elif command == 'x':
        break
    else:
        print("**Error, unknown command, try again...")
#
# done
#
