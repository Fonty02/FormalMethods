#pip install visual-automata
from visual_automata.fa.dfa import VisualDFA

import json

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
    states = set()
    input_symbols = set()
    for s in dfa_description["states"]:
        states.add(s)
    for a in dfa_description["alphabet"]:
        input_symbols.add(a)
    initial_state = dfa_description["initial_state"]
    final_states = set()
    for f in dfa_description["accepting_states"]:
        final_states.add(f)
    transitions = {}
    for t in dfa_description["transitions"]:
        if t["from"] not in transitions:
            transitions[t["from"]] = {}
        transitions[t["from"]][t["input"]] = t["to"]
    #for every state, if there is no transition for a symbol, add a transition to a dead state
    dead_state = "q_dead"
    states.add(dead_state)
    for s in states:
        if s not in transitions:
            transitions[s] = {}
        for i in input_symbols:
            if i not in transitions[s]:
                transitions[s][i] = dead_state
    
    dfa = VisualDFA(states=states, input_symbols=input_symbols, transitions=transitions, initial_state=initial_state, final_states=final_states)
    dfa.show_diagram()
    
    


dfa_description=fromJSONtoDict("def.json")
print(run_dfa(dfa_description, "a"))
print(run_dfa(dfa_description, "b"))
print(run_dfa(dfa_description, "aab"))
print(run_dfa(dfa_description, "adsada"))
draw_dfa(dfa_description)
