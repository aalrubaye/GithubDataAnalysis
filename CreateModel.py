import MongoConnection
import pprint
import networkx as nx

__author__ = 'Abdul Rubaye'


# The main class of generated the model
class ModelGenerator:

    # create a network instance
    graph = nx.Graph()

    def __init__(self):
        # connects to the db
        self.final_collection = MongoConnection.connect()

        self.generate_graph()

    # print function
    def print_entry(self):
        for elem in self.final_collection.find():
            pprint.pprint(elem)
            break

    # Add the model nodes and edges
    def generate_graph(self):

        for entry in self.final_collection.find():
            # add the repo node + adding some attributes to the node
            self.graph.add_node(entry['repo_name'],
                                repo_size=entry['repo_size'],
                                repo_language=entry['repo_language'],
                                repo_forks_count=entry['repo_forks_count'],
                                repo_network_count=entry['repo_network_count'],
                                repo_stargazers=entry['repo_stargazers'],
                                repo_subscribers_count=entry['repo_subscribers_count'],
                                repo_watchers=entry['repo_watchers'])
            # add the actor node
            self.graph.add_node(entry['actor'])

            # connect actor node -> repo node
            self.graph.add_edge(entry['repo_name'], entry['actor'])

            # add the followers node
            # connect followers node -> actor node
            for follower in entry['followers']:
                self.graph.add_node(follower)
                self.graph.add_edge(entry['actor'], follower)

        # export graph as a graphml file
        nx.write_graphml(self.graph, "/Users/Abduljaleel/Desktop/model.graphml")


if __name__ == "__main__":
    ModelGenerator()
