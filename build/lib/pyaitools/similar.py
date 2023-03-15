
# pip install networkx==2.3
import networkx as nx



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




if __name__ == "__main__":
    input_list = ["A","B","C","A"]
    similar_input_list = ["a","b","c","b"]
    c_list = find_connected_area(input_list, similar_input_list)
    print(c_list)
    # [{'A', 'a'}, {'B', 'b'}, {'c', 'C'}]
