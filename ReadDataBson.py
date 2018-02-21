__author__ = 'Abdul Rubaye'

from pymongo import MongoClient
import pprint
import urllib2
import simplejson

# list of any database collections
# ["commit_comments", "commits", "events", "followers", "forks", "geo_cache", "issue_comments", "issue_events",
# 	"issues", "org_members", "pull_requests", "pull_requst_comments", "repo_collaborators", "repo_labels",
# 	"repos", "topics", "users", "watchers" ]

client = MongoClient()
database = client.github_16
events = database.events
events_forks = database.events_forks

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


# fetches the followers of a user from a url and create a list
def actor_followers_list(url):
    followers_list = []
    new_url = add_client_id_client_secret_to_url(url)
    try:
        response = urllib2.urlopen(new_url)
        data = simplejson.load(response)
        for actor in data:
            followers_list.append(actor['login'])
        return followers_list
    except urllib2.URLError, e:
        return 'null'


# fetches the user object from a url and calls the followers list creator
def read_actor_login(url):
    new_url = add_client_id_client_secret_to_url(url)
    try:
        response = urllib2.urlopen(new_url)
        data = simplejson.load(response)
        return actor_followers_list(data['followers_url'])
    except urllib2.URLError, e:
        return 'null'


# appends the client id and the client secret to urls
def add_client_id_client_secret_to_url(url):
    return url+'?client_id='+client_id+'&client_secret='+client_secret


# to create a separate database out of the downloaded github bson file only for our work
def create_database():
    for event in events.find():
        repo = event['repo']['name'].split('/')[1]
        event_type = event['type']
        actor = event['actor']['login']
        followers = read_actor_login(event['actor']['url'])
        print repo,' - ', event_type, ' - ', actor, ' - ' , followers


# separate ForkEvents and insert them in a collection
def feed_collection():
    index = 1
    for elem in events.find():
        if elem['type'] == 'ForkEvent':
            events_forks.insert(elem)
            index += 1
            print index


# below is the area where I call the functions

feed_collection()

