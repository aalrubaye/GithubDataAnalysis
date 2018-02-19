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
users = database.users

def print_first_elem(collection):
    for a in collection.find():
          pprint.pprint(a)
          break

def print_in_range(collection, range):
    index = 0
    for a in collection.find():
          pprint.pprint(a)
          if index == range:
            break
          else:
              print_separator()
              index += 1


def print_in_range_between_collections(collection1,collection2,field, range):
    index = 0
    for a in collection1.find():
          print_with_condition(collection2, field, a['actor']['login'])
          if index == range:
            break
          else:
              print_separator()
              index += 1


def print_with_condition(collection, field, value):
    for a in collection.find():
      if a[field] == value:
        pprint.pprint(a)

def print_separator():
    print ('---------------------------------------------------------------------------')

# reading from a url
def read_url(url) :
    response = urllib2.urlopen(url)
    data = simplejson.load(response)
    pprint.pprint(data[1])
    pprint.pprint(data[1]["login"])


# url = "https://api.github.com/users/hackernix/followers"
# read_url(url)

# print collection.count()



print_in_range_between_collections(events,users, 'login', 100)
# print_first_elem(events)
# print_separator()
# print_first_elem(users)
# print_with_condition(users,'login','davidlewallen')
