import networkx as nx
import json
import matplotlib.pyplot as plt

def fromJSONtoDict(filepath):
    with open(filepath, 'r') as file:
        json_string = file.read()
    return json.loads(json_string)

def run_dfa(dfa, input_string):
    current_state = dfa["initial_state"]
    for symbol in input_string:
        transition=None
        for t in dfa["transitions"]:
            if t["from"] == current_state and t["input"] == symbol:
                transition = t
                break
        if transition is None:
            return "INPUT NOT VALID"
        current_state = transition["to"]
    return "Accepted" if current_state in dfa["accepting_states"] else "Rejected"

def draw_dfa(dfa_description):
    G = nx.DiGraph()
    for t in dfa_description["transitions"]:
        G.add_edge(t["from"], t["to"], label=t["input"])
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    node_colors=[]
    for node in G.nodes():
        if node==dfa_description["initial_state"]:
            node_colors.append("yellow")
        elif node in dfa_description["accepting_states"]:
            node_colors.append("green")
        else:
            node_colors.append("grey")
    nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=2000, font_size=20, font_weight="bold", width=2, edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.scatter([],[], color="yellow", label="Initial State")
    plt.scatter([],[], color="green", label="Accepting State")
    plt.scatter([],[], color="grey", label="Normal State")
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title="Node Colors")
    plt.title("DFA")
    plt.size=(20,20)
    plt.show()
    
    


dfa_description=fromJSONtoDict("def.json")
draw_dfa(dfa_description)
print(run_dfa(dfa_description, "a"))
print(run_dfa(dfa_description, "b"))
print(run_dfa(dfa_description, "aab"))
print(run_dfa(dfa_description, "adsada"))
