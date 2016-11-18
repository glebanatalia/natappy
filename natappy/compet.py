from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.common.exceptions import WebDriverException
from time import gmtime, strftime
from functools import partial
from PIL import Image
from instagram.client import InstagramAPI
from os.path import expanduser
import concurrent.futures
import requests
import os
import time
import tweepy
import threading
from datetime import datetime
from itertools import cycle
from contextlib import suppress
import fbcompet
import compdf
home = expanduser("~")
import pickle
import pandas
import urllib

LOCK = threading.Lock()

maxTweets = 2000
tweetsPerQry = 100
sinceId = None
max_id = 0

links = []


def take_screenshot(url, image_name, note):
    links.append([url, image_name, note])


def screenname_to_linkname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b['blogger'] == blogger][media])[0]


def linkname_to_screenname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b[media] == blogger]['blogger'])[0]


def instagram_passwords_():
    passwords = []
    file = ([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open(
        '%s/Desktop/natappy/passwords/instagram_passwords.txt' % home, 'r') if ',' in line])
    for line in file:
        appaswords = {}
        appaswords['client_id'] = line[0]
        appaswords['client_secret'] = line[1]
        appaswords['token'] = line[2]
        appaswords['name'] = line[3]
        appaswords['username'] = line[4]
        appaswords['password'] = line[5]
        passwords.append(appaswords)
    return passwords

instagram_passwords = instagram_passwords_()


def process_post(post, platform, logg_details, bloggers, followers_data, startdate):
    if platform == 'Twitter':
        author_name = post.author.screen_name
        onepost = process_post_twitter(post, author_name, bloggers, followers_data, startdate)
    if platform == 'Instagram':
        author_name = post.user.username
        onepost = process_post_instagram(
            logg_details, post, author_name, bloggers, followers_data, startdate)
    return onepost


def get_followers_count_ig(user_id, logg_details):
    link = 'https://api.instagram.com/v1/users/%s?access_token=%s' % (
        user_id, logg_details['token'])

    followers1 = requests.get(link)
    print('Instagram limits left:', followers1.headers['X-Ratelimit-Remaining'])
    if int(followers1.headers['X-Ratelimit-Remaining']) < 30:
        followers = 0
        raise Exception(
            'You run out of rate limits. Application must close now. Please try again in 30 minutes.')
    followers = requests.get(link).json()['data']['counts']['followed_by']
    return followers


def process_post_instagram(logg_details, post, author_name, bloggers, followers_data, fromdate):
    from_ = datetime(fromdate[0], fromdate[1], fromdate[2])
    time_ = time_ = datetime(int(str(post.created_time)[:10].split(
        '-')[0]), int(str(post.created_time)[:10].split('-')[1]), int(str(post.created_time)[:10].split('-')[2]))
    if post.caption and post.caption.text and time_ >= from_:
        if 'smashbox' in str(post.caption.text).lower() or 'bootsuk' in str(post.caption.text).lower():
            authorname = post.user.full_name if post.user.full_name else post.user.username
            take_screenshot(str(post.link), str(post.user.username) +
                            '_' + str(post.id), note='regular')
            followers = get_followers_count_ig(post.user.id, logg_details)
            try:
                eng = 100 * (post.like_count + post.comment_count) / followers
            except ZeroDivisionError:
                eng = 0.000
            if post.user.username not in followers_data['Instagram']:
                followers_data['Instagram'][post.user.username] = followers
            else:
                followers_data['Instagram'][post.user.username] += followers
            followers_data['Instagram'][post.user.username] = followers
            print('Instagram posts matches criteria')
            return {'media': 'Instagram', 'post_id': post.id, 'authorid': post.user.id, 'authortw': post.user.username, 'author': authorname, 'text': str(post.caption.text), 'created_at': str(post.created_time)[:16], 'likes': post.like_count, 'comments': post.comment_count, 'link': post.link, 'shares': 0, 'engagement': str(("%.2f" % eng)), 'followers': followers}

    return None


def collect_posts_insta(autho, logg_details, bloggers, followers_data, fromdate, searchQuery):
    try:
        tag_name = searchQuery.rstrip(' ')
        tags_media, next_ = autho.tag_recent_media(count=100, tag_name=tag_name)
    except:
        tag_name1 = searchQuery.lstrip('@').rstrip(' ')
        tag_name = tag_name1.lstrip('#').rstrip(' ')
        tags_media, next_ = autho.tag_recent_media(count=100, tag_name=tag_name)
    counter = 1
    from_ = datetime(fromdate[0], fromdate[1], fromdate[2])
    day_before_from = from_
    while next_ and counter < 70:
        more_media, next_ = autho.tag_recent_media(
            count=100, tag_name=searchQuery, with_next_url=next_)
        times_ = [datetime(int(str(post.created_time)[:10].split('-')[0]), int(str(post.created_time)
                                                                               [:10].split('-')[1]), int(str(post.created_time)[:10].split('-')[2])) for post in more_media]
        if [time for time in times_ if time >= day_before_from]:
            tags_media.extend(more_media)
            counter += 1
        else:
            counter = 71
    print('Instagram posts found:', len(tags_media))
    return tags_media


