import compdf
import newpdf
from selenium import webdriver
from time import gmtime, strftime
from selenium.webdriver.support import ui
from functools import partial
from PIL import Image
from instagram.client import InstagramAPI
from os.path import expanduser
import concurrent.futures
import xlsxwriter
import requests
import textwrap
import os
import time
import tweepy
import threading
import pickle
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
import natappy
import compet
import fbcompet
import fbshares
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

maxTweets = 2000
tweetsPerQry = 100
sinceId = None
max_id = 0


def collect_facebook_reshares(dirname, facebook_reshares):
    if facebook_reshares:
        with suppress(Exception):
            os.makedirs('%s/Desktop/%s/Facebook_shares' % (home, dirname))
            print('going to collect reshares info')
            for blogger in facebook_reshares.keys():
                for post in facebook_reshares[blogger].keys():
                    only_post_id = post.split('_')[1]
                    post_reshares = fbshares.collecting_reshares_everything(only_post_id, dirname)
                    facebook_reshares[blogger][post] = post_reshares
    return facebook_reshares


def collect_twitter_reshares(dirname, twitter_reshares):
    if twitter_reshares:
        return fbshares.collect_retweets(twitter_reshares)


def campaign_competition(blogpost, comptags, competition, campaign, brandname, excludetags, bloggers, tags, repformat, platforms, fromdate, todate, replies, retweets, blogposts):

    post_info = {}
    #  all_media,followers_data for competition
    all_media = {}
    followers_data = {'Twitter': {}, 'Instagram': {}, 'Facebook': {}}
    platshorts = '_'.join([natappy.platshort[platform] for platform in platforms])
    dirname = '%s-%s-%s' % (platshorts, '_'.join([tag for tag in tags]),
                            str(strftime("%Y_%m_%d_%H_%M", gmtime())))
    with suppress(Exception):
        os.makedirs('%s/Desktop/%s' % (home, dirname))
    if repformat == 'Full':
        for platform in platforms:
            with suppress(Exception):
                os.makedirs('%s/Desktop/%s/%s_screenshots' % (home, dirname, platform))
    for platform in [plat for plat in competition if plat not in['Facebook', 'Blogs']]:
        with suppress(Exception):
            os.makedirs('%s/Desktop/%s/%s_screenshots' % (home, dirname, platform))
        all_media[platform] = compet.competition(platform, bloggers, followers_data, startdate=fromdate,
                                                 searchQuery=comptags, maxTweets=maxTweets, tweetsPerQry=tweetsPerQry, max_id=max_id, sinceId=sinceId)
    if 'Facebook' in competition:
        with suppress(Exception):
            os.makedirs('%s/Desktop/%s/Facebook_screenshots' % (home, dirname))
        all_media['Facebook'] = fbcompet.collecting_reshares_everything(
            tags, dirname=dirname, followers_data=followers_data, fromdate=fromdate, todate=todate)

    pickle.dump(all_media, open(
        '{home}/Desktop/natappy/pickle/all_media.pickle'.format(home=home), 'wb'))
    pickle.dump(dirname, open(
        '{home}/Desktop/natappy/pickle/dirname.pickle'.format(home=home), 'wb'))
    pickle.dump(followers_data, open(
        '{home}/Desktop/natappy/pickle/followers_data.pickle'.format(home=home), 'wb'))

    followers_data = pickle.load(
        open('{home}/Desktop/natappy/pickle/followers_data.pickle'.format(home=home), 'rb'))
    dirname = pickle.load(
        open('{home}/Desktop/natappy/pickle/dirname.pickle'.format(home=home), 'rb'))
    all_media = pickle.load(
        open('{home}/Desktop/natappy/pickle/all_media.pickle'.format(home=home), 'rb'))

    if repformat == 'Full':
        compet.collect_screenshots(dirname)
        compdf.excel(dirname, all_media, followers_data)


