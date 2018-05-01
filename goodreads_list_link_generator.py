import requests, lxml.html
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

s = requests.session()
login = s.get("https://www.goodreads.com/user/sign_in")

login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
form['user[email]'] = "bcarlborg@gmail.com"
form['user[password]'] = "8bpa6w6PwmK"
response = s.post("https://www.goodreads.com/user/sign_in", data=form)
print("response: url: ", response.url)
print("beau in response", ("beau" in response.text))

list_2 = s.get("https://www.goodreads.com/shelf/show/project-gutenberg?page=1")
# print(list_2.text)
soup = BeautifulSoup(list_2.text, 'html.parser')
link_list = soup.find_all("a", class_="bookTitle", href=True)

base_url = "https://www.goodreads.com"
url_list = []
for book in link_list:
  print(publish_info(base_url + book['href']))
