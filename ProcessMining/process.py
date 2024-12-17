# Importazione delle librerie
import pm4py
import matplotlib.pyplot as plt
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.evaluation import precision, simplicity, generalization

# Caricamento del log XES
def load_xes_log(file_path):
    try:
        print("Caricamento del file di log...")
        log = pm4py.read_xes(file_path)
        print("Log caricato con successo!")
        return log
    except Exception as e:
        print(f"Errore nel caricamento del file: {e}")
        return None

# Scoperta con Alpha Miner
def alpha_miner_discovery(log):
    print("\nScoperta del modello con Alpha Miner...")
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)
    #pm4py.view_petri_net(net, initial_marking, final_marking)
    return net, initial_marking, final_marking

# Scoperta con Heuristic Miner
def heuristic_miner_discovery(log):
    print("\nScoperta del modello con Heuristic Miner...")
    net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log)
   # pm4py.view_petri_net(net, initial_marking, final_marking)
    return net, initial_marking, final_marking

# Scoperta con Inductive Miner
def inductive_miner_discovery(log):
    print("\nScoperta del modello con Inductive Miner...")
    tree = pm4py.discover_process_tree_inductive(log)
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree)
    #pm4py.view_petri_net(net, initial_marking, final_marking)
    return net, initial_marking, final_marking

# Calcolo delle metriche per un modello scoperto
def evaluate_model(log, net, initial_marking, final_marking):
    print("\nValutazione delle metriche:")
    
    # Fitness tramite Token Replay
    replay_results = token_replay.apply(log, net, initial_marking, final_marking)
    fitness_value = replay_results["log_fitness"]
    
    # Precision
    precision_value = precision.evaluate(log, net, initial_marking, final_marking)
    
    # Simplicity
    simplicity_value = simplicity.evaluate(net)
    
    # Generalization
    generalization_value = generalization.evaluate(log, net, initial_marking, final_marking)
    
    # Output delle metriche
    print(f" - Fitness: {fitness_value:.4f}")
    print(f" - Precision: {precision_value:.4f}")
    print(f" - Simplicity: {simplicity_value:.4f}")
    print(f" - Generalization: {generalization_value:.4f}")
    
    return fitness_value, precision_value, simplicity_value, generalization_value

# Analisi comparativa con grafici
def plot_metrics(alpha_metrics, heuristic_metrics, inductive_metrics):
    algorithms = ['Alpha Miner', 'Heuristic Miner', 'Inductive Miner']
    metrics = ['Fitness', 'Precision', 'Simplicity', 'Generalization']
    
    # Creazione delle barre per ciascuna metrica
    values = [
        [alpha_metrics[0], heuristic_metrics[0], inductive_metrics[0]],  # Fitness
        [alpha_metrics[1], heuristic_metrics[1], inductive_metrics[1]],  # Precision
        [alpha_metrics[2], heuristic_metrics[2], inductive_metrics[2]],  # Simplicity
        [alpha_metrics[3], heuristic_metrics[3], inductive_metrics[3]]   # Generalization
    ]
    
    # Creazione del grafico
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        axes[i].bar(algorithms, values[i], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        axes[i].set_title(metric)
        axes[i].set_ylabel("Valore")
        axes[i].set_ylim(0, 1)  # Le metriche sono normalizzate tra 0 e 1
    
    plt.tight_layout()
    plt.suptitle("Comparazione delle Metriche per Algoritmi di Process Discovery", fontsize=14, y=1.02)
    plt.show()

# Funzione principale
if __name__ == "__main__":
    # Specifica il percorso del file XES
    file_path = "activitylog_uci_detailed_weekends.xes"  # Sostituisci con il percorso corretto
    
    # Caricamento del file di log
    log = load_xes_log(file_path)
    
        # Scoperta con Alpha Miner
    alpha_net, alpha_initial, alpha_final = alpha_miner_discovery(log)
    alpha_metrics = evaluate_model(log, alpha_net, alpha_initial, alpha_final)
    
    # Scoperta con Heuristic Miner
    heuristic_net, heuristic_initial, heuristic_final = heuristic_miner_discovery(log)
    heuristic_metrics = evaluate_model(log, heuristic_net, heuristic_initial, heuristic_final)
    
    # Scoperta con Inductive Miner
    inductive_net, inductive_initial, inductive_final = inductive_miner_discovery(log)
    inductive_metrics = evaluate_model(log, inductive_net, inductive_initial, inductive_final)
    
    # Visualizzazione delle metriche con grafici
    plot_metrics(alpha_metrics, heuristic_metrics, inductive_metrics)
