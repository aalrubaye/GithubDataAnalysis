__author__ = 'Abdul Rubaye'

from pymongo import MongoClient
import pprint
import urllib2
import simplejson
import os


# list of any database collections
# ["commit_comments", "commits", "events", "followers", "forks", "geo_cache", "issue_comments", "issue_events",
# 	"issues", "org_members", "pull_requests", "pull_requst_comments", "repo_collaborators", "repo_labels",
# 	"repos", "topics", "users", "watchers" ]

client = MongoClient()
database = client.github_16
events = database.events
users = database.users
repo = database.repos

# client id and client secret are used in calling the github API
# they will help to raise the maximum limit of calls per hour
file=open("privateVar.txt",'r').read()
client_id = file.split('\n', 1)[0]
client_secret = file.split('\n', 1)[1]


def print_first_elem(collection):
    for elem in collection.find():
          pprint.pprint(elem)
          break
    print collection.count()

def print_in_range(collection, offset, position):
    for elem in collection.find()[offset:position]:
          # pprint.pprint(elem)
          print elem['watchers_count']
          print_separator()


def print_with_condition(collection, field, value):
    for elem in collection.find():
      if elem[field] == value:
        pprint.pprint(elem)

def print_separator():
    print ('---------------------------------------------------------------------------')

# fetches the followers of a user from a url and create a list
def actor_followers_list(url):
    followers_list = []
    try:
        response = urllib2.urlopen(url)
        data = simplejson.load(response)
        for actor in data:
            followers_list.append(actor['login'])
        return followers_list
    except urllib2.URLError, e:
        return 'null'

# fetches the user object from a url and calls the followers list creator
def read_actor_login(url):
    try:
        response = urllib2.urlopen(url)
        data = simplejson.load(response)
        return actor_followers_list(data['followers_url'])
    except urllib2.URLError, e:
        return 'null'


def create_database():

    actor = ''
    repo = ''
    followers = []
    event_type = ''
    followers_count = 0

    for event in events.find():
        repo = event['repo']['name'].split('/')[1]
        event_type = event['type']
        actor = event['actor']['login']
        followers = read_actor_login(event['actor']['url'])
        print repo,' - ', event_type, ' - ', actor, ' - ' , followers



print client_secret
