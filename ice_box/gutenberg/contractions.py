import requests
from bs4 import BeautifulSoup
import csv

page = requests.get("https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions")
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find("table", class_="wikitable sortable")
pairs = table.find_all("tr")

start = 1
excluded_last = 2

try:
    filename = 'contractions.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['contraction']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(start, len(pairs)-excluded_last):
            con = pairs[i].td.text
            if con == "can't (rarely, cain't)":
                writer.writerow({'contraction': "can't"})
                writer.writerow({'contraction': "cain't"})
            else:
                writer.writerow({'contraction': con})
except csv.Error as e:
    sys.exit('file {}, {}'.format(filename, e))
