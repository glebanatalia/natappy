# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:37:08 2016

@author: WaR7
"""

#!/Users/WaR7/anaconda/python

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

facebook_reshares={}
twitter_reshares={}
links=[]


def screenname_to_linkname(blogger,media):
    a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
    b=pandas.DataFrame(a)
    return list(b[b['Blogger']==blogger][media])[0]

def linkname_to_screenname(blogger,media):
    a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
    b=pandas.DataFrame(a)
    return list(b[b[media]==blogger]['Blogger'])[0]


def username_to_id(blogger):
    a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
    b=pandas.DataFrame(a)
    return list(b[b['Instagram']==blogger]['Instagram ID'])[0]


    
def followers_fb(blogger,logg_details):
    if blogger == 'nothing':
        return [], 0       
    link = "https://graph.facebook.com/v2.5/%s?fields=likes&access_token=%s"%(blogger,logg_details['token'])         
    try:    
        followers = requests.get(link).json()['likes']
    except:
        followers=0
    return followers 
                


def get_followers_count_ig(blogger,logg_details):
    link='https://api.instagram.com/v1/users/%s?access_token=%s' %(username_to_id(blogger),logg_details['token'])   
    run_out_of_limits = False
    try:
        followers1=requests.get(link) 
        print ('Instagram limits left:', followers1.headers['X-Ratelimit-Remaining'])
        if int(followers1.headers['X-Ratelimit-Remaining'])<30:
            run_out_of_limits = True
        else:
            followers=requests.get(link).json()['data']['counts']['followed_by']   
    except Exception as e:
        print (e)
        print ('Instagram followers count error. Api response: ',requests.get(link).json())
        raise Exception('Instagram API Error')        
    if run_out_of_limits:
        raise Exception('You run out of rate limits. Application must close now. Please try again in 30 minutes.')
    return followers


def pagination_tw_inside(blogger,twapi,replies=None,retweets=None):
    recent_media=[]  
    followers=0
    for tweet in tweepy.Cursor(twapi.user_timeline, twapi, screen_name=blogger, count=1, include_rts=True).items(limit=1): 
        
        followers=tweet.author.followers_count
        if hasattr(tweet, 'retweeted_status'):  
            retweeted=True
            likes=tweet.retweeted_status.favorite_count
            retweet=tweet.retweeted_status.retweet_count  
        else:
            retweeted=False
            likes=tweet.favorite_count  
            retweet=tweet.retweet_count 
        replied=True if tweet.in_reply_to_status_id_str!=None and tweet.in_reply_to_screen_name!=None else False            
        tweet_link='https://twitter.com/%s/status/%s' %(blogger,tweet.id) 
        tweet_tags=['#'+hashtag['text'] for hashtag in tweet.entities.get('hashtags')]+['@'+mension['screen_name'] for mension in tweet.entities.get('user_mentions')]
        tweet_dict= {'tweet_id':tweet.id, 'text':str(tweet.text), 
         'retweeted':retweeted,                                        
         'likes': likes,
         'retweet': retweet,                                                             
         'created_at':str(tweet.created_at),
         'replied':replied,
         'in_reply_to_user_ID_str': str(tweet.in_reply_to_screen_name), 
         'in_reply_to_status_id': str(tweet.in_reply_to_status_id_str),
         'link':str(tweet_link),
         'tags':list(tweet_tags)}
        recent_media+=[tweet_dict] 
    print ('Twitter',len(recent_media),'posts checked for blogger:', blogger )            
    return followers
    
def pagination_tw(blogger,twapi,replies,retweets):
    if blogger=='nothing':
        return [],0
    counter=0
    while counter<15:
    #else:
        try:
            return pagination_tw_inside(blogger,twapi)
        except Exception as e:
            print ('Can not connect host. Next trial in 30 sec. Exception:',e)
            time.sleep(30)
            return pagination_tw(blogger,twapi,replies,retweets)
            counter+=1
         #print ('Exception:', e, 'blogger:', blogger)
         #pass
    return 0

def twitter_passwords_():
    passwords=[]
    file=([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open('%s/Desktop/natappy/passwords/twitter_passwords.txt' %home,'r') if ',' in line])   
    for line in file:
        appaswords={}
        appaswords['consumer_key']=line[0]
        appaswords['consumer_secret']=line[1]
        appaswords['token']=line[2]
        appaswords['token_secret']=line[3]
        appaswords['name']=line[4]
        appaswords['username']=line[5]
        appaswords['password']=line[6]
        passwords.append(appaswords)
    return passwords
    
twitter_passwords = twitter_passwords_()

def instagram_passwords_():
    passwords=[]
    file=([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open('%s/Desktop/natappy/passwords/instagram_passwords.txt' %home,'r') if ',' in line])   
    for line in file:
        appaswords={}
        appaswords['client_id']=line[0]
        appaswords['client_secret']=line[1]
        appaswords['token']=line[2]
        appaswords['name']=line[3]
        appaswords['username']=line[4]
        appaswords['password']=line[5]
        passwords.append(appaswords)
    return passwords
    
instagram_passwords = instagram_passwords_()
    
def facebook_passwords_():
    passwords=[]
    file=([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open('%s/Desktop/natappy/passwords/facebook_passwords.txt' %home,'r') if ',' in line])   
    for line in file:
        appaswords={}
        appaswords['expires']=line[0]
        appaswords['token']=line[1]
        appaswords['name']=line[2]
        appaswords['username']=line[3]
        appaswords['password']=line[4]
        passwords.append(appaswords)
    return passwords
    
facebook_passwords = facebook_passwords_()

def logg():
   return {'Facebook': cycle(facebook_passwords),'Instagram': cycle(instagram_passwords),'Twitter': cycle(twitter_passwords)}

TEMP = logg()   
def get_password(platform):
    with LOCK:
        password = next(TEMP[platform])
    return password



def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


   
def split_text(text):
    return textwrap.wrap(text,60)



def excel(posts):  
    print ('creating excel')

    workbook = xlsxwriter.Workbook('%s/Desktop/Report.xlsx' %(home))
    worksheet = workbook.add_worksheet()
    fieldsnames= ('MEDIA','BLOGGER','FOLLOWERS')

    col = 0    
    for name in fieldsnames:
      #  sheet[str(columns[0])+str(row)]=name
        worksheet.write(0, col,name)
        col += 1
    row=1   
    for post in posts:
        col=0              
        for name in post[:3]:         
            worksheet.write(row,col,name)
        #    sheet[str(columns[col])+str(row)]=name
            col+=1
        row+=1
   # wb.save('%s/Desktop/%s/Report.xlsx' %(home,dirname))
    workbook.close()
 
platshort={'Facebook':'FB','Instagram':'IG','Twitter':'TW','Blogs':'BL'}     


a=pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' %home)
b=pandas.DataFrame(a)
bloggers=list(b['Blogger'])

if __name__ == '__main__':
    follows=[]
    for blogger in bloggers:  
        print (blogger)
        blogerfoll=[blogger]
        blogger1=screenname_to_linkname(blogger,'Facebook')
        logg_details=get_password('Facebook')
        blogerfoll.append(followers_fb(blogger1, logg_details))
        bloggerig=screenname_to_linkname(blogger,'Instagram')
        logg_details=get_password('Instagram')
        blogerfoll.append(get_followers_count_ig(bloggerig,logg_details))
        logg_details=get_password('Twitter')    
        blogger3=screenname_to_linkname(blogger,'Twitter')
        auth = tweepy.AppAuthHandler(logg_details['consumer_key'], logg_details['consumer_secret'])
        twapi = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)
        blogerfoll.append(pagination_tw_inside(blogger3,twapi))
        print (blogger)
        print (blogerfoll)
        follows.append(blogerfoll)
        