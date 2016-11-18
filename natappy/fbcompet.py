from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import ui
from PIL import Image
import time
from contextlib import suppress
from os.path import expanduser
import datetime
import concurrent.futures
from functools import partial
import requests
from itertools import cycle
import concurrent.futures
import xlsxwriter
import requests
import textwrap
import os
import time
import tweepy
import threading
home = expanduser("~")
LOCK = threading.Lock()
from math import floor
import pandas

postscount_data = {'Facebook': {}}


def screenname_to_linkname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b['blogger'] == blogger][media])[0]


def linkname_to_screenname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b[media] == blogger]['blogger'])[0]


def facebook_passwords_():
    passwords = []
    file = ([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open(
        '%s/Desktop/natappy/passwords/facebook_passwords.txt' % home, 'r') if ',' in line])
    for line in file:
        appaswords = {}
        appaswords['expires'] = line[0]
        appaswords['token'] = line[1]
        appaswords['name'] = line[2]
        appaswords['username'] = line[3]
        appaswords['password'] = line[4]
        passwords.append(appaswords)
    return passwords

facebook_passwords = facebook_passwords_()


def logg():
    return {'Facebook': cycle(facebook_passwords)}

TEMP = logg()


def get_password(platform):
    with LOCK:
        password = next(TEMP[platform])
    return password


def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def month_to_number(month):
    return int({'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': 10, 'November': 11, 'December': 12}[month])


def converted_date(date):
    day = int(date.split(' ')[0])
    month = month_to_number(date.split(' ')[1])
    year = int(date.split(' ')[2])
    return datetime.datetime(year, month, day)


def collect_reshares(dirname, driver, hashtag):
    print('Collecting competition posts...')
    # driver.get('https://www.facebook.com/shares/view?id='+str(post_id))
    driver.get('https://www.facebook.com/hashtag/%s' % hashtag)
    driver.maximize_window()
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(3)
        wait = ui.WebDriverWait(driver, 10)
        wait.until(page_is_loaded)
        if lastCount == lenOfPage:
            match = True
    driver.save_screenshot('%s/Desktop/%s/Facebook_screenshots/allposts.png' % (home, dirname))
    source = str(driver.page_source)
    reshares = []
    firts_part = source.split(
        '</h5><div class=""><div class="_5pcp"><span><span class="fsm fwn fcg"><a class="_5pcq" href="')
    for el in firts_part:
        try:
            if 'posts' in str(el.split('\"')[0]):
                reshares.append("https://www.facebook.com" + str(el.split('\"')[0]))
            if 'permalink' in el.split('\"')[0] and 'target' in el.split('\"')[1]:
                reshares.append("https://www.facebook.com" + str(el.split('\"')[0]))
            if 'photos' in str(el.split('\"')[0]):
                reshares.append("https://www.facebook.com" + str(el.split('\"')[0]))
            if 'videos' in str(el.split('\"')[0]):
                reshares.append("https://www.facebook.com" + str(el.split('\"')[0]))
            if 'photo' in str(el.split('\"')[0]) and not 'photos' in str(el.split('\"')[0]):
                reshares.append(str(el.split('\"')[0]).replace('amp;', ''))

        except:
            pass
    print('competition posts found:', len(reshares))
    return reshares


def collect_reshare_results(url, dirname):
    author = 'anonymous'
    driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome('/Users/War7/Desktop/chromedriver')
  #  driver.get("https://www.facebook.com")
    try:
        post_id = url.split('posts/')[1]
    except:
        pass
    if 'photo' in url and not 'photos' in url:
        post_id = url.split('fbid=')[1].split('&set')[0]
        url = 'https://www.facebook.com/' + str(post_id)
    if 'permalink' in url and 'groups' not in url:
        post_id = url.split('id=')[2]
        url = url.replace('amp;', '')
    if 'groups' in url:
        post_id = url.split('permalink/')[1].rstrip('/')
    if 'photos' in url:
        post_id = url.split('/')[6]
        url = url.split('photos')[0] + 'posts/' + str(post_id)
    if 'videos' in url:
        post_id = url.split('videos/')[1].rstrip('/')
        url = 'https://www.facebook.com/' + str(post_id)

    driver.get(url)
    time.sleep(8)

    driver.save_screenshot('%s/Desktop/%s/Facebook_screenshots/%s.png' % (home, dirname, post_id))
    time.sleep(3)
    try:
        img = Image.open('%s/Desktop/%s/Facebook_screenshots/%s.png' % (home, dirname, post_id))
        img.crop((195, 133, img.size[0] - 300, img.size[1])
                 ).save('%s/Desktop/%s/Facebook_screenshots/%s.png' % (home, dirname, post_id))
    except:
        pass
    source = str(driver.page_source)
    likes, comments, shares = 0, 0, 0
  #  with suppress(Exception):
    try:
        createddate = source.split('<abbr title="')[1].split(' at ')[0]. split(', ')[1]
        createtime = source.split('<abbr title="')[1].split(' at ')[1].split('\"')[0]
        author_id = source.split('"actorid":"')[1].split('\"')[0]
    except:
        email_field = driver.find_element_by_id("email")
        email_field.send_keys("nglebawar@gmail.com")
        time.sleep(15)
        password_field = driver.find_element_by_id("pass")
        time.sleep(3)
        password_field.send_keys("white2015")
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.get(url)
        time.sleep(6)
        driver.save_screenshot('%s/Desktop/%s/Facebook_screenshots/%s.png' %
                               (home, dirname, post_id))
        time.sleep(2)
        try:
            img = Image.open('%s/Desktop/%s/Facebook_screenshots/%s.png' % (home, dirname, post_id))
            img.crop((195, 133, img.size[0] - 300, img.size[1])).save(
                '%s/Desktop/%s/Facebook_screenshots/%s.png' % (home, dirname, post_id))
        except:
            pass
        source = driver.page_source
    createddate = source.split('<abbr title="')[1].split(' at ')[0]. split(', ')[1]
    createtime = source.split('<abbr title="')[1].split(' at ')[1].split('\"')[0]
    author_id = source.split('"actorid":"')[1].split('\"')[0]
    with suppress(Exception):
        likes = int(source.split('likecount\":')[1].rsplit(',\"')[0])
    with suppress(Exception):
        comments = int(source.split('commentcount')[1][2:].rsplit(',\"')[0])
    with suppress(Exception):
        shares = int(source.split('sharecount')[1][2:].rsplit(',\"')[0])
    with suppress(Exception):
        author = source.split('\"ownerName\":"')[1].split('\"')[0]
    if author:
        if ') ' in author:
            author = author.split(') ')[1]
        if '-' in author:
            author = author.split('-')[1]
    driver.quit()
    try:
        authortw = source.split(
            'class="_5pb8 _29h _303" href="https://www.facebook.com/')[1].split('?')[0]
    except:
        authortw = author
    return author, authortw, author_id, post_id, likes, comments, shares, createddate, createtime


def count_followers(url, author_id):
    driver = webdriver.PhantomJS()
    email_field = driver.find_element_by_id("email")
    email_field.send_keys("nglebawar@gmail.com")
    time.sleep(15)
    password_field = driver.find_element_by_id("pass")
    time.sleep(3)
    password_field.send_keys("white2015")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.get(url)
    time.sleep(6)
    driver.save_screenshot('%s/Desktop/%s.png' % (home, author_id))
    time.sleep(2)
    audience = 0
    if 'permalink' in url:
        facebook_profile = 'href="https://www.facebook.com/profile.php?id=%s&amp;sk=followers"' % (
            author_id)
    if 'permalink' not in url and 'photos' not in url:
        facebook_profile = 'href="%s"' % (url.split('posts')[0] + 'followers')
    if 'photos' in url:
        facebook_profile = 'href="%s"' % (url.split('photos')[0] + 'followers')
      #  driver.get(url.split('photos')[0].rstrip('/'))
    if 'videos' in url:
        facebook_profile = 'href="%s"' % (url.split('videos')[0] + 'followers')
       # driver.get(url.split('videos')[0].rstrip('/'))
    driver.get('https://www.facebook.com/%s' % author_id)
    driver.save_screenshot('%s/Desktop/%s.png' % (home, url))
    source = driver.page_source
    if 'photo' in url and not 'photos' in url:
        facebook_profile = source.split('"page_uri":"')[1].split(
            '\"')[0].replace('\\', '') + '/' + 'followers'
    try:
        mightbeaudience = source.split(facebook_profile)
    except:
        return 0
    for el in mightbeaudience:
        if ' people</a>' in el:
            try:
                audience = int(el.split(' people</a></div><span')[0].lstrip('\">').replace(',', ''))
            except:
                pass
    return audience


def count_friends(url, author_id):
    driver = webdriver.PhantomJS()
#    driver = webdriver.Chrome('/Users/War7/Desktop/chromedriver')
    email_field = driver.find_element_by_id("email")
    email_field.send_keys("nglebawar@gmail.com")
    time.sleep(5)
    password_field = driver.find_element_by_id("pass")
    time.sleep(3)
    password_field.send_keys("white2015")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    # audience=0
    if 'permalink' in url:
        facebook_profile = 'href="https://www.facebook.com/profile.php?id=%s&amp;sk=friends"' % (
            author_id)
    if 'permalink' not in url and 'photos' not in url:
        facebook_profile = 'href="%s"' % (url.split('posts')[0] + 'friends')
    if 'photos' in url:
        facebook_profile = 'href="%s"' % (url.split('photos')[0] + 'friends')
    if 'videos' in url:
        facebook_profile = 'href="%s"' % (url.split('videos')[0] + 'friends')
    driver.get('https://www.facebook.com/%s' % author_id)
    time.sleep(3)
    source = driver.page_source
