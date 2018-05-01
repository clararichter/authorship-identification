import requests, lxml.html
from bs4 import BeautifulSoup


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

list_2 = s.get("https://www.goodreads.com/shelf/show/project-gutenberg?page=2")
# print(list_2.text)
soup = BeautifulSoup(list_2.text, 'html.parser')
link_list = soup.find_all("a", class_="bookTitle", href=True)

base_url = "https://www.goodreads.com"
url_list = []
for book in link_list:
  url_list.append(base_url + book['href'])

print(url_list)
