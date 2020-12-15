from operator import itemgetter
from github import Github
import networkx as nx
import sys
import matplotlib.pyplot as plt

class githubStars:
    def __init__(self):
        self.ACCESS_TOKEN = ''
        self.USER = ''
        self.REPO = ''
        self.stargazers = ''
        self.client = ''
        self.repo = ''
        self.user = ''
        self.color_map = []

    def setToken(self, ACCESS_TOKEN):
        self.ACCESS_TOKEN = ACCESS_TOKEN

    def setUser(self, USER):
        self.USER = USER

    def setRepo(self, REPO):
        self.REPO = REPO

    def getGraph(self):
        self.client = Github(self.ACCESS_TOKEN, per_page=100)
        self.user = self.client.get_user(self.USER)
        self.repo = self.user.get_repo(self.REPO)
        self.stargazers = [s for s in self.repo.get_stargazers()]
        print("Количество лайков", len(self.stargazers))
        g = nx.DiGraph()
        self.color_map = []
        self.color_map.append('red')
        g.add_node(self.repo.name + '(repo)', type='repo', lang=self.repo.language, owner=self.user.login)
        for sg in self.stargazers:
            self.color_map.append('blue')
            g.add_node(sg.login + '(user)', type='user')
            g.add_edge(sg.login + '(user)', self.repo.name + '(repo)', type='gazes')
        return g

    def getMoreGraph(self, g):
        for i, sg in enumerate(self.stargazers):
            # Добавить ребра "следования” между пользователями в графе,
            # если это отношение существует
            try:
                for follower in sg.get_followers():
                    if follower.login + '(user)' in g:
                        g.add_edge(follower.login + '(user)', sg.login + '(user)',
                                   type='follows')
            except Exception as e:
                print("Encountered an error fetching followers for", sg.login,
                      "Skipping.", file=sys.stderr)
                print(e, file=sys.stderr)
            print("Processed", i + 1, " stargazers. Num nodes/edges in graph",
                  g.number_of_nodes(), g.number_of_edges())
            print("Rate limit remaining", self.client.rate_limiting)
        # Вывести меры центральности для топ-10 узлов
        h = g.copy()
        dc = sorted(nx.degree_centrality(h).items(),
                    key=itemgetter(1), reverse=True)
        print("Degree Centrality")
        print(dc[:10])
        print()
        bc = sorted(nx.betweenness_centrality(h).items(),
                    key=itemgetter(1), reverse=True)
        print("Betweenness Centrality")
        print(bc[:10])
        print()
        print("Closeness Centrality")
        cc = sorted(nx.closeness_centrality(h).items(),
                    key=itemgetter(1), reverse=True)
        print(cc[:10])

        return g

    def plotGraph(self, g):
        print(nx.info(g))
        nx.draw(g, node_color=self.color_map, with_labels=True)
        plt.show()
