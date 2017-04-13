import requests
from bs4 import BeautifulSoup


def get_title_top1000():
    n = 1
    result = []
    while n < 1001:
        url = 'https://www.letssingit.com/artists/popular/{}'.format(n)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")

        items = soup.find_all('a', 'high_profile')

        for item in items:
            singer = item.string
            result.append(singer)
            n += 1
        print(result)
        # return result

# get_title_top1000()


# def get_title():
#     url = 'http://www.billboard.com/charts/billboard-200'
#     source_code = requests.get(url)
#     plain_text = source_code.text
#     soup = BeautifulSoup(plain_text, "html.parser")
#
#     # print(soup)
#
#
#     main = soup.find(id='main')
#     # pprint(main)
#
#     items = main.find_all('div', 'chart-row__title')
#     # print(items)
#
#     result = []
#
#     for item in items:
#         title = item.find('h2').string.strip()
#         # print(title)
#         result.append(title)
#
#     return result




# list_v2 = soup.find('table', 'table_as_list_v2 rnk1 img2')
# # pprint(list_v2)
#
# items = list_v2.find_all('a', 'high_profile')
# # items = list_v2.find_all('td')
# pprint(items)
#
# test = items.getText()
#
# print(test)
#
# singer = items.string.a.strip()
# pprint(singer)


# result = []

# for item in items:
#     singer = item.find('a > high_profile').string.strip()
#     print(singer)
#     result.append(singer)
#     # print(result)
# return result

# get_title_top1000()


# def get_page(url):
#     """Get the text of the web page at the given URL
#     return a string containing the content"""
#
#     fd = urlopen(url)
#     content = fd.read()
#     fd.close()
#
#     return content.decode('utf8')


# def spider():
#     url = 'http://www.billboard.com/charts/billboard-200'
#     source_code = requests.get(url)
#     plain_text = source_code.text
#
#     links = set()
#     text = get_page(url)
#
#     soup = BeautifulSoup(plain_text, "html.parser")
#
#     for link in soup.find_all('a'):
#         if 'href' in link.attrs:
#             links.add(link.attrs['href'])
#     # print(links)
#
#     return links


# def find_assignments(text):
#     url = 'http://www.billboard.com/charts/billboard-200'
#     source_code = requests.get(url)
#     plain_text = source_code.text
#
#     soup = BeautifulSoup(plain_text, "html.parser")
#
#     for link in soup.find_all('a'):
#         if 'href' in link.attrs:
#             links.add(link.attrs['href'])
#     # print(links)
#
#     return links

#
# def spider(text):
#     url = 'http://www.billboard.com/charts/billboard-200'
#     source_code = requests.get(url)
#     plain_text = source_code.text
#     # soup = BeautifulSoup(plain_text, "html.parser")
#     # print(soup)
#
#     soup = BeautifulSoup(text)
#
#     chart_row_container = soup.find_all('div', 'chart_row_container')
#
#     result = []
#
#     for row in chart_row_container:
#         title = row.find('div', 'h2').string.strip()
#         artist = row.find('div', 'a').string.strip()
#         result.append(title, artist)
#     print(result)
#     return result

# def spider():
#     url = 'http://www.billboard.com/charts/billboard-200'
#     source_code = requests.get(url)
#     plain_text = source_code.text
#     soup = BeautifulSoup(plain_text, "html.parser")
#
#     # print(soup)
#
#     result = []
#
#     for item in soup.select('div > h2'):
#         title = item.string
#         # print(title)
#         result.append(title)
#         pprint(result)
#     return result
#
# spider()
