import time

import MongoConnection
import pprint
import networkx as nx
from random import *
import random
import numpy as np

__author__ = 'Abdul Rubaye'


# The main class of generated the model
class ModelGenerator:

    # create a network instance
    graph = nx.Graph()

    def __init__(self):
        # connects to the db
        self.final_collection = MongoConnection.connect()
        self.generate_graph()

    def language(self, lang):
        switcher = {
            None: 0,
            'JavaScript': 1,
            'Java': 2,
            'Python': 3,
            'C++': 4,
            'HTML': 5,
            'PHP': 6,
            'Ruby': 7,
            'C': 8,
            'C#': 9,
            'Go': 10,
            'CSS': 11,
            'Shell': 12,
            'Jupyter Notebook': 13,
            'TypeScript': 14,
            'Objective-C': 15,
            'Swift': 16,
            'R': 17,
            'Vue': 18,
            'Kotlin': 19,
            'Scala': 20,
            'Other':21
        }
        return switcher.get(lang, 21)

    # print function
    def print_entry(self):
        for elem in self.final_collection.find():
            pprint.pprint(elem)
            break

    # Prepares and adds a node + attributes to the graph
    def add_node(self, entry, label, node_type):
        attributes = [-1 for _ in range(7)]
        if node_type == 3:
            attributes[0] = entry['repo_size']
            attributes[1] = self.language(entry['repo_language'])
            attributes[2] = entry['repo_forks_count']
            attributes[3] = entry['repo_network_count']
            attributes[4] = entry['repo_stargazers']
            attributes[5] = entry['repo_subscribers_count']
            attributes[6] = entry['repo_watchers']

        self.graph.add_node(label,
                            repo_size=attributes[0],
                            repo_language=attributes[1],
                            repo_forks_count=attributes[2],
                            repo_network_count=attributes[3],
                            repo_stargazers=attributes[4],
                            repo_subscribers_count=attributes[5],
                            repo_watchers=attributes[6],
                            node_type=node_type)

    # generates the model
    def generate_graph(self):

        index = 0

        forks = []
        followers = []
        repos = []

        for entry in self.final_collection.find():
            # add the repo node + adding some attributes to the node
            self.add_node(entry, entry['repo_name'], 3)
            forks.append(entry['repo_forks_count'])
            repos.append(entry['repo_name'])

            # add the actor node
            self.add_node(entry, entry['actor'], 2)

            # connect actor node -> repo node
            self.graph.add_edge(entry['repo_name'], entry['actor'])

            flwrs = []
            # add the followers node
            # connect followers node -> actor node
            for follower in entry['followers']:
                self.add_node(entry, follower, 1)
                self.graph.add_edge(entry['actor'], follower)
                flwrs.append(follower)
            followers.append(flwrs)
            index += 1
            # print index
            if index == 10:
                break

        # export graph as a graphml file
        nx.write_graphml(self.graph, "/Users/Abduljaleel/Desktop/model.graphml")

    # Adds edges to the graph based on different probabilities
    def add_edges_to_graph(self, forks, followers, repos):
        prob = self.compute_probabilities(forks)
        rand = self.rand_pick(prob)
        if len(followers[rand]) == 0:
            prob.pop(rand)
            followers.pop(rand)
            forks.pop(rand)
            repos.pop(rand)
        else:
            follower_to_connect = followers[rand].pop()
            self.graph.add_edge(repos[rand], follower_to_connect)
            self.graph.node[repos[rand]]['repo_forks_count'] += 1
            forks[rand] += 1
            if len(followers[rand]) == 0:
                prob.pop(rand)
                followers.pop(rand)
                forks.pop(rand)
                repos.pop(rand)

    # Computes the probabilities of a set of numbers
    def compute_probabilities(self, forks):
        summ = 0
        for i in range (len(forks)):
            summ += forks[i]
        probb = []
        for j in range(len(forks)):
            probb.append(float(forks[j])/float(summ))
        return probb

    # Picks a random action based on stochastic probabilities using numpy
    def rand_pick(self, prob_list):
        return np.random.choice(len(prob_list), 1, p=prob_list)[0]


if __name__ == "__main__":
    ModelGenerator()
