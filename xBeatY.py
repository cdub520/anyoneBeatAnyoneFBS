import urllib.request
import urllib.parse
import json
import sys

class Graph:
    def __init__(self):
        self.nodes=set()
        self.edges={}
        self.distances = {}
    def add_edge(self, win_team, lose_team):
        if win_team == None:
            self.edges[lose_team] = []
        if win_team not in self.edges:
            self.edges[win_team] = [lose_team]
        else:
            self.edges[win_team].append(lose_team)
        self.distances[(win_team,lose_team)] = 1    
                
    def getTeamWins(self,team_name):
        url = "https://api.collegefootballdata.com/games?"
        params = {'year':2019,'seasonType':'regular','team':team_name}
        url = url + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        season_json=json.loads(r.decode('utf-8'))
        if team_name not in self.nodes:
            self.nodes.add(team_name)
        for game in season_json:
            if game["home_points"]==None:
                break
        #team home and win
            elif (game["home_team"]==team_name and game["home_points"]>game["away_points"]):
                if game["away_team"] not in self.nodes:
                    self.nodes.add(game["away_team"])
                self.add_edge(team_name,game["away_team"])
                if game["away_team"] not in self.edges:
                    self.add_edge(None,game["away_team"])
        #team away and win
            elif (game["away_team"]==team_name and game["away_points"]>game["home_points"]):
                if game["away_team"] not in self.nodes:
                    self.nodes.add(game["home_team"])
                self.add_edge(team_name,game["home_team"])
                if game["home_team"] not in self.edges:
                    self.add_edge(None,game["home_team"])
            else:
                if team_name not in self.edges:
                    self.edges[team_name]=[]   
    def getTeamNames(self):
        url = "https://api.collegefootballdata.com/teams/fbs?year=2019"
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        season_json=json.loads(r.decode('utf-8'))
        for team in season_json:
            self.nodes.add(team["school"])

    def generate_1_depth_graph(self,center_team):
        self.getTeamWins(center_team)
        for team in self.edges[center_team]:
            self.getTeamWins(team)
    def generate_graph(self):
        self.getTeamNames()
        for teams in self.nodes.copy():
            self.getTeamWins(teams)


    def min_path(self,start,end):
        tdist, preceding_node =self.search(start)
        dist = tdist[end]
        backpath = [end]
        try:
            while end != start:
                end = preceding_node[end]
                backpath.append(end)
                path = list(reversed(backpath))
        except KeyError:
            path = None
        
        returnString="Because {0} beat {1}".format(path[0],path[1])
        for i in range(1,len(path)-1):
            returnString +="\nand {0} beat {1}".format(path[i],path[i+1])
        returnString+="\n{0} will beat {1}".format(path[0],path[len(path)-1])    
        print(returnString)
        return dist, path     
    def search(self,x_team):
        visited = {x_team: 0}
        path = {}
        nodes = set(self.nodes)
        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node

            if min_node is None:
                break
            nodes.remove(min_node)
            current_weight = visited[min_node]
            for edge in self.edges[min_node]:
                weight = current_weight + self.distances[(min_node,edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node                      
        return visited,path
def __main__():
    graph = Graph()
    graph.generate_graph()
    graph.min_path(sys.argv[1],sys.argv[2])
__main__()