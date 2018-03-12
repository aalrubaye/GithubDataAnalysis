from pymongo import MongoClient
import pprint
import urllib2
import simplejson
from datetime import datetime, timedelta
import time


__author__ = 'Abdul Rubaye'


# list of any database collections
# ["commit_comments", "commits", "events", "followers", "forks", "geo_cache", "issue_comments", "issue_events",
# 	"issues", "org_members", "pull_requests", "pull_requst_comments", "repo_collaborators", "repo_labels",
# 	"repos", "topics", "users", "watchers" ]

client = MongoClient()
database = client.github_16
events = database.events
events_forks = database.events_forks
final_collection = database.final_collection

# client id and client secret are used in calling the github API
# they will help to raise the maximum limit of calls per hour
# note: you will need your private txt file that includes the private keys
privateVar = open("privateVar.txt",'r').read()
client_id = privateVar.split('\n', 1)[0]
client_secret = privateVar.split('\n', 1)[1]


def print_first_elem():
    for elem in events.find():
        pprint.pprint(elem)
        break
    print events.count()


def print_in_range(offset, position):
    for elem in events.find()[offset:position]:
        pprint.pprint(elem)
        # print elem['watchers_count']
        print_separator()


def print_with_condition(field, value):
    for elem in events.find():
        if elem[field] == value:
            pprint.pprint(elem)


# prints dashes as separator, only to beautify the prints
def print_separator():
    print ('-'*100)

# fetches the user object from a url and calls the followers list creator
def fetch_actor_followers(url):
    followers_list = []
    new_url = add_client_id_client_secret_to_url(url)
    try:
        response = urllib2.urlopen(new_url)
        data = simplejson.load(response)
        for follower in data:
            followers_list.append(follower['login'])
        return followers_list
    except urllib2.URLError, e:
        return None

def fetch_repo_information(url):
    new_url = add_client_id_client_secret_to_url(url)
    try:
        response = urllib2.urlopen(new_url)
        data = simplejson.load(response)
        return data
    except urllib2.URLError, e:
        return None

# appends the client id and the client secret to urls
def add_client_id_client_secret_to_url(url):
    return url+'?client_id='+client_id+'&client_secret='+client_secret

# separate ForkEvents and insert them in a collection
def feed_events_forks_collection():
    index = 1
    for elem in events.find():
        if elem['type'] == 'ForkEvent':
            events_forks.insert(elem)
            index = index + 1
            print index


# to create a separate database out of the downloaded github bson file only for our work
def create_database_from_forks_events(offset,position):
    index = offset
    for event in events_forks.find()[offset:position]:
        repo = fetch_repo_information(event['repo']['url'])
        followers_list = fetch_actor_followers(event['payload']['forkee']['owner']['followers_url'])
        if (repo is not None) & (followers_list is not None):
            entry = {
                "id": event['id'],
                "created_at": event['created_at'],
                "actor": event['actor']['login'],
                "followers": followers_list,
                "repo_name": repo['name'],
                "repo_created_at": repo['created_at'],
                "repo_language": repo['language'],
                "repo_size": repo['size'],
                "repo_stargazers": repo['stargazers_count'],
                "repo_watchers": repo['watchers_count'],
                "repo_forks_count": repo['forks_count'],
                "repo_network_count": repo['network_count'],
                "repo_subscribers_count": repo['subscribers_count'],
                "followers_url": event['payload']['forkee']['owner']['followers_url'],
                "repo_url": event['repo']['url']
            }
            final_collection.insert(entry)
        index += 1
        print index


# below is the area where I call the functions

# 1 - we need to separate the forks events for more convenient
# feed_events_forks_collection()

# 2- create a mongodb collection for the elements we want
# create_database_from_forks_events(13200,15600)
#
# for e in final_collection.find():
#     pprint.pprint(e)

offset = 37280
ii = 0
while ii < 4:
    position = offset+2400
    print datetime.now()

    dt = datetime.now() + timedelta(hours=1)

    # 2- create a mongodb collection for the elements we want
    create_database_from_forks_events(offset, position)


    # dt = dt.replace(minute=10)
    #
    while datetime.now() < dt:
        time.sleep(1)

    offset = position
    ii += 1



# print final_collection.count()