#---------------------------------------------------------------------------------------------------------#

    all_media2 = {}
    followers_data2 = natappy.create_followers_data(bloggers, platforms)

    for platform in [plat for plat in platforms if plat not in ['Blogs']]:
        all_media2[platform] = natappy.get_post_with_tags(
            bloggers, platform, tags, repformat, fromdate, todate, followers_data2, replies, retweets, excludetags, dirname)

    pickle.dump(all_media2, open(
        '{home}/Desktop/natappy/pickle/all_media2.pickle'.format(home=home), 'wb'))
    pickle.dump(followers_data2, open('{home}/Desktop/followers2.pickle'.format(home=home), 'wb'))

    all_media2 = pickle.load(
        open('{home}/Desktop/natappy/pickle/all_media2.pickle'.format(home=home), 'rb'))
    followers_data2 = pickle.load(
        open('{home}/Desktop/natappy/pickle/followers2.pickle'.format(home=home), 'rb'))

    facebook_reshares = natappy.facebook_reshares
    twitter_reshares = natappy.twitter_reshares

    reshares = {'Facebook': {}, 'Twitter': {}}
    reshares['Facebook'] = collect_facebook_reshares(dirname, facebook_reshares)
    reshares['Twitter'] = collect_twitter_reshares(dirname, twitter_reshares)

    pickle.dump(reshares, open(
        '{home}/Desktop/natappy/pickle/reshares.pickle'.format(home=home), 'wb'))
    reshares = pickle.load(
        open('{home}/Desktop/natappy/pickle/reshares.pickle'.format(home=home), 'rb'))
    fbshares.nice_reshares_excel(reshares, dirname)
    if repformat == 'Full':
        natappy.collect_screenshots(dirname)
        if 'Blogs' in platforms:
            post_info = natappy.collect_blog_screenshots(dirname, blogposts)
            pickle.dump(post_info, open(
                '{home}/Desktop/natappy/pickle/postsinfo.pickle'.format(home=home), 'wb'))

    rep = canvas.Canvas("%s/Desktop/%s/%s-%s.pdf" % (home, dirname, dirname,
                                                     str(strftime("%Y_%m_%d_%H_%M_%S", gmtime()))), pagesize=A4)
    rep.setPageSize(landscape(A4))
    newpdf.welcome_pages(rep, brandname, campaign)
    if bloggers:
        newpdf.site_statistic_page(rep, all_media2, followers_data2, bloggers, platforms)
        if len(all_media2.keys()) == 3:
            newpdf.social_media_reach_page(rep, all_media2, followers_data2, reshares)
        if len(all_media2.keys()) == 2:
            newpdf.two_social_media_reach_page(rep, all_media2, followers_data2, reshares)
        if len(all_media2.keys()) == 1:
            newpdf.one_social_media_reach_page(rep, all_media2, followers_data2, reshares)
        if 'Instagram' in platforms:
            newpdf.Instagram_results_page(rep, bloggers, all_media2, followers_data2)
        if 'Twitter' in platforms:
            newpdf.Twitter_results_page(rep, bloggers, all_media2, followers_data2)
        if 'Facebook' in platforms:
            newpdf.Facebook_results_page(rep, bloggers, all_media2, followers_data2)

    all_media = compdf.select_others_posts(all_media, bloggers)
    if len(all_media.keys()) == 3:
        compdf.social_media_reach_page(rep, all_media, followers_data)
    if len(all_media.keys()) == 2:
        compdf.two_social_media_reach_page(rep, all_media, followers_data)
    if len(all_media.keys()) == 1:
        compdf.one_social_media_reach_page(rep, all_media, followers_data)

    if repformat != 'Quick':
        with suppress(Exception):
            if bloggers:
                for blogger in bloggers:
                    if post_info:
                        if blogger in blogposts:
                            if blogposts[blogger]:
                                newpdf.blogger_blogposts_page(
                                    rep, dirname, blogger, blogposts, post_info)
                    newpdf.blogger_social_media_page(rep, dirname, blogger, all_media2)
        with suppress(Exception):
            compdf.other_social_media_page(rep, bloggers, dirname, all_media)
    newpdf.last_page(rep)
    rep.save()
    natappy.excel(all_media2, dirname, tags, followers_data2)


if __name__ == '__main__':
    info = {'replies': False, 'comptags': ['peonyliminzanziba'], 'fromdate': [2016, 2, 9], 'blogposts': [], 'todate': [2016, 2, 16], 'blogpost': {'Peony Lim': ['http://peonylim.com/']}, 'bloggers': ['Peony Lim'], 'retweets': False,
            'format': 'Full', 'campaign': '', 'brandname': 'competition+bloggers+blog', 'tags': ['peonyliminzanziba'], 'platforms': ['Facebook', 'Instagram', 'Twitter', 'Blogs'], 'excludetags': ['Exclude tag'], 'competition': ['Instagram', 'Twitter']}

    campaign_competition(info['blogpost'], info['comptags'], info['competition'], info['campaign'], info['brandname'], info['excludetags'], info[
                         'bloggers'], info['tags'], info['format'], info['platforms'], info['fromdate'], info['todate'], info['replies'], info['retweets'], info['blogposts'])
