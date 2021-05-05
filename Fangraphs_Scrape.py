#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from bs4 import BeautifulSoup
import os
import glob
from datetime import datetime
from dateutil.parser import parse
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui


# In[2]:


info = {}
def make_date_dfs(date):
    info[date] = []
    
    fangraphs_url = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=c%2C6%2C8%2C9%2C10%2C11%2C12%2C13%2C21%2C14%2C16%2C-1%2C24%2C25%2C26%2C307%2C310&season=2021&month=1000&season1=2021&ind=0&team=&rost=&age=&filter=&players=&startdate=' + date + '&enddate=' + date + '&page=1_300')
    fangraphs_soup = BeautifulSoup(fangraphs_url.content,'html.parser')
    fangraphs_table = fangraphs_soup.find_all('table', {'class': 'rgMasterTable'})[0]
    
    fangraphs_pitchers_url = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c%2C7%2C8%2C13%2C14%2C4%2C5%2C11%2C17%2C18%2C24%2C19%2C-1%2C25%2C26%2C27%2C327%2C324%2C-1%2C31%2C331&season=2021&month=1000&season1=2021&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=' + date + '&enddate=' + date + '&page=1_300')
    fangraphs_pitchers_soup = BeautifulSoup(fangraphs_pitchers_url.content,'html.parser')
    fangraphs_pitchers_table = fangraphs_pitchers_soup.find_all('table', {'class': 'rgMasterTable'})[0]
    
    espn_url = requests.get('https://www.espn.com/mlb/schedule/_/date/' + date.replace('-',''))
    espn_soup = BeautifulSoup(espn_url.content,'html.parser')
    espn_table = espn_soup.find_all("table")[0]
    
    for idx, table in enumerate([fangraphs_table, fangraphs_pitchers_table, espn_table]):
        rows = []
        for tr in table.find_all('tr')[1:]:
            cells = []
            tds = tr.find_all('td')
            if len(tds) == 0:
                ths = tr.find_all('th')
                for th in ths:
                    cells.append(th.text.strip())
            else:
                for td in tds:
                    cells.append(td.text.strip())
            rows.append(cells)
        table = rows
        table = pd.DataFrame(rows)
        info[date].append(table)
    return dates


# In[4]:


from datetime import date, timedelta

start_date = date(2021,4,1)
today = date.today()

# this will give you a list containing all of the dates
dates = [str(start_date + timedelta(days=x)) for x in range((today-start_date).days + 1)][:-1]


# In[5]:


for day in dates:
    make_date_dfs(day)


# In[6]:


for day, date_info in info.items():
    if len(date_info) != 3:
        print('length of day is ', len(date_info), ', should be 3')


# In[7]:


def clean_dfs():
    for date, date_info in info.items():
        date_info[0] = date_info[0].drop(1)
        date_info[0].columns = date_info[0].iloc[0]
        date_info[0] = date_info[0].drop(0)
        date_info[0]['Date'] = date
        
        date_info[1] = date_info[1].drop(1)
        date_info[1].columns = date_info[1].iloc[0]
        date_info[1] = date_info[1].drop(0)
        date_info[1]['Date'] = date
       
        date_info[2] = date_info[2].drop(columns=6)
        date_info[2].columns = ['Away','Home','Result','Win','Loss','Save']
        date_info[2]['Date'] = date
        

clean_dfs()


# In[8]:


hitters = 0
pitchers = 1
summary = 2
matchups = 3


# In[9]:


def stack_batter_dfs():
    batter_dfs = []
    for date, date_info in info.items():
        date_info[0].Date = date
        batter_dfs.append(date_info[0])
    return pd.concat(batter_dfs, axis = 0)
batter_season_df = stack_batter_dfs()
def stack_pitcher_dfs():
    pitcher_dfs = []
    for date, date_info in info.items():
        date_info[1].Date = date
        pitcher_dfs.append(date_info[1])
    return pd.concat(pitcher_dfs, axis = 0)
pitcher_season_df = stack_pitcher_dfs()


# In[11]:


info[dates[len(dates)-1]][summary]


# In[12]:


info[dates[len(dates)-1]][hitters]

