import networkx as nx
import os
import json
import pandas as pd


def getJsonData_funcGNN_version(graph, target_mr):
    if graph.has_node('\\n'):
        graph.remove_node('\\n')
    edge_list = []
    # convert the node labels which are strings to sorted integers without affecting the node attributes.
    graph_with_int_id = nx.relabel.convert_node_labels_to_integers(graph, first_label=0, ordering='sorted',
                                                                   label_attribute=None)

    edge_tuples = list(graph_with_int_id.edges(data=False))

    # get graph edge lists
    for i in edge_tuples:
        edge_list.append(list(i))

    # get graph attributes in the ascending order as the node labels
    node_label_list = []

    node_list_sorted = list(sorted(graph_with_int_id.nodes(data=True)))

    for i in range(len(node_list_sorted)):
        if node_list_sorted[i][0] == i and node_list_sorted[i][1].get('label') is not None:
            node_label_list.insert(i, node_list_sorted[i][1].get('label').replace('"', ''))
        else:
            print("Node {} \n is not sorted in the node list, or has no label - this node will be ignored".format(
                node_list_sorted[i]))

    jsonDict = {}
    jsonDict["graph_1"] = edge_list
    jsonDict["labels_1"] = node_label_list
    jsonDict["mr_label"] = target_mr

    # print(jsonDict)
    return jsonDict


def getJsonData_labels_as_dict(graph, target_mr):
    if graph.has_node('\\n'):
        graph.remove_node('\\n')
    g1_edgeList = []
    node_labels_dict = {}

    # convert the node labels which are strings to sorted integers without affecting the node attributes.
    graph_with_int_id = nx.relabel.convert_node_labels_to_integers(graph, first_label=0, ordering='default',
                                                                   label_attribute=None)
    # print(sortedIntGraph_1)

    edge_tuples = list(graph_with_int_id.edges(data=False))

    # get graph edge lists
    for i in edge_tuples:
        g1_edgeList.append(list(i))

    # get graph attributes in the ascending order as the node labels
    node_label_list = []

    nodeList_g1 = list(sorted(graph_with_int_id.nodes(data=True)))
    # print(nodeList_g1)
    # print(len(nodeList_g1))

    for i in range(len(nodeList_g1)):
        if nodeList_g1[i][0] == i and nodeList_g1[i][1].get('label') is not None:
            # print(nodeList_g1[i][1].get('label'))
            node_label_list.insert(i, nodeList_g1[i][1].get('label').replace('"', '').replace('[', '').replace(']',
                                                                                                               '').replace(
                ':', '').replace('@', '').replace('int', '').replace('double', '').strip())
            tmp = nodeList_g1[i][1].get('label').replace('"', '').replace('[', '').replace(']', '').replace(':',
                                                                                                            '').replace(
                '@', '').replace('int', '').replace('double', '').strip()
            node_labels_dict[i] = str(tmp)
        else:
            print("Node {} \n is not sorted in the node list, or has no label - this node will be ignored".format(
                node_label_list[i]))

    # generate the json files
    jsonDict = {}
    jsonDict["edges"] = g1_edgeList
    jsonDict["labels"] = node_labels_dict
    jsonDict["target"] = target_mr

    # print(jsonDict)
    return jsonDict


def dumpJson(output_dir, jsonFile, g1):  # function to dump the Json files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(str(output_dir) + str(g1) + '.json', 'w') as fp:
        json.dump(jsonFile, fp)


def main():
    mr_types = ["MR_ADD", "MR_EXC", "MR_INC", "MR_INV", "MR_MUL", "MR_PER"]
    # dotFile_data_path = '/Users/katrinaliang/Documents/funcGNN_for_PMR/dotFiles/'
    dotFile_data_path = '/Users/katrinaliang/Documents/SPAT/DotFiles/baseline_dot/'
    mr_labels_csv = "/Users/katrinaliang/Documents/SPAT/listMet_labelsMR.csv"

    for mr in mr_types:
        count_dot_files = 0
        json_output_dir = '/Users/katrinaliang/Documents/funcGNN_for_PMR/baseline_json/' + mr + '/'
        df_mr = pd.read_csv(mr_labels_csv).set_index('Method_Name')
        df_mr = df_mr[[mr]]

        dot_files = [f for f in os.listdir(dotFile_data_path) if
                     os.path.isfile(os.path.join(dotFile_data_path, f)) and f.endswith('.dot')]

        for dot in dot_files:
            method_name = dot.split('_m.')[0]
            graph = nx.drawing.nx_pydot.read_dot(str(dotFile_data_path) + str(dot))

            MR_add_target = df_mr.loc[method_name][mr]
            jsonData = getJsonData_funcGNN_version(graph, int(MR_add_target))
            dumpJson(json_output_dir, jsonData, method_name)
            count_dot_files += 1

        print("Converted {} dot files to JSON. \n Saved in {}".format(count_dot_files, json_output_dir))


if __name__ == '__main__':
    main()