def process_post_twitter(tweet, author_name, bloggers, followers_data, startdate):

    followers = tweet.author.followers_count
    tweet_link = 'https://twitter.com/%s/status/%s' % (tweet.author.screen_name, tweet.id)
    retweeted = True if hasattr(tweet, 'retweeted_status') else False
    likes = tweet.retweeted_status.favorite_count if hasattr(
        tweet, 'retweeted_status') else tweet.favorite_count
    retweet = tweet.retweeted_status.retweet_count if hasattr(
        tweet, 'retweeted_status') else tweet.retweet_count
    replied = True if tweet.in_reply_to_screen_name != None and tweet.in_reply_to_status_id_str != None else False
    time_ = time_ = datetime(int(str(tweet.created_at)[:10].split(
        '-')[0]), int(str(tweet.created_at)[:10].split('-')[1]), int(str(tweet.created_at)[:10].split('-')[2]))
    from_ = datetime(startdate[0], startdate[1], startdate[2])
    try:
        eng = 100 * (int(likes) + int(retweet)) / followers
    except ZeroDivisionError:
        eng = 0.000
    tweet_dict = {'post_id': tweet.id, 'text': str(tweet.text),
                  'media': 'Twitter',
                  'comments': 0,
                  'retweeted': retweeted,
                  'likes': likes,
                  'authorid': tweet.author.id,
                  'authortw': tweet.author.screen_name,
                  'author': tweet.author.name,
                  'about_author': tweet.author.description,
                  'location': tweet.author.location,
                  'shares': retweet,
                  'created_at': str(tweet.created_at),
                  'replied': replied,
                  'in_reply_to_user_ID_str': str(tweet.in_reply_to_screen_name),
                  'in_reply_to_status_id': str(tweet.in_reply_to_status_id_str),
                  'link': str(tweet_link),
                  'followers': followers,
                  'engagement': str(("%.2f" % eng))}
    if time_ >= from_:
        take_screenshot(tweet_link, str(tweet.author.screen_name) + '_' + str(tweet.id), 'regular')
        if tweet.author.screen_name not in followers_data['Twitter']:
            followers_data['Twitter'][tweet.author.screen_name] = followers
        else:
            followers_data['Twitter'][tweet.author.screen_name] += followers
        followers_data['Twitter'][tweet.author.name] = followers
        print('Twitter posts matches criteria')
        return tweet_dict
    return None


