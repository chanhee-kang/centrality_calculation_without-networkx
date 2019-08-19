import pandas as pd
from multiprocessing import Pool, cpu_count, Queue
from tqdm import tqdm

class Graph():
    def __init__(self, node_list):
        self.node_list = node_list
        self.num_node = len(node_list)
        self.graph = {name:{} for name in node_list.keys()}
        for name, node in tqdm(node_list.items(), desc="BUILD GRAPH"):
            for neighbor in node.get_neighbors():
                self.graph[name][neighbor] = 1

        self.paths = {start:{} for start in self.node_list}

        pool = Pool(cpu_count())  # multiprocessing pool
        paths = []

        # multiprocessing으로 shortestpath 계산 후 paths에 결과 출력
        for result in tqdm(pool.imap_unordered(self.save_shortestPath, enumerate(list(self.node_list)[:-1])),
                        desc="GET SHORTEST PATH", total=len(self.node_list)-1):
            paths += result

        for path in paths:
            self.paths[path[0]][path[1]] = path[2]
            self.paths[path[1]][path[0]] = path[2][::-1]  # 반대로 입력

        # multiprocessing 종료
        pool.close()
        pool.join()

    def save_shortestPath(self, tup):
        i = tup[0]
        start = tup[1]
        res = []
        for end in list(self.node_list)[i+1:]:
            shortestPath = self.shortestPathBFS(start, end)
            res.append((start,end,shortestPath))  # tuple로 저장
        return res

    def get_neighbors(self, node_name):
        return self.graph[node_name].keys()

    def get_graph(self):
        return self.graph

    def shortestPathBFS(self, start, end):
        visited = set([start])
        prev = {}
        queue = [start]  # bfs를 위한 queue
        while len(queue)>0:
            node = queue.pop(0)  # queue에 있는 첫번째 node
            if node == end: #도착 노드를 찾았으면 탐색 종료
                break
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    prev[neighbor] = node #queue에 추가하면서 이전노드를 기록

        def path(node):
            shortest_path = [node]
            while node != start:
                node = prev[node]  # prev 정보를 타고 path 생성
                shortest_path.insert(0, node)
            return shortest_path

        return path(node)

    def get_degree_centrality(self, node_name: str):
        return len(self.graph[node_name].keys())  # 연결된 모든 노드의 수

    def get_closeness_centrality(self, node_name: str):
        closeness = 0
        for path in self.paths[node_name].values():
            closeness += len(path)  # path 길이 만큼이 closeness
        return (self.num_node - 1) / max(1, closeness)  # closeness 값이 0이 됨을 방지

    def get_betweenness_centrality(self, node_name: str):
        total = 0  # 모든 shortest path 수
        betweenness = 0
        for other_node in self.node_list:
            if node_name != other_node:
                for path in self.paths[other_node].values():
                    total += 1
                    if node_name in path:  # path에 해당 노드가 있으면
                        betweenness += 1  # counting
        return node_name, betweenness / total

class Node():
    def __init__(self, name):
        self.name = name
        self.accessibility = {}

    def add_edge(self, airport):  # edge counting (accessibility)
        if airport.name in self.accessibility:
            self.accessibility[airport.name] += 1
            airport.accessibility[self.name] += 1
        else:
            self.accessibility[airport.name] = 1
            airport.accessibility[self.name] = 1

    def get_neighbors(self):
        return self.accessibility.keys()

if __name__ == "__main__":
    df = pd.read_csv("/Users/chanhee.kang/Desktop/centrality/routes.csv")  # pandas 모듈로 csv 파일 읽기
    source = df['sourceairport']
    dest = df['destinationairport']
    node_list = {}  # name : node

    for s, d in zip(source, dest):
        if s not in node_list:  # dictionary 등록
            ns = Node(s)
            node_list[s] = ns
        if d not in node_list:  # dictionary 등록
            nd = Node(d)
            node_list[d] = nd
        node_list[s].add_edge(node_list[d])  # dictionary 갱신

    graph = Graph(node_list)

    # degree centrality
    degree_centrality = []
    for name in tqdm(node_list, desc="CLOSENESS CENTRALITY"):
        degree_centrality.append((name, graph.get_degree_centrality(name)))
    degree_centrality = pd.DataFrame(degree_centrality, columns = ['airport', 'degree_centrality'])
    degree_centrality = degree_centrality.sort_values(['degree_centrality'], ascending=[False])
    degree_centrality.to_csv('csv file')

    # closeness centrality
    closeness_centrality = []
    for name in tqdm(node_list, desc="CLOSENESS CENTRALITY"):
        closeness_centrality.append((name, graph.get_closeness_centrality(name)))
    closeness_centrality = pd.DataFrame(closeness_centrality, columns = ['airport', 'closeness_centrality'])
    closeness_centrality = closeness_centrality.sort_values(['closeness_centrality'], ascending=[False])
    closeness_centrality.to_csv('csv file')

    # betweenness centrality
    pool = Pool(cpu_count())
    betweenness_centrality = []
    for name, betweenness in tqdm(pool.imap_unordered(graph.get_betweenness_centrality, node_list), desc="BETWEENNESS CENTRALITY"):
        betweenness_centrality.append((name, betweenness))  # betweenness 계산에 multiprocessing 적용
    betweenness_centrality = pd.DataFrame(betweenness_centrality, columns = ['airport', 'betweenness_centrality'])
    betweenness_centrality = betweenness_centrality.sort_values(['betweenness_centrality'], ascending=[False])
    betweenness_centrality.to_csv('csv file')

    # multiprocessing 종료
    pool.close()
    pool.join()

    print(degree_centrality)
    print(closeness_centrality)
    print(betweenness_centrality)
