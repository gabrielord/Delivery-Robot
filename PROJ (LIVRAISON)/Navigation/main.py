from PROJ_graph import * 
from PROJ_robot import *
# 5 is the initial node and 4 is the next one, to help with the orientation

# Get input from the user through the terminal
Depart = int(input("Départ: "))
Arrivee = int(input("Arrivée: "))
Orientation = input("Orientation du véhicule (Nord/Sud/L'est/L'oest): ")

initial_direction, initial_node, final_node = Orientation, Depart, Arrivee, 

# Création des graphes
G = createGrid()

## Comentei e não deu ruim
#remove_flag = False

## Initialization du chemin
moves, path = shortest_path(initial_node, final_node, initial_direction,atTheNode=True, G=G)

path_index = 0

robot = Robot(initial_direction=moves.get(), initial_node=path[path_index], final_node=final_node)

detectedCarrefour = False
detectedObstacle = False

def navigationObstacleManagement():
    global moves
    global path
    global path_index
    # calculate before which node the obstacle is
    nextNode = robot.getNextNode()
    # delete the edge
    remove_edge(robot.node, nextNode, G)
    # calculate the new direction
    robot.directionHalfTurn()
    # print(G)
    # calculate the new path
    print(robot.node)
    moves, path = shortest_path(robot.node, final_node, robot.direction, atTheNode=False, G=G)   
    path_index = 0     

def navigationCarrefourManagement():
    global path_index
    global moves
    # increase the path_index
    path_index += 1
    # see what is the next direction
    next_direction = moves.get()
    # calculate the turn based on the current and on the next direction
    next_turn = robot.get_next_turn(next_direction=next_direction)
    # update robot (future preview)
    robot.node = path[path_index]
    robot.direction = next_direction
    return next_turn

while robot.node != final_node:
    print("Actual node: ",robot.node, "\n", "Actual Direction: " ,robot.direction)
    question = input("Le prochain nœud du chemin est-il disponible? (Oui/Non): ")
    if question.lower() == 'oui':
        detectedObstacle = False
    elif question.lower() == 'non':
        detectedObstacle = True

    if detectedObstacle:
        print("\nOBSTACLE DETECTED")
        # demitourne() <---------------
        navigationObstacleManagement()
        
    elif detectedCarrefour:
        print("\nCARREFOUR DETECTED")
        next_turn = navigationCarrefourManagement()
        print("Virar para :", next_turn)
         # tourne(next_turn)<-------
        detectedCarrefour = False

    else:
        print("Andando na aresta...")
        detectedCarrefour = True
        
    #if robot.node == 11:
    #    detectedObstacle = True