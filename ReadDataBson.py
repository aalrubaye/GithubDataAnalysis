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

def print_first_elem(collection):
    for elem in collection.find():
          pprint.pprint(elem)
          break
    print collection.count()

def print_in_range(collection, range):
    index = 0
    for elem in collection.find():
          pprint.pprint(elem)
          if index == range:
            break
          else:
              print_separator()
              index += 1

def print_with_condition(collection, field, value):
    for elem in collection.find():
      if elem[field] == value:
        pprint.pprint(elem)

def print_separator():
    print ('---------------------------------------------------------------------------')

# reading from a url
def read_url(url) :
    response = urllib2.urlopen(url)
    data = simplejson.load(response)
    pprint.pprint(data[1])
    pprint.pprint(data[1]["login"])

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



def events_repo_users():

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


# url = "https://api.github.com/users/hackernix/followers"
# read_url(url)


# print_first_elem(events)
# print_separator()
# print_first_elem(users)
# print_with_condition(users,'login','davidlewallen')

# events_repo_users()
print_first_elem(events)

print_first_elem(repo)
