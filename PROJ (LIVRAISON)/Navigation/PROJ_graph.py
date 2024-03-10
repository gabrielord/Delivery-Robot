import networkx as nx
from Navigation.PROJ_robot import *
from queue import Queue

def createGrid():
    # Création des graphes
    G = nx.Graph()

    # Ajout des nœuds
    for i in range(1, 26):
        G.add_node(i)

    # Ajout des arêtes pour former un carré
    for i in range(1, 6):
        for j in range(1, 6):
            node1 = (i - 1) * 5 + j
            node2 = node1 + 1
            node3 = node1 + 5

            if j < 5:
                G.add_edge(node1, node2)
            if i < 5:
                G.add_edge(node1, node3)
    return G            
    
# Fonction pour supprimer une arête
def remove_edge(node1, node2, G):
    if G.has_edge(node1, node2):
        G.remove_edge(node1, node2)
        # print(G.edges())
        print("L'arete entre ", node1," et ",node2," a ete supprime.")
    else:
        print("L'arete entre",node1," et ",node2," n'existe pas dans le graphe.")

def shortest_path(source, target, initial_direction, atTheNode, G):
    global_path = [source, initial_direction]
    try:
        moves = Queue()  # Queue to store moves between nodes
        if atTheNode:
            moves.put(initial_direction)
        
        if initial_direction == "Nord":
            next_node = source + 5
        elif initial_direction == "L'est":
            next_node = source + 1
        elif initial_direction == "L'oest":
            next_node = source - 1
        else:
            next_node = source - 5
            
        if atTheNode:
            path = [source] + nx.shortest_path(G, source=next_node, target=target)
        else:
            path = [source] + nx.shortest_path(G, source=source, target=target)
        
        if len(path) >= 2:
            global_path[0] = path[0]
            global_path[1] = path[1]

        if atTheNode:
            p=1
        else:
            p=1 

        move = ""
        for i in range(p,len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]

            # Determine moves based on the difference in node indices
            
            if next_node - current_node == 1:
                move = "L'est"
            elif next_node - current_node == -1:
                move = "L'oest"
            elif next_node - current_node == 5:
                move = "Nord"
            elif next_node - current_node == -5:
                move = "Sud"
            elif next_node - current_node == 0:
                move = initial_direction

            moves.put(move)
        if len(path) > 2:
            moves.put(move)
        print("Le meilleur itineraire entre ", source," et ", target, " est : ", path)
        return moves, path

    except nx.NetworkXNoPath:
        print("Aucun itineraire entre ",source," et ",target," n'a ete trouve.")
        return None
