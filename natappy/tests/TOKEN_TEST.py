# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:32:20 2015

@author: WaR7
"""
import requests
from os.path import expanduser
import tweepy
from tweepy import TweepError

home = expanduser("~")




def facebook_passwords_():    
    passwords=[]
    file=([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open('%s/Desktop/natappy/passwords/facebook_passwords.txt' %home,'r') if ',' in line])   
    for line in file:
        appaswords={}
        appaswords['token']=line[1]
        passwords.append(appaswords)
    return passwords
    
facebook_passwords = facebook_passwords_()


def trial_fb(logg_details,todate=[2015, 11, 29],fromdate=[2015,11,30],blogger='AliGordonPage'):
    until = "%s/%s/%s" %(todate[0],todate[1],todate[2])
    since = "%s/%s/%s" %(fromdate[0],fromdate[1],fromdate[2])  
    link = "https://graph.facebook.com/v2.5/%s?fields=likes,posts.until(%s).since(%s){link,message,shares,status_type,created_time,likes.summary(true),comments.summary(true)}&access_token=%s"%(blogger,until, since,logg_details)         
    return requests.get(link)
    
    
for logg_details in facebook_passwords:
    print ('token:', logg_details['token'])
    print ('response',trial_fb(logg_details['token']))
    

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


def trial_ig(logg_details):
    link='https://api.instagram.com/v1/users/183238952?access_token=%s' %logg_details['token']    
    return requests.get(link)


for logg_details in instagram_passwords:
    print ('token:', logg_details['token'])
    apiresponse=trial_ig(logg_details)
    print ('response',apiresponse)
    if  not apiresponse.ok   :       
        print ('Token:',logg_details['token'],'failed. Application name:',logg_details['name'],'account username:',logg_details['username'],'password:',logg_details['password'])
            
    
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

def trial_tw(logg_details):   
    auth = tweepy.OAuthHandler(logg_details['consumer_key'], logg_details['consumer_secret'])
    auth.set_access_token(logg_details['token'], logg_details['token_secret'])
    twapi = tweepy.API(auth)
    autho=twapi
    try:
        a=autho.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
        print ('Token:', logg_details['token'])
        print ('<Response 200>')
    except TweepError:
        print ('Token:', logg_details['token'], 'failed. Application name:',logg_details['name'],'Account username:',logg_details['username'],'Password:', logg_details['password'] )
    except Exception as e:
        print ('Another exception:',e)

for logg_details in twitter_passwords:
    trial_tw(logg_details)