def collect_posts_twitter(api, bloggers, followers_data, startdate, searchQuery, maxTweets, tweetsPerQry, max_id, sinceId):
    from_ = datetime(startdate[0], startdate[1], startdate[2])
    competition_posts = []
    tweetCount = 0
    Run = True
    while tweetCount < maxTweets and Run:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(
                        q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            max_id = new_tweets[-1].id
            for tweet in new_tweets:

                tweet_time = datetime(int(str(tweet.created_at)[:10].split(
                    '-')[0]), int(str(tweet.created_at)[:10].split('-')[1]), int(str(tweet.created_at)[:10].split('-')[2]))
                if tweet_time < from_:
                    Run = False
                else:
                    competition_posts.append(tweet)
            tweetCount += len(new_tweets)
        except tweepy.TweepError as e:
            print("some error : " + str(e))
            break
    print('Twitter posts found:', len(competition_posts))
    return competition_posts


def twitter_passwords_():
    passwords = []
    file = ([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open(
        '%s/Desktop/natappy/passwords/twitter_passwords.txt' % home, 'r') if ',' in line])
    for line in file:
        appaswords = {}
        appaswords['consumer_key'] = line[0]
        appaswords['consumer_secret'] = line[1]
        appaswords['token'] = line[2]
        appaswords['token_secret'] = line[3]
        appaswords['name'] = line[4]
        appaswords['username'] = line[5]
        appaswords['password'] = line[6]
        passwords.append(appaswords)
    return passwords

twitter_passwords = twitter_passwords_()


def analyse_competition(logg_details, platform, bloggers, followers_data, autho, query, startdate, maxTweets, tweetsPerQry, max_id, sinceId):
    if platform == 'Twitter':
        posts = collect_posts_twitter(autho, bloggers, followers_data, startdate=startdate, searchQuery=query,
                                      maxTweets=maxTweets, tweetsPerQry=tweetsPerQry, max_id=max_id, sinceId=sinceId)
    if platform == 'Instagram':
        posts = collect_posts_insta(autho, logg_details, bloggers,
                                    followers_data, startdate, searchQuery=query)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        result = list(executor.map(partial(process_post, logg_details=logg_details, platform=platform,
                                           bloggers=bloggers, followers_data=followers_data, startdate=startdate), posts))
    result_filtered = [x for x in filter(lambda x: x is not None, result)]
    return result_filtered


def competition(platform, bloggers, followers_data, startdate, searchQuery, maxTweets, tweetsPerQry, max_id, sinceId):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        result = list(executor.map(partial(process_query, bloggers=bloggers, followers_data=followers_data, startdate=startdate,
                                           maxTweets=maxTweets, tweetsPerQry=tweetsPerQry, max_id=max_id, sinceId=sinceId, platform=platform), searchQuery))
    return {post['link']: post for query_result in result for post in query_result}


def logg():
    return {'Twitter': cycle(twitter_passwords), 'Instagram': cycle(instagram_passwords)}

TEMP = logg()


def get_password(platform):
    with LOCK:
        password = next(TEMP[platform])
    return password


def autho_twitter(logg_details):
    auth = tweepy.AppAuthHandler(logg_details['consumer_key'], logg_details['consumer_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    if (not api):
        print("Can't Authenticate")
    return api


def autho_instagram(logg_details):
    autho = InstagramAPI(access_token=logg_details['token'], client_id=logg_details[
                         'client_id'], client_secret=logg_details['client_secret'])
    return autho


def process_query(query, bloggers, startdate, maxTweets, tweetsPerQry, max_id, sinceId, platform, followers_data):
    logg_details = get_password(platform)
    if platform == 'Twitter':
        autho = autho_twitter(logg_details)
    if platform == 'Instagram':
        autho = autho_instagram(logg_details)
    query_results = analyse_competition(logg_details, platform, bloggers, followers_data, autho, query,
                                        startdate=startdate, maxTweets=maxTweets, tweetsPerQry=tweetsPerQry, max_id=max_id, sinceId=sinceId)
    return [x for x in filter(lambda x: x is not None, query_results)]


def cut_screenshot_twitter(screenshot, note, url):
    img = Image.open(screenshot)
    print('Twitter image size:', img.size)
    img.crop((note[0], note[1], note[0] + note[2], note[1] + note[3])).save(screenshot)


def cut_screenshot_instagram(screenshot, note):
    img = Image.open(screenshot)
    if img.size[1] > 900:
        cutmore = img.size[1] - 900
    else:
        cutmore = 0
    img.crop((0, 77, img.size[0], img.size[1] - 120 - cutmore)).save("%s" % screenshot)
    time.sleep(2)


def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def cut_screenshot(screenshot, url, note, platform, dirname, name):
    try:
        if platform == 'Instagram':
            cut_screenshot_instagram(screenshot, note)
        if platform == 'Twitter':
            cut_screenshot_twitter(screenshot, note, url)
    except IndexError:
        phantom(url, name, note, dirname, platform)


def phantom(url, name, note, dirname, platform):
    try:
        browser = webdriver.PhantomJS()
        if platform == 'Twitter':
            browser.get(url)
            time.sleep(6)
            print('Collecting screenshots...', url)
            browser.set_window_size(1366, 1500)
            try:
                element = browser.find_element_by_css_selector(
                    'div.expansion-container.js-expansion-container')
                browser.save_screenshot('%s/Desktop/%s/%s_screenshots/%s.png' %
                                        (home, dirname, platform, name))
                size = element.size
                location = element.location
                note = [int(location['x']), int(location['y']),
                        int(size['width']), int(size['height'])]
                browser.quit()
                cut_screenshot('%s/Desktop/%s/%s_screenshots/%s.png' % (home, dirname, platform,
                                                                        name), url=url, note=note, platform=platform, dirname=dirname, name=name)

            except:
                print('Did not find selector.Will try once again, url:', url)
                browser.quit()
                phantom(platform, url, name, note, dirname)

        browser.get('%s' % url)
        time.sleep(3)
        browser.save_screenshot('%s/Desktop/%s/%s_screenshots/%s.png' %
                                (home, dirname, platform, name))
        browser.quit()
        cut_screenshot('%s/Desktop/%s/%s_screenshots/%s.png' % (home, dirname, platform,
                                                                name), url=url, note=note, platform=platform, dirname=dirname, name=name)
    except WebDriverException:
        print('Your interner speed sucks. Will wait until it gets better and try one again. ')
        time.sleep(5)
        phantom(url, name, note, dirname, platform)
    except urllib.error.URLError:
        print('Urllib error ignored. URL:', url)
        pass


def collect_screenshot(url_name, dirname):
    url = url_name[0]
    name = url_name[1]
    note = url_name[2]
    if 'facebook' in url:
        phantom(url, name, note, dirname, platform='Facebook')
    if 'instagram' in url:
        phantom(url, name, note, dirname, platform='Instagram')
    if 'twitter' in url:
        phantom(url, name, note, dirname, platform='Twitter')


def collect_screenshots(dirname):
    print('Collecting Competition Entries screenshots... Screenshots to collect:', len(links))
    tic = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=15) as executor:
        int in executor.map(partial(collect_screenshot, dirname=dirname), links)
    print('Screenshots collected. Elapsed:', time.time() - tic,
          'Average:', int(time.time() - tic) / len(links), ' per image.')

platshort = {'Facebook': 'FB', 'Instagram': 'IG', 'Twitter': 'TW'}


def competreport(platforms, tags, fromdate, bloggers, todate, repformat, brandname, campaign):
    all_media = {}
    followers_data = {'Twitter': {}, 'Instagram': {}, 'Facebook': {}}
    with suppress(Exception):
        os.remove('%s/Desktop/natappy/comp_urls.txt' % home)
    platshorts = '_'.join([platshort[platform] for platform in platforms])
    dirname = '%s-%s-%s' % (platshorts, '_'.join([tag for tag in tags]),
                            str(strftime("%Y_%m_%d_%H_%M", gmtime())))
    with suppress(Exception):
        os.makedirs('%s/Desktop/%s' % (home, dirname))
    if repformat == 'Full':
        for platform in platforms:
            with suppress(Exception):
                os.makedirs('%s/Desktop/%s/%s_screenshots' % (home, dirname, platform))
    for platform in [plat for plat in platforms if plat not in['Facebook']]:
        all_media[platform] = competition(platform, bloggers, followers_data, startdate=fromdate,
                                          searchQuery=tags, maxTweets=maxTweets, tweetsPerQry=tweetsPerQry, max_id=max_id, sinceId=sinceId)
    if 'Facebook' in platforms:
        with suppress(Exception):
            os.makedirs('%s/Desktop/%s/Facebook_screenshots' % (home, dirname))
        all_media['Facebook'] = fbcompet.collecting_reshares_everything(
            tags, dirname=dirname, followers_data=followers_data, fromdate=fromdate, todate=todate)
    pickle.dump(all_media, open('{home}/Desktop/all_media.pickle'.format(home=home), 'wb'))
    pickle.dump(dirname, open('{home}/Desktop/dirname.pickle'.format(home=home), 'wb'))
    pickle.dump(followers_data, open(
        '{home}/Desktop/followers_data.pickle'.format(home=home), 'wb'))

    followers_data = pickle.load(
        open('{home}/Desktop/followers_data.pickle'.format(home=home), 'rb'))
    dirname = pickle.load(open('{home}/Desktop/dirname.pickle'.format(home=home), 'rb'))
    all_media = pickle.load(open('{home}/Desktop/all_media.pickle'.format(home=home), 'rb'))

    # if repformat=='Full':

    #  collect_screenshots(dirname)
    compdf.excel(dirname, all_media, followers_data)
    compdf.pdf(all_media, dirname, bloggers, tags, fromdate, platforms,
               followers_data, brandname='SmashboxUK', campaign='BeLegendary')

if __name__ == '__main__':
    info = {'todate': [2016, 5, 11], 'blogposts': [], 'excludetags': ['Exclude tag'], 'blogpost': {}, 'replies': False, 'competition': ['Instagram'], 'format': 'Full', 'fromdate': [
        2016, 4, 10], 'tags': ['belegendary'], 'comptags': ['belegendary'], 'retweets': False, 'brandname': 'BeLegendary', 'campaign': 'SmashboxUK', 'bloggers': [], 'platforms': ['Instagram']}
  #  info= {'campaign': 'Fabulous in Dubai', 'format': 'Full', 'retweets': False, 'excludetags': [], 'fromdate': [2016, 1, 29], 'kind': 'competition', 'tags': ['fabulousindubai'], 'todate': [2016, 2, 5], 'replies': False, 'brandname': 'My Report',  'platforms': ['Instagram', 'Twitter'], 'bloggers': [], 'brand': {'Instagram': None, 'Twitter': None, 'Facebook': None, 'Name': None}}

    competreport(platforms=info['platforms'], tags=info['tags'], fromdate=info['fromdate'], bloggers=info[
                 'bloggers'], todate=info['todate'], repformat=info['format'], brandname=info['brandname'], campaign=info['campaign'])
