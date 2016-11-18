# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:37:09 2016

@author: WaR7
"""


from selenium import webdriver
from time import gmtime, strftime
from selenium.webdriver.support import ui
from functools import partial
from PIL import Image
from instagram.client import InstagramAPI
from os.path import expanduser
import concurrent.futures, xlsxwriter, requests, textwrap, os, time, tweepy,threading,pickle
from datetime import datetime
from itertools import cycle
from contextlib import suppress
from datetime import timedelta
home = expanduser("~")
LOCK = threading.Lock()
from selenium.common.exceptions import WebDriverException
import fbshares
import newpdf
import pandas 
import shutil
import urllib
import openpyxl
import numpy as np
import natappy


a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
b=pandas.DataFrame(a)


bloggers_database=list(b['Blogger'])
print (bloggers_database)


def collect(blogger):
    natappy.create_report([blogger],['Facebook','Instagram','Twitter'],['a','i','e','y',''],'Quick',[2009, 3, 3],[2016, 3, 10],False,False,['excludetags'],'','',{})




for blogger in bloggers_database:
    try:
        collect(blogger)
    except:
        pass
    
    
#https://github.com/glebanatalia/my-first-blog.git