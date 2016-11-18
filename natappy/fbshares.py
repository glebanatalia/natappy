from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import ui
from PIL import Image
import time
from contextlib import suppress
from os.path import expanduser
import xlsxwriter
home = expanduser("~")

from os.path import expanduser
import concurrent.futures
import threading
from itertools import cycle
import tweepy
home = expanduser("~")
LOCK = threading.Lock()
from itertools import cycle
import pandas


def screenname_to_linkname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b['blogger'] == blogger][media])[0]


def linkname_to_screenname(blogger, media):
    a = pandas.read_excel('%s/Desktop/natappy/bloggers.xlsx' % home)
    b = pandas.DataFrame(a)
    return list(b[b[media] == blogger]['blogger'])[0]


def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def collect_reshares(post_id, dirname, driver):
    print('Collecting shared posts...')
    driver.get('https://www.facebook.com/shares/view?id=' + str(post_id))
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
        if lastCount == lenOfPage:
            match = True
    source = str(driver.page_source)
    reshares = []
    firts_part = source.split(
        '</h5><div class=""><div class="_5pcp"><span><span class="fsm fwn fcg"><a class="_5pcq" href="/')
    for el in firts_part:
        try:
            if 'posts' in str(el.split('\"')[0]):
                reshares.append("https://www.facebook.com/" + str(el.split('\"')[0]))
            if 'permalink' in el.split('\"')[0] and 'target' in el.split('\"')[1]:
                reshares.append("https://www.facebook.com/" + str(el.split('\"')[0]))
        except:
            pass
    print('Reposts found:', len(reshares))
    if len(reshares) > 0:
        driver.save_screenshot('%s/Desktop/%s/Facebook_shares/%s.png' % (home, dirname, post_id))
        time.sleep(3)
        img = Image.open('%s/Desktop/%s/Facebook_shares/%s.png' % (home, dirname, post_id))
        img.crop((374, 53, img.size[0] - 486, img.size[1])
                 ).save('%s/Desktop/%s/Facebook_shares/%s.png' % (home, dirname, post_id))
    return reshares


def collect_reshare_results(url, driver):
    try:
        post_id = url.split('posts/')[1]
    except:
        pass
    if 'permalink' in url and 'groups' not in url:
        post_id = url.split('id=')[2]
        url = url.replace('amp;', '')
    if 'groups' in url:
        post_id = url.split('permalink/')[1].rstrip('/')
    driver.get(url)
    source = str(driver.page_source)
    likes, comments, shares = 0, 0, 0
    likes = int(source.split('likecount\":')[1].rsplit(',\"')[0])
    comments = int(source.split('commentcount')[1][2:].rsplit(',\"')[0])
    shares = int(source.split('sharecount')[1][2:].rsplit(',\"')[0])
    return post_id, likes, comments, shares


def count_page_likes(url, driver):
    author, audience = 'not known', 0
    if 'permalink' in url:
        url = url.replace('amp;', '')
        author_id = url.split('id=')[2]
        facebook_profile = 'href="https://www.facebook.com/profile.php?id=%s&amp;sk=likes"' % (
            author_id)
        driver.get('https://www.facebook.com/profile.php?id=%s' % author_id)
    if 'permalink' not in url:
        facebook_profile = 'href="%s"' % (url.split('posts')[0] + 'likes')
        driver.get(url.split('posts')[0].rstrip('/'))
    source = driver.page_source
    author = source.split('pageTitle">')[1].split('<')[0]
    try:
        mightbeaudience = source.split(facebook_profile)
    except:
        return author, 0
    for el in mightbeaudience:
        if ' people like this</div>' in el:
            try:
                audience = int(el.split(' people like this</div>')
                               [0].split('">')[2].replace(',', ''))
            except:
                pass
    return author, audience


def count_followers(url, driver):
    audience = 0
    author = 'not known'
    if 'permalink' in url:
        url = url.replace('amp;', '')
        author_id = url.split('id=')[2]
        facebook_profile = 'href="https://www.facebook.com/profile.php?id=%s&amp;sk=followers"' % (
            author_id)
        driver.get('https://www.facebook.com/profile.php?id=%s' % author_id)
    if 'permalink' not in url:
        facebook_profile = 'href="%s"' % (url.split('posts')[0] + 'followers')
        driver.get(url.split('posts')[0].rstrip('/'))
    source = driver.page_source
    author = source.split('pageTitle">')[1].split('<')[0]
    try:
        mightbeaudience = source.split(facebook_profile)
    except:
        return author, 0
    for el in mightbeaudience:
        if ' people</a>' in el:
            try:
                audience = int(el.split(' people</a></div><span')[0].lstrip('>').replace(',', ''))
            except:
                pass
    return author, audience


def count_friends(url, driver):
    audience = 0
    author = 'not known'
    if 'permalink' in url:
        url = url.replace('amp;', '')
        author_id = url.split('id=')[2]
        facebook_profile = 'href="https://www.facebook.com/profile.php?id=%s&amp;sk=friends"' % (
            author_id)
        driver.get('https://www.facebook.com/profile.php?id=%s' % author_id)
    if 'permalink' not in url:
        facebook_profile = 'href="%s"' % (url.split('posts')[0] + 'friends')
        driver.get(url.split('posts')[0].rstrip('/'))
    source = driver.page_source
    author = source.split('pageTitle">')[1].split('<')[0]
    try:
        mightbeaudience = source.split(facebook_profile)
    except:
        return author, 0
    for el in mightbeaudience:
        if '</a></span></div></div></div></div></div><div' in el:
            try:
                audience = int(el.split('</a></span></div></div></div></div></div><div')
                               [0].lstrip('>').replace(',', ''))
            except:
                pass
    return author, audience


