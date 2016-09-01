from functools import partial
from os.path import expanduser
from datetime import datetime
from itertools import cycle
from contextlib import suppress
import concurrent.futures, xlsxwriter, requests, time, tweepy,threading
import json

LOCK = threading.Lock()
home = expanduser("~")
#hfdfh

class Blogger():
     def __init__(self, name , facebook_username, instagram_username, twitter_username):
         self.twitter = twitter_username
         self.instagram = instagram_username
         self.facebook = facebook_username
         self.name = name
         
obama = Blogger('Obama','barackobama','barackobama','barackobama')


def request_more_media(next_, direction):  
    more_media = requests.get(next_).json() 
    if 'paging' in more_media and more_media['paging'] and direction in more_media['paging'] and more_media['paging'][direction]:
        more_data=more_media['data']
        more_next_=more_media['paging'][direction]        
        return more_data, more_next_
    if 'paging' in more_media and more_media['paging'] and not more_media['paging'][direction]:
        more_data=more_media['data']
        return more_data, None
    if 'paging' not in more_media and not more_media['data']:
        return [],None       


def browse_posts_in_direction(root, direction):
    counter=0
    collected = []
    while root and counter<30:
        answer=request_more_media(root, direction=direction)  
        collected.extend(answer[0])
        root = answer[1]
        counter+=1 
    return collected


def pagination_fb(blogger,logg_details,FACEBOOK_LIMIT = 20):
    if blogger == 'nothing':
        return [], 0    
    link = "https://graph.facebook.com/v2.5/%s?fields=likes,posts.limit(%s){link,message,shares,status_type,created_time,likes.summary(true),comments.summary(true)}&access_token=%s"%(blogger.facebook,FACEBOOK_LIMIT,logg_details['token'])         
    try:    
        first_media = requests.get(link).json()        
        next_, previous_, recent_media, followers = None, None, [], 0
        if 'posts' in first_media and first_media['posts']: 
            followers = first_media['likes']               
            recent_media = first_media['posts']['data']
            if 'paging' in first_media['posts']:
                next_ = first_media['posts']['paging'].get('next', None)
                previous_ = first_media['posts']['paging'].get('previous', None)  
        else:
            print ('blogger:', blogger, 'did not post anything yet')
            link = "https://graph.facebook.com/v2.5/%s?fields=likes&access_token=%s" %(blogger.facebook,logg_details['token'])
            return [],requests.get(link).json()['likes']            
        recent_media.extend(browse_posts_in_direction(root=next_, direction='next'))
        recent_media.extend(browse_posts_in_direction(root=previous_, direction='previous'))
        print ('Facebook', len(recent_media),'for', blogger,'checked')
        return recent_media, followers                 
    except KeyError:
        print ('blogger:', blogger,'has private profile. Can not provide data.')
    return [],0 



def get_followers_count_ig(blogger):
    try:
        url = 'http://instagram.com/' + blogger.instagram 
        media = requests.get(url).text
        where =  media.find('window._sharedData')
        half = (media[where+21:])
        where2 = half.find(';</script>')
        content = half[:where2]
        to_process = (json.loads(content)['entry_data']['ProfilePage'])
        return to_process[0]['user']['followed_by']['count']
    except Exception as e:
        print ('instagram followers count error:', e)
        return 0 
      
    


def user_recent_media(username,max_id):
    url = 'http://instagram.com/' + username.instagram + '/media' + ('?&max_id=' + max_id if max_id is not None else '')
    media = json.loads(requests.get(url).text)
    recent_media = media['items']
    if 'more_available' not in media or media['more_available'] is False:
        max_id = None
    else:
        max_id = media['items'][-1]['id']
    return recent_media, max_id        
        
        
    
def pagination_ig(blogger, INSTAGRAM_LIMIT = 10):
    recent_media, next_ = user_recent_media(blogger, None)
    counter = 0
    try:
        while next_ and counter< INSTAGRAM_LIMIT:  
            more_media, next_ = user_recent_media(blogger,next_)            
            recent_media.extend(more_media)
            counter+= 1
        return recent_media
    except:
        return []

 
       
def pagination_tw_inside(blogger,twapi,TWEETS_LIMIT = 2000):
    recent_media,followers = [], 0  
    for tweet in tweepy.Cursor(twapi.user_timeline, twapi, screen_name=blogger.twitter, count=200, include_rts=True).items(limit=TWEETS_LIMIT):         
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
    return recent_media, followers
 


def pagination_tw(blogger,twapi,TRIALS = 15):
    counter = 0
    while counter < TRIALS:
        try:
            return pagination_tw_inside(blogger,twapi)
        except:
              counter+=1
              time.sleep(15)
              return pagination_tw(blogger,twapi)
    return [],0



def instagram_passwords_():
    '''passwords should be list of dictionaries'''
    '''[{'consumer_key':,'consumer_secret':,'token':,'token_secret':,'name':,'username':,'password':}]'''
 
    passwords = []
    return passwords
    
instagram_passwords = instagram_passwords_()

 

def twitter_passwords_():
    '''passwords should be list of dictionaries '''
    '''[{'consumer_key':,'consumer_secret':,'token':,'token_secret':,'name':,'username':,'password':}]'''
 
    passwords = []
    return passwords
    
twitter_passwords = twitter_passwords_()

 
 
def facebook_passwords_():
    '''passwords should be list of dictionaries'''
    '''     [{'expires':,'token':,'name':'username','password'}]'''
    passwords = []

    return passwords
    
facebook_passwords = facebook_passwords_()



