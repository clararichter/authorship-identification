import requests
from bs4 import BeautifulSoup
import csv
import re

def publish_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title_box = soup.find("h1", class_ = "bookTitle" )
    title = title_box.contents[0].strip()

    authors_box = soup.find_all("span", itemprop ="name")
    author = []
    for a in authors_box:
        author += a.contents

    date_box = soup.find_all("div", class_="row", limit = 2)
    pub = date_box[1].find("nobr", class_ = "greyText")
    if pub == None:
        pub = date_box[1].contents[0]
    pub = list(map(int, re.findall(r'\d+', pub.string)))
    if len(pub) == 1:
        date =  pub[0]
    else:
        date = pub[1]

    return {"title": title, "author": author, "date": date}




print(publish_info("https://www.goodreads.com/book/show/40395.A_Princess_of_Mars"))
