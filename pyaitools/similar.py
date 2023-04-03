import numpy as np
from collections import Counter
from itertools import chain


class Cset:
    def __init__(self, list_set):
        self.list_set = list_set
        # 集合被并展开成列表
        self.list_set_flat = list(chain(*list_set))

    def get_origin_list_set_index(self, index):
        """通过输入平展列表的索引，获得原始list_set中所在集合的索引"""
        flat_dict = dict()
        tmp_len = 0
        for i, k in enumerate(self.list_set):
            for j in range(0, len(k)):
                flat_dict.update({tmp_len + j: i})
            tmp_len += len(k)
        return flat_dict[index]


def find_connected_area(list_set, connected_area_min_num=2):
    Cls = Cset(list_set)
    lsf = Cls.list_set_flat

    repeat_e = []
    for key, value in dict(Counter(lsf)).items():
        if value > 1:
            repeat_e.append(key)
    for i, re in enumerate(repeat_e):
        lsf = np.array(lsf)
        result = np.where(lsf == re)
        if len(result[0]) <= 1:
            continue
        merge_set_index = list(
            map(lambda x: Cls.get_origin_list_set_index(x), result[0])
        )
        new_list_set = list()
        new_l_set = set()
        for i, ls in enumerate(list_set):
            if i in merge_set_index:
                new_l_set = new_l_set | ls
            else:
                new_list_set.append(ls)
        new_list_set = [new_l_set] + new_list_set
        list_set = new_list_set
        Cls = Cset(list_set)
        lsf = Cls.list_set_flat

    list_set = list(filter(lambda x: len(x) > connected_area_min_num, list_set))
    return list_set


# pip install networkx==2.3
# import networkx as nx

'''
def find_connected_area(input_list, similar_input_list, connected_area_min_num=0):
    """根据相似关系找出连通子图"""
    G = nx.Graph()
    G.add_nodes_from(input_list)
    G.add_nodes_from(similar_input_list)
    G.add_edges_from(list(zip(input_list, similar_input_list)))
    c_dict = nx.all_pairs_node_connectivity(G)
    c_list = []
    for key, value in c_dict.items():
        c_set = set({key})
        for k, v in value.items():
            if v:
                c_set.add(k)
        if c_set not in c_list and len(c_set) > connected_area_min_num:
            c_list.append(c_set)
    return c_list 
'''


if __name__ == "__main__":
    input_list = ["A", "B", "C", "A"]
    similar_input_list = ["a", "b", "c", "b"]
    list_set = list(zip(input_list, similar_input_list))
    list_set = list(map(lambda x: set(x), list_set))
    c_list = find_connected_area(list_set, 2)
    print(c_list)
    # [{'A', 'a'}, {'B', 'b'}, {'c', 'C'}]