def logg():
   return {'Facebook': cycle(facebook_passwords),'Twitter': cycle(twitter_passwords),'Instagram':cycle(instagram_passwords)}


TEMP = logg()   
def get_password(platform):
    with LOCK:
        password = next(TEMP[platform])
    return password



def process_post_facebook(post): 
        likes, shares, comments, post_message = 0,0,0, ''
        with suppress(Exception):          
            likes=post['likes']['summary']['total_count']
        with suppress(Exception):
            shares=post['shares']['count']
        with suppress(Exception):
            comments=post['comments']['summary']['total_count']
        with suppress(Exception):
            post_message = post['message']
        link='https://www.facebook.com/%s' %post['id'] 
        return post['id'], {'text': post_message, 'shares': shares,'likes':likes,'created at': post['created_time'],'comments': comments,'link': link}



def process_post_instagram(post):
    time_=datetime.fromtimestamp(int(post['created_time']))
    post_message = '' 
    with suppress(Exception):  
        post_message = post['caption']['text'] 
    try:   
        return post['id'], {'text':post_message,'created at': str(time_),'likes':post['likes']['count'],'comments':post['comments']['count'],'link':post['link'],'shares': 0}
    except AttributeError:
        pass



def process_post_twitter(post,blogger):
    tweet_link='https://twitter.com/%s/status/%s' %(blogger,str(post['tweet_id']))                   
    return int(post['tweet_id']), {'text':post['text'],'likes': post['likes'],'shares': post['retweet'],'created at':str(post['created_at']),'in_reply_to_user_ID_str': post['in_reply_to_user_ID_str'],'in_reply_to_status_id': post['in_reply_to_status_id'],'link':tweet_link,'comments':0 }    



def process_post(post,blogger,platform): 
    if platform=='Facebook':
        return process_post_facebook(post)
    if platform=='Instagram':  
        return process_post_instagram(post)
    if platform=='Twitter': 
        return process_post_twitter(post,blogger)             



def process_blogger_facebook(blogger,logg_details):
      recent_media,followers=pagination_fb(blogger,logg_details)        
      return recent_media,followers



def process_blogger_instagram(blogger):
     followers=get_followers_count_ig(blogger)     
     recent_media=pagination_ig(blogger) 
     print ('266')
     return recent_media,followers
   
   
      
def process_blogger_twitter(blogger,logg_details):  
    auth = tweepy.AppAuthHandler(logg_details['consumer_key'], logg_details['consumer_secret'])
    autho = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)
    if (not autho):
        print ("Can't Authenticate")
    if autho.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']<10:
        raise Exception('You run out of rate limits. Application must close now. Please try again in 30 minutes.')        
    recent_media,followers=pagination_tw(blogger,autho)
    return recent_media,followers



def process_blogger(blogger,platform):
    print ('a')
    logg_details=get_password(platform)
    print ('log details', logg_details)
    if platform=='Instagram':
        blogger_posts_info=process_blogger_instagram(blogger)
  
    if platform=='Facebook': 
        blogger_posts_info=process_blogger_facebook(blogger,logg_details=logg_details)
    if platform=='Twitter':
        blogger_posts_info=process_blogger_twitter(blogger,logg_details=logg_details)
    print ('blogger_posts_info')
    recent_media, followers = blogger_posts_info

    if recent_media:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            result = list(executor.map(partial(process_post,blogger = blogger, platform=platform), recent_media))
            result_filtered = {k:v for k,v in filter(lambda x: x is not None, result)}               
            return blogger, result_filtered     



def get_posts(bloggers,platform):   
    executor_map = map
    if True:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
        executor_map = executor.map        
    results = executor_map(partial(process_blogger, platform=platform), bloggers)
    results_bloggers = {k:v for k,v in filter(lambda x: x is not None, results)}               
    print (results_bloggers)
    return results_bloggers




def excel_format(all_media): 
    post_in_excel_format=[]    
    for media in all_media.keys():
        for blogger in all_media[media].keys():  
            counter=1                 
            for post in all_media[media][blogger].keys():  
                post_details=[media,blogger.name,str(post),all_media[media][blogger][post]['link'],all_media[media][blogger][post]['created at'][:10],all_media[media][blogger][post]['created at'][10:],all_media[media][blogger][post]['text'],all_media[media][blogger][post]['likes'],all_media[media][blogger][post]['shares'],all_media[media][blogger][post]['comments'],all_media[media][blogger][post]['likes']+all_media[media][blogger][post]['shares']+all_media[media][blogger][post]['comments'],counter]
                post_in_excel_format.append(post_details)
                counter+=1
    return post_in_excel_format



def excel(all_media, report_path):  
    workbook = xlsxwriter.Workbook(report_path)
    worksheet = workbook.add_worksheet()
    fieldsnames= ('MEDIA','BLOGGER','POST_ID','POSTS_LINK','CREATED_DATE','CREATED_TIME','POSTS_TEXT','POSTS_LIKES','POSTS_SHARES','POSTS_COMMENTS','POST_INTERACTIONS')
    col = 0    
    for name in fieldsnames:
        worksheet.write(0, col,name)
        col += 1
    posts=excel_format(all_media)
    row=1   

    for post in posts:
        col=0              
        for name in post[:12]:
            worksheet.write(row,col,name)
            col+=1
        row+=1

    workbook.close()




def collect_posts(bloggers,platforms):
    all_media = {'Facebook':[],'Instagram':[],'Twitter':[]}
    for platform in platforms: 
        all_media[platform]=get_posts(bloggers,platform) 
    excel(all_media)





if __name__ == '__main__':
    collect_posts()










