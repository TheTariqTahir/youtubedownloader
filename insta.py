import datetime
import requests

from instagrapi import Client

import json

def get_session(user_name,password):
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.datetime.now().timestamp())
    response = requests.get(link)
    csrf = response.cookies['csrftoken']

    

    payload = {
        'username': user_name,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)

    if json_data["authenticated"]:

        print("login successful")
        cookies = login_response.cookies
        cookie_jar = cookies.get_dict()
        csrf_token = cookie_jar['csrftoken']
        print("csrf_token: ", csrf_token)
        session_id = cookie_jar['sessionid']
        print("session_id: ", session_id)
        
        return session_id
    
    else:
        print("login failed ", login_response.text)
    
    
    
    
    
session_id='54094635318%3A00jQYlHfhDiISf%3A25%3AAYc5a3pyMWd1SufhhkE48oz-pvhL2GuriKsUEOqUHw'


user_name = 'mr_meemer.69'
password = 'rspmrmeemer6969'
    
# # session_id = get_session(user_name,password)
# cl = Client()
# # # cl.login_by_sessionid(session_id)
# cl.login(username=user_name,password=password)
# print(cl.user_following(user_name))

# from instabot import Bot

# bot = Bot()
# bot.login(username=user_name,password=password)

# print(bot.get_user_followers(user_name))

import requests
import json
from time import sleep
import random
import sys

#all our URLs
url = 'https://www.instagram.com'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
followers_url = 'https://www.instagram.com/graphql/query/'
output_file = 'snakes.txt'

session = requests.Session()
query_hash_followers = 'c76146de99bb02f6415203be841dd25a' #some sort of md5 hash used for follower lookup (seems cosntant)
query_hash_following = 'd04b0a864b4b54837c0d870b0e77e076' #same thing, just for the "following" queries

#queries followers, and people we follow
def runQuery(login, followers):
    if not login['success']:
        print('Could not log in, check to see if credentials are valid. Or disable 2-step authentication.')
        sys.exit(0)
    
    # this is the query that browers seem to be using to fetch followers
    # we can maybe fetch # of followers and just set 'first' to that
    query = { 
        'id' : login['userId'],
        'include_reel': False,
        'fetch_mutual': False,
        'first': random.randint(100, 200) #does my query_hash only work with 24? we'll find out, UPDATE: guess not
    }

    #results
    result = []

    #search parameter
    hasNextPage = True
    offset = ''
    edge_type = 'edge_followed_by' if followers else 'edge_follow'

    while hasNextPage:
        #sleep, so we dont' seem like a machine
        sleep(random.uniform(0, 2)) 

        #insert offset
        if len(offset) > 0:
            query['after'] = offset

        response = session.get(followers_url, params={
            'query_hash': query_hash_followers if followers else query_hash_following,
            'variables': json.dumps(query)
        })

        response_data = json.loads(response.text)

        for node in response_data['data']['user'][edge_type]['edges']:
            result.append(node['node']['username'])

        hasNextPage = response_data['data']['user'][edge_type]['page_info']['has_next_page']
        offset  = response_data['data']['user'][edge_type]['page_info']['end_cursor']
    
    result.sort()

    # with open('followers.txt' if followers else 'following.txt', 'w+') as ff:
    #     ff.write("\n".join(result))

    return result

def findSnakes(following, followers):
    i1 = 0
    i2 = 0
    snakes = []
    #A simple O(n) algorithm
    #Below is how it works

    # () -> snake
    # I follow:  [a, (b), d, (e), f]
    # Follow me: [a, c, d, f]

    while i1 < len(following):
        #if we follow each other
        if following[i1] == followers[i2]:
            i1 += 1
            i2 += 1
        #found a snake
        elif following[i1] < followers[i2]:
            snakes.append(following[i1])
            i1 += 1
        else: i2 += 1
    
    with open(output_file, 'w+') as res:
        res.write('-------SNAKES (%d total) -------\n' % (len(snakes)))
        res.write('\n'.join(snakes))

def login():
    #make it look like we're logging in from Chrome
    session.headers.update({
        'Connection': 'keep-alive',
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    })

    # apparently this is important?
    session.cookies.update({
        'ig_pr': '1',
        'ig_vw': '1920',
    })

    #extact csrf token
    response = session.get(url)
    csrf_token = response.cookies['csrftoken']
    
    login = {}

    #add it to the session
    session.headers.update({ 'X-CSRFToken': csrf_token })

    #load credentials from JSON file
    try:
        with open('login.json', 'r') as credentials:
            login = json.loads(credentials.read())
    except Exception:
        print('Looks like you don\'t have a "login.json" - create one now & re-start')
        sys.exit(0)

    #sleep a random amount of time so they'll think we're a human
    sleep(random.randint(3, 7))

    response = session.post(login_url, data=login, allow_redirects=True)
    
    #let's hope it works bois
    great_success = json.loads(response.text)
    
    #update csrftoken once again
    csrf_token = response.cookies['csrftoken']

    #get the user id, we'll need this to get our followers
    userId = great_success['userId']
    session.headers.update({ 'X-CSRFToken': csrf_token })

    #kind of important we have this
    assert userId is not None
    
    return {
        'success' : great_success['authenticated'],
        'userId': userId
    }

#try to log in
logged_in = login()

print('Scanning...')
#run 2 queries
followers = runQuery(logged_in, True)
following = runQuery(logged_in, False)

#run analysis
findSnakes(following, followers)
print('Done! Please check', output_file)