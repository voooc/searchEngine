# -!- coding: utf-8 -!-
from pygraph.classes.digraph import digraph


class PRIterator:
    __doc__ = '''计算一张图中的PR值'''

    def __init__(self):
        self.damping_factor = 0.85   # 阻尼系数,即α
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001    # 确定迭代是否结束的参数
        self.graph = digraph()
        self.path = '../data/relation.txt'

    def read_data(self):
        with open(self.path, encoding='utf-8') as f:
            txt = f.read()
        lines = txt.strip().split('\n')
        node_list = []
        edge_list = []
        for e in lines[0:]:
            if [e.split(' ')[0], e.split(' ')[1]] not in edge_list:
                node_list.append(e.split(' ')[0])
                node_list.append(e.split(' ')[1])
                edge_list.append([e.split(' ')[0], e.split(' ')[1]])
        node_list = list(set(node_list))
        self.graph.add_nodes(node_list)
        self.graph.add_edge(e)

    def page_rank(self):
        self.read_data()
        #  先将图中没有出链的节点改为对所有节点都有出链
        print(len(self.graph.nodes()))
        num = 0
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:
                for node2 in self.graph.nodes():
                    num += 1
                    print(num)
                    digraph.add_edge(self.graph, (node, node2))
        nodes = self.graph.nodes()
        graph_size = len(nodes)
        if graph_size == 0:
            return
        page_rank = dict.fromkeys(nodes, 1.0/graph_size)  # 给每个节点赋予初始的PR值
        damping_value = (1.0 - self.damping_factor) / graph_size  # 公式中的(1−α)/N部分
        for i in range(self.max_iterations):
            change = 0
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):  # 遍历所有“入射”的页面
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)  # 绝对值
                page_rank[node] = rank
            print("This is NO.%s iteration" % (i + 1))
            if change < self.min_delta:
                break
        return page_rank







