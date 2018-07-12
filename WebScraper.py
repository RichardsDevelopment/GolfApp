import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import sys
import MySQLdb
import csv

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="golfapp")

cursor= db.cursor()

def update(table, url):
    rows = []
    i = 0

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Exception: ", e)
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'lxml')
    table2 = soup.find_all('table')[1]
    df = pd.read_html(str(table2))

    results = df[0].to_json(orient = 'records')

    parsed = json.loads(results)

    while i < len(parsed):
        name = parsed[i]["PLAYER NAME"]
    
        if parsed[i]["RANK THIS WEEK"][0] == "T":
            rank = int(parsed[i]["RANK THIS WEEK"][1:])
        else:
            rank = int(parsed[i]["RANK THIS WEEK"])

        rows.append((name, rank))
        i+=1

    sql = "TRUNCATE TABLE " + table 
    cursor.execute(sql)

    values = ', '.join(map(str, rows))
    sql = "INSERT INTO " + table + " (name, rank) VALUES {}".format(values)
    cursor.execute(sql)

def updateSalary():
	rows = []

	with open('DKSalaries.csv', 'r') as file:
		fileReader = csv.reader(file)
		
		sql = "TRUNCATE TABLE salaries"
		cursor.execute(sql)
		
		print("Populating salaries for this week...")
		for row in fileReader:
			if(row[0] == "Position"):
				continue
				
			name = row[2]
			salary = int(row[5])
			
			rows.append((name, salary))
		
		data = ", ".join(map(str, rows))
		sql = "INSERT INTO salaries (name, salary) VALUES {}".format(data)
		cursor.execute(sql)
	
	print("Salaries updated!")
		
			
urls = ["https://www.pgatour.com/stats/stat.02671.html","https://www.pgatour.com/stats/stat.138.html",
    "https://www.pgatour.com/stats/stat.120.html","https://www.pgatour.com/stats/stat.101.html","https://www.pgatour.com/stats/stat.102.html",
    "https://www.pgatour.com/stats/stat.103.html","https://www.pgatour.com/stats/stat.02674.html","https://www.pgatour.com/stats/stat.02675.html",
    "https://www.pgatour.com/stats/stat.02564.html","https://www.pgatour.com/stats/stat.130.html", "https://www.pgatour.com/stats/stat.02568.html", "https://www.pgatour.com/stats/stat.129.html"]

tables = ["standings", "top10s", "scoreavg", "drivdist", "drivaccu", "gir", "sgteegreen", "sgtotal", "sgputt", "scram", "sgapproach", "totaldriving"]

j = 0

for j in range(0, len(urls)):
    print("Populating", tables[j], "...")

    update(tables[j], urls[j])

    print(tables[j], "populated!") 

updateSalary()			
	
db.commit() 

db.close()