def count_friends_or_followers(url, driver):
    author1, friends = count_friends(url, driver)
    author2, likes = count_page_likes(url, driver)
    author3, followers = count_followers(url, driver)
    authors = [someone for someone in [author1, author2, author3] if someone not in ['not known']]
    author = authors[0] if authors else 'not known'
    impression = friends + likes + followers
    if author:
        if ') ' in author:
            author = author.split(') ')[1]
        return author, impression
    else:
        return 'not known', impression


def define_reshare_type(url, driver):
    if 'groups' in url:
        reshare_type = 'ShareToGroup'
    if 'permalink' in url and 'groups' not in url:
        reshare_type = 'WeirdShare'
    if 'posts' in url:
        reshare_type = 'RegularShare'
    return reshare_type


def count_group_members(url, driver):
    driver.get(url.split('posts')[0].rstrip('/'))
    source = driver.page_source
    author = source.split('pageTitle">')[1].split('<')[0]
    audience = source.split('id="count_text">')[1].split(' members')[0].replace(',', '')
    if 'data-tab-key' in audience:
        audience = 0
    if ')' in author:
        author = author.split(') ')[1]
    return author, int(audience)


def collect_people_who_reshare_results(url, driver):
    audience = 0
    main_author = 'not known'
    reshare_type = define_reshare_type(url, driver)
    if reshare_type == 'ShareToGroup':
        with suppress(Exception):
            main_author, audience = count_group_members(url, driver)
    else:
        main_author, audience = count_friends_or_followers(url, driver)
    return main_author, audience


def collecting_reshares_everything(post_id, dirname):
    driver = webdriver.PhantomJS()
    driver.get("https://www.facebook.com")
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_is_loaded)
    email_field = driver.find_element_by_id("email")
    email_field.send_keys("nglebawar@gmail.com")
    password_field = driver.find_element_by_id("pass")
    password_field.send_keys("white2015")
    password_field.send_keys(Keys.RETURN)
    reshares = collect_reshares(post_id, dirname, driver)
    reshares_collection = {}
    for el in reshares:
        resharer, audience = (collect_people_who_reshare_results(el, driver))
        post_id, likes, comments, shares = (collect_reshare_results(el, driver))
        reshares_collection[post_id] = {}
        reshares_collection[post_id] = {'link': el, 'likes': likes, 'comments': comments,
                                        'shares': shares, 'author': resharer, 'impression': int(audience)}
    return reshares_collection


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


def logg():
    return {'Twitter': cycle(twitter_passwords)}

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


def collect_retweets(retweeted):
    all_retweets = {}
    executor_map = map
    if True:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
        executor_map = executor.map
    for blogger in retweeted.keys():
        results = list(executor_map(processing_retweets, retweeted[blogger]))
        all_retweets[blogger] = {k: v for k, v in results}
    return all_retweets


def processing_retweets(tweet):
    logg_details = get_password('Twitter')
    autho = autho_twitter(logg_details)
    print('Processing retweet:', tweet)
    retweets = autho.retweets(tweet)
    tweet_retweets = {}
    for retweet in retweets:
        author = retweet.author.name
        print('Author', author)
        authortw = retweet.author.screen_name
        followers = retweet.author.followers_count
        print('Audience:', followers)
        likes = retweet.retweeted_status.favorite_count
        retweets_count = retweet.retweeted_status.retweet_count
        tweet_link = 'https://twitter.com/%s/status/%s' % (authortw, retweet.id)
        tweet_dict = {'tweet_id': retweet.id, 'text': str(retweet.text),
                      'likes': likes,
                      'shares': retweets_count,
                      'created_at': str(retweet.created_at),
                      'link': str(tweet_link), 'author': author, 'impression': followers, 'comments': 0}
        tweet_retweets[retweet.id] = tweet_dict
    return tweet, tweet_retweets


def nice_reshares_excel(reshares_collection, dirname):
    nice_format = excel_format(reshares_collection)
    excel(nice_format, dirname)


def excel_format(reshares_collection):
    post_in_excel_format = []

    for media in reshares_collection.keys():
        if reshares_collection[media]:
            for blogger in reshares_collection[media].keys():
                for post in reshares_collection[media][blogger].keys():
                    counter = 1
                    for share in reshares_collection[media][blogger][post].keys():
                        link1 = 'www.facebook.com/%s' % (
                            post) if media == 'Facebook' else 'www.twitter.com/statuses/%s' % (post)
                        share_details = [blogger, media, str(post), link1, reshares_collection[media][blogger][post][share]['author'], reshares_collection[media][blogger][post][share]['link'], reshares_collection[media][blogger][
                            post][share]['likes'], reshares_collection[media][blogger][post][share]['comments'], reshares_collection[media][blogger][post][share]['shares'], reshares_collection[media][blogger][post][share]['impression']]
                        post_in_excel_format.append(share_details)
                        counter += 1
    return post_in_excel_format


def excel(nice_format, dirname):
    print('Creating excel for reposts...')
    workbook = xlsxwriter.Workbook('%s/Desktop/%s/SharesReport.xlsx' % (home, dirname))
    worksheet = workbook.add_worksheet()
    fieldsnames = ('BLOGGER', 'MEDIA', 'POST ID', 'ORIGINAL LINK', 'AUTHOR',
                   'SHARED LINK', 'LIKES', 'COMMENTS', 'SHARES', 'IMPRESSION')
    col = 0
    for name in fieldsnames:
        worksheet.write(0, col, name)
        col += 1
    row = 1

    for post in nice_format:
        col = 0
        for name in post:

            worksheet.write(row, col, name)
            col += 1
        row += 1
    workbook.close()


# class="_39g5" href="https://www.facebook.com/Ghgfghffdgghu/friends">
