from pprint import pprint

import requests
from bs4 import BeautifulSoup

url = 'http://www.billboard.com/charts/billboard-200'

r = requests.get(url)
data = r.text

soup = BeautifulSoup(data, 'html.parser')

# pprint(soup)
#
# title1 = soup.find_all('div')
# pprint(title1)

# div = soup.find('div', {'class': 'class-name'})
#
# ps = div.find_all('p')
# lis = div.find_all('li')
#
# # print the content of all <p> tags
# for p in ps:
#     print(p.text)
#
# # print the content of all <li> tags
# for li in lis:
#     print(li.text)

# title2 = soup.find_all('data-tracklabel')
# pprint(title2)

# test = soup.find_all('div': 'a')
# print(test)
# for singer in soup.find_all('data-tracklabel'):
#     print(singer.get('data-tracklabel'))