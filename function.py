from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def get_data_soup(url_data):
    url = url_data
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def get_data_header(soup):
    header_items = []
    names = []
    schedule_table = soup.find('table', {'class': 'listtbl'})
    schedule_list = schedule_table.find_all('tr')
    schedule_header = schedule_list[0]
    header_items_temp = schedule_header.find_all('td', {'class': 'rline'})
    for i in header_items_temp:
        header_items.append(i.text)
    names_temp = schedule_header.find_all('a')
    for i in names_temp:
        names.append(i.text)
    return names, header_items

def get_data_schedule(soup, names, header_items):
    schedule_table = soup.find('table', {'class': 'listtbl'})
    schedule_list = schedule_table.find_all('tr')
    lines = []
    dates = []
    schedule_items = schedule_list[1:]
    for schedule_item in schedule_items:
        line = {}
        date = schedule_item.find('td').text
        dates.append(date)
        attendance_temp = schedule_item.find_all('td')
        attendance_temp = attendance_temp[len(header_items)+1:]
        for i, name in zip(attendance_temp, names):
            line[name] = i.text

        #print(line)
        lines.append(line)
    
    df_sc = pd.DataFrame(lines, index=dates)
    return df_sc


def get_expl(soup):
    return soup.find('div', {'class':'explbox'}).text

def get_comment(soup):
    comment = soup.find('div',{'class':"commentbox"}).find('li').text
    comment = comment.strip()
    comment = comment.replace(' ', '')
    comment_list = re.split('[()]', comment)
    return comment_list[1:]
