from pymongo import MongoClient


__author__ = 'Abdul Rubaye'


def connect():
    client = MongoClient()
    database = client.github_16
    # final_collection = database.final_collection
    collection = database.collection_no_noise
    return collection