#    driver.save_screenshot('/Users/War7/Desktop/%s.png' %(author_id))
    if 'photo' in url and not 'photos' in url:
        facebook_profile = source.split('"page_uri":"')[1].split('\"')[
            0].replace('\\', '') + '/' + 'friends'
    # try:
    mightbeaudience = source.split(facebook_profile)
    # except:
    #   return 0
    for el in mightbeaudience:
        if '</a></span></div></div></div></div></div><div' in el:
            try:
                audience = int(el.split('</a></span></div></div></div></div></div><div')
                               [0].lstrip('>').replace(',', ''))
            except:
                pass
    driver.quit()
    return audience


def count_friends_or_followers(url, author_id):

    try:
        followers = int(count_followers(url, author_id))
    except:
        followers = 0
    try:
        friends = int(count_friends(url, author_id))
    except:
        friends = 0
    # author2,likes=count_page_likes(url,driver)
    try:
        impression = friends + followers
    except:
        impression = 0
    return impression


def define_reshare_type(url):
    if 'groups' in url:
        reshare_type = 'ShareToGroup'
    if 'permalink' in url and 'groups' not in url:
        reshare_type = 'WeirdShare'
    if 'posts' in url:
        reshare_type = 'RegularShare'
    if 'photos' in url:
        reshare_type = 'PhotoAdded'
    if 'videos' in url:
        reshare_type = 'VideoAdded'
    if 'photo' in url and not 'photos' in url:
        reshare_type = 'WeirdPhoto'
    return reshare_type


def count_group_members(url, driver):
    driver = webdriver.PhantomJS()
    author = 'not known'
    audience = 0
    driver.get(url.split('posts')[0].rstrip('/'))
    source = driver.page_source
    author = source.split('pageTitle">')[1].split('<')[0]
    audience = source.split('id="count_text">')[1].split(' members')[0].replace(',', '')
    if 'data-tab-key' in audience:
        audience = 0
    if ')' in author:
        author = author.split(') ')[1]
    return int(audience)


def collect_people_who_reshare_results(author_id, url, followers_data, dirname, fromdate, todate, el):
    logg_details = get_password('Facebook')
    try:
        link = "https://graph.facebook.com/v2.5/%s?fields=likes,name&access_token=%s" % (
            author_id, logg_details['token'])
        json = requests.get(link).json()
        if 'name' in json and 'likes' in json:
            return json['name'], json['likes']
        else:
            reshare_type = define_reshare_type(url)
            if reshare_type == 'ShareToGroup':
                with suppress(Exception):
                    main_author, audience = count_group_members(url)
            else:
                audience = count_friends_or_followers(url, author_id)
        return 'not known', audience
    except:
        return 'not known', 0


def collecting_reshares_everything(tags, dirname, followers_data, fromdate, todate):
    driver = webdriver.PhantomJS()
    driver.get("https://www.facebook.com")
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_is_loaded)
    email_field = driver.find_element_by_id("email")
    email_field.send_keys("nglebawar@gmail.com")
    password_field = driver.find_element_by_id("pass")
    password_field.send_keys("white2015")
    password_field.send_keys(Keys.RETURN)
    for tag in tags:
        tag = tag.lstrip('#').lstrip('@')
        reshares = collect_reshares(dirname, driver, tag)
    driver.quit()
    tic = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        result = list(executor.map(partial(process_tag_post, dirname=dirname,
                                           followers_data=followers_data, fromdate=fromdate, todate=todate), reshares))
    print('elapsed:', time.time() - tic)
    return {post['link']: post for post in result if post}


def process_tag_post(el, followers_data, dirname, fromdate, todate):
    author, authortw, author_id, post_id, likes, comments, shares, createddate, createdtime = (
        collect_reshare_results(el, dirname))
    audience = (collect_people_who_reshare_results(author_id, el,
                                                   followers_data, dirname, fromdate, todate, el))[1]

    if audience != 0 and author not in postscount_data['Facebook']:
        postscount_data['Facebook'][author] = 1
    if audience != 0 and author in postscount_data['Facebook']:
        postscount_data['Facebook'][author] += 1

    if author not in followers_data['Facebook']:
        followers_data['Facebook'][author] = audience
    else:
        if audience == 0:
            try:
                audience = floor(followers_data['Facebook'][author] /
                                 postscount_data['Facebook'][author])
            except:
                audience = 0
            followers_data['Facebook'][author] += audience
        else:
            followers_data['Facebook'][author] += audience
    try:
        eng = 100 * (int(likes) + int(comments) + int(shares)) / audience
    except ZeroDivisionError:
        eng = 0.000
    if datetime.datetime(todate[0], todate[1], todate[2]) >= converted_date(createddate) >= datetime.datetime(fromdate[0], fromdate[1], fromdate[2]):
        return {'engagement': str(("%.2f" % eng)), 'media': 'Facebook', 'text': '   ', 'created_at': createddate, 'post_id': post_id, 'link': el, 'likes': likes, 'comments': comments, 'shares': shares, 'author': author, 'authortw': authortw, 'followers': int(audience)}
    return None


# https://www.packtpub.com/packt/offers/free-learning
