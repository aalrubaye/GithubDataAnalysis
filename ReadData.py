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
collection = database.repos

# for a in collection.find():
#       # pprint.pprint(a)
#       # break
#       if a['watchers_count'] != 0:
#         print a['created_at']
#         print

# print collection.count()





# ------------------------------------------------------------

# reading from a url
def read_url(url) :
    response = urllib2.urlopen(url)
    data = simplejson.load(response)
    pprint.pprint(data[1])
    pprint.pprint(data[1]["login"])


url = "https://api.github.com/users/hackernix/followers"
read_url(url)

# ------------------------------------------------------------
