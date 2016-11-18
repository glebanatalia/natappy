# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:10:47 2015

@author: WaR7
"""
import requests
from os.path import expanduser
import tweepy
from tweepy import TweepError


home = expanduser("~")

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
    a=autho.rate_limit_status()['resources']
    limits={}
    for limit in a:
        for limit_kind in a[limit]:
            #print (limit_kind)
            limits[limit_kind]=[]
            for limit_kind2 in a[limit][limit_kind]:
                limits[limit_kind].append(a[limit][limit_kind][limit_kind2])
               # print (limit_kind2,a[limit][limit_kind][limit_kind2])
    return limits        
     

for logg_details in twitter_passwords:
    limits=trial_tw(logg_details)
    for limit in limits:
        if limits[limit][0]!=limits[limit][1]:
            print ('Running low of limit:', limit, 'limits left:', str(limits[limit][0])+'/'+ str(limits[limit][1]))
