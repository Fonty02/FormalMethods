import pm4py
import matplotlib.pyplot as plt
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
import pm4py.write as write_xes
from pm4py.algo.evaluation.replay_fitness import algorithm as fitness
from pm4py.algo.evaluation.precision import algorithm as precision
from pm4py.algo.evaluation.simplicity import algorithm as simplicity
from pm4py.algo.evaluation.generalization import algorithm as generalization

def format_csv(input_file, output_file):
    """
    This function reads a CSV file and formats it in a specific way.
    Args:
        input_file (str): Name of the input CSV file
        output_file (str): Name of the output CSV file
    """
    formatted_rows = []
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            #Add the header
            formatted_rows.append("Timestamp, CaseID, Activity")
            # Format each line in the file
            for line in lines:
                line = line.strip()
                if not line:  # Ignore empty lines
                    continue
                elements = line.split()
                if len(elements) >= 4:  
                    timestamp = f"{elements[0]} {elements[1]}"
                    case_id = elements[2]
                    activity = ' '.join(elements[3:])
                    formatted_row = f"{timestamp}, {case_id}, {activity}"
                    formatted_rows.append(formatted_row)
        # Write the formatted rows to the output file
        with open(output_file, 'w', newline='') as file:
            for row in formatted_rows:
                file.write(row + '\n')
    except Exception as e:
        print(f"A problem occurred while formatting the CSV file: {e}")
        

def csv_to_xes(input_file):
    """
    This function reads a CSV file and converts it to a XES file.
    Args:
        input_file (str): Name of the input CSV file
    """
    data = pd.read_csv(input_file, sep=",")
    cols = ['time:timestamp', 'case:concept:name','concept:name']
    data.columns = cols
    data['time:timestamp'] = pd.to_datetime(data['time:timestamp'])
    data['concept:name'] = data['concept:name'].astype(str)
    log = log_converter.apply(data, variant=log_converter.Variants.TO_EVENT_LOG)
    #the output file is named as the input file with the extension .xes
    output_name = input_file.split(".")[0] + ".xes"
    write_xes.write_xes(log, output_name)




def plot_metrics(alpha_metrics, heuristic_metrics, inductive_metrics):
    """
    This function plots the metrics of different process discovery algorithms.
    Args:
        alpha_metrics (tuple): Tuple containing the metrics of the Alpha Miner
        heuristic_metrics (tuple): Tuple containing the metrics of the Heuristic Miner
        inductive_metrics (tuple): Tuple containing the metrics of the Inductive Miner
    """
    algorithms = ['Alpha Miner', 'Heuristic Miner', 'Inductive Miner']
    metrics = ['Fitness', 'Precision', 'Simplicity', 'Generalization']
    
    # Replace None with 0 for plotting
    def handle_none(metric):
        return [0 if x is None else x for x in metric]

    values = [
        handle_none([alpha_metrics[0], heuristic_metrics[0], inductive_metrics[0]]),  # Fitness
        handle_none([alpha_metrics[1], heuristic_metrics[1], inductive_metrics[1]]),  # Precision
        handle_none([alpha_metrics[2], heuristic_metrics[2], inductive_metrics[2]]),  # Simplicity
        handle_none([alpha_metrics[3], heuristic_metrics[3], inductive_metrics[3]])   # Generalization
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for i, metric in enumerate(metrics):
        axes[i].bar(algorithms, values[i], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        axes[i].set_title(metric)
        axes[i].set_ylabel("Valore")
        axes[i].set_ylim(0, 1)
    plt.tight_layout()
    plt.suptitle("Comparing Process Discovery Algorithms",  fontsize=14, y=1.02)
    plt.savefig("images/metrics.png")
    plt.close()


def Heuristic_mining(file_path):
    """
    This function performs the Heuristic Miner algorithm on an event log.
    Args:
        file_path (str): Path to the XES file
        Returns:
        tuple: Tuple containing the metrics of the Heuristic Miner
    """
    event_log = pm4py.read_xes(file_path)
    net, initial_marking, final_marking = heuristics_miner.apply(event_log)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.save(gviz, "images/heuristic_miner.png")
    
    fitness_value = fitness.apply(event_log, net, initial_marking, final_marking)["averageFitness"]
    precision_value = precision.apply(event_log, net, initial_marking, final_marking)  # Direct float value
    simplicity_value = simplicity.apply(net)
    generalization_value = generalization.apply(event_log, net, initial_marking, final_marking)
    
    l=[fitness_value, precision_value, simplicity_value, generalization_value]
    return l


def Inductive_mining(file_path):
    """
    This function performs the Inductive Miner algorithm on an event log.
    Args:
        file_path (str): Path to the XES file
    Returns:
        tuple: Tuple containing the metrics of the Inductive Miner
    """
    event_log = pm4py.read_xes(file_path)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.save(gviz, "images/inductive_miner.png")


    fitness_value = fitness.apply(event_log, net, initial_marking, final_marking)["averageFitness"] 
    precision_value = precision.apply(event_log, net, initial_marking, final_marking)
    simplicity_value = simplicity.apply(net)
    generalization_value = generalization.apply(event_log, net, initial_marking, final_marking)
    
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    l=[fitness_value, precision_value, simplicity_value, generalization_value]
    return l

def Alpha_mining(file_path):
    """
    This function performs the Alpha Miner algorithm on an event log and evaluates the model.
    Args:
        file_path (str): Path to the XES file
    Returns:
        tuple: Tuple containing the metrics of the Alpha Miner
    """
    event_log = pm4py.read_xes(file_path)
    
    # Apply Alpha Miner to discover the Petri net
    net, initial_marking, final_marking = alpha_miner.apply(event_log)
    
    fitness_value = fitness.apply(event_log, net, initial_marking, final_marking)["averageFitness"]  # Direct dictionary
    precision_value = precision.apply(event_log, net, initial_marking, final_marking)  # Direct float value
    simplicity_value = simplicity.apply(net)
    generalization_value = generalization.apply(event_log, net, initial_marking, final_marking)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.save(gviz, "images/alpha_miner.png")
    
    l=[fitness_value, precision_value, simplicity_value, generalization_value]
    return l


def Process_Map(file_path):
    """
    This function reads an event log and discovers the Directly-Follows Graph (DFG).
    Args:
        file_path (str): Path to the XES file
    """

    event_log = pm4py.read_xes(file_path)
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
    pm4py.save_vis_dfg(dfg, start_activities, end_activities, "images/dfg.png")
    

if __name__ == "__main__":
    
    input_file = "base_kasteren.csv"
    #the output file is named input_file_name_formatted.csv
    output_file = input_file.split(".")[0] + "_formatted.csv"
    format_csv(input_file, output_file)
    csv_to_xes(output_file)
    Path = output_file.split(".")[0] + ".xes"

    # Process Map
    Process_Map(Path)
    
    # Execute the mining
    alpha_metrics = Alpha_mining(Path)
    heuristic_metrics = Heuristic_mining(Path)
    inductive_metrics = Inductive_mining(Path)

    plot_metrics(alpha_metrics, heuristic_metrics, inductive_metrics)

