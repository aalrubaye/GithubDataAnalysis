import random

import MongoConnection
import networkx as nx
import numpy as np
from enum import Enum

__author__ = 'Abdul Rubaye'


# The main class of generated the model
class ModelGenerator:

    # create a network instance
    graph = nx.Graph()
    # number of the times we aim to generate extra models
    models_number = 2
    limit = 100
    is_random = True
    time = 0
    forks = []
    repos = []

    def __init__(self):
        # connects to the db
        self.final_collection = MongoConnection.connect()
        # True = random
        # False = Prob_random
        self.generate_graph(False)


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
    def generate_graph(self, rnd):
        self.is_random = rnd

        index = 0

        for entry in self.final_collection.find():
            # add the repo node + adding some attributes to the node
            self.add_node(entry, entry['repo_name'], self.node_type('Repo'))
            self.forks.append(entry['repo_forks_count'])
            self.repos.append(entry['repo_name'])

            # add the actor node
            self.add_node(entry, entry['actor'], self.node_type('Actor'))

            # connect actor node -> repo node
            self.graph.add_edge(entry['repo_name'], entry['actor'])

            index += 1
            print index
            if index == self.limit:
                break

        self.repo_repo()

    # If a user forked more than a repo, this def will connects them
    def repo_repo(self):
        for node in self.graph.degree:
            if node[1] > 1:
                rp_to_be_connected = []
                for rp in self.graph.edges(node[0]):
                    rp_to_be_connected.append(rp[1])
                rp_len = len(rp_to_be_connected)
                for k in range(rp_len):
                    for j in range(k+1,rp_len):
                        rp1 = rp_to_be_connected[k]
                        rp2 = rp_to_be_connected[j]
                        self.graph.add_edge(rp1, rp2)
        self.follower_actor()

    # Connects the followers to users
    def follower_actor(self):
        print ('Followers')
        followers = []
        index = 0
        for entry in self.final_collection.find():
            flwrs = []
            # add the followers node
            # connect followers node -> actor node
            for follower in entry['followers']:
                self.add_node(entry, follower, self.node_type('Follower'))
                self.graph.add_edge(entry['actor'], follower)
                flwrs.append(follower)
            followers.append(flwrs)
            index += 1
            print index
            if index == self.limit:
                break

        # exports graph as a graphml file
        nx.write_graphml(self.graph, "/Users/Abduljaleel/Desktop/"+self.model_name(self.is_random, self.time)+".graphml")
        self.time += 1
        # generates a second model with more connection but same nodes
        self.add_edges_to_graph(self.forks, followers, self.repos, self.time)

    # Adds edges to the graph based on different probabilities
    def add_edges_to_graph(self, forks_list, followers, repos_list, time):
        if self.models_number > 0:
            print('-'*100)
            print('Generating the model at time t'+str(time))
            # Making a copy of the lists just to pass them in the next edges generation iteration
            forks = forks_list[:]
            repos = repos_list[:]

            # index_list is a list of those elements that will be evaluated
            # those elements index will be be evaluated that follower[index] is not empty
            index_list = []

            for i in range(len(followers)):
                if len(followers[i]) != 0:
                    index_list.append(i)

            for i in range(len(forks)):
                if self.is_random is False:
                    prob = self.compute_probabilities(forks, index_list)
                    index_of_rand, rand = self.weight_random_pick(prob, index_list)
                else:
                    index_of_rand, rand = self.random_pick(index_list)
                # print prob
                # print index_list
                # print rand

                follower_to_connect = followers[rand].pop()
                self.graph.add_edge(repos[rand], follower_to_connect)
                self.graph.node[repos[rand]]['repo_forks_count'] += 1
                self.graph.node[follower_to_connect]['node_type'] = self.node_type('Actor')
                forks[rand] += 1
                if len(followers[rand]) == 0:
                    # print ('done')
                    index_list.pop(index_of_rand)
                # print ('-'*100)
                print i

            # export graph as a graphml file
            nx.write_graphml(self.graph, "/Users/Abduljaleel/Desktop/"+self.model_name(self.is_random, time)+".graphml")
            self.models_number -= 1
            self.add_edges_to_graph(forks_list, followers, repos_list, time+1)

    # Computes the probabilities of a set of numbers
    def compute_probabilities(self, forks, index):
        cumulative_forks_count = 0
        for i in range(len(forks)):
            if i in index:
                cumulative_forks_count += forks[i]
        prob = []
        for j in range(len(forks)):
            if j in index:
                prob.append(float(forks[j])/float(cumulative_forks_count))
        return prob

    # Picks a random number
    def weight_random_pick(self, prob_list, index_list):
        rand = np.random.choice(len(prob_list), 1, p=prob_list)[0]
        # while rand not in index_list:
        #     rand = np.random.choice(len(prob_list), 1, p=prob_list)[0]
        return rand, index_list[rand]


    def random_pick(self, index_list):
        rand = np.random.randint(len(index_list), size=1)[0]
        return rand, index_list[rand]

    def node_type(self, t):
        switcher = {
            'Repo': 3,
            'Actor': 2,
            'Follower': 1
        }
        return switcher.get(t, 1)

    # Extracts the correspondent index of a language
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

    # returns the model name for exporting graph file purposes
    def model_name(self, random, time):
        if random:
            return "random_model_t"+str(time)
        else:
            return "prob_model_t"+str(time)

if __name__ == "__main__":
    ModelGenerator()
