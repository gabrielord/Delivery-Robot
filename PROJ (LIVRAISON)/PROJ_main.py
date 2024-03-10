from PROJ_header import *
from PROJ_mouvements import *
from PROJ_image import *
from Navigation.PROJ_graph import *
from Navigation.PROJ_robot import *

## CONSTANTS
gainInclination = 0.0
debug = True
suivreHuit = False
delayCarrefour=1

## Global Variables
moves, path, path_index = None, None, 0
count_loops_obstacle = 0
coutCarrefour = 0

def navigationObstacleManagement(robot, final_node, G):
    global moves, path, path_index
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

def navigationCarrefourManagement(robot):
    global moves, path, path_index
    # increase the path_index
    path_index += 1
    ("s")
    # see what is the next direction
    next_direction = moves.get()
    # calculate the turn based on the current and on the next direction
    next_turn = robot.get_next_turn(next_direction=next_direction)
    # update robot (future preview)
    robot.node = path[path_index]
    robot.direction = next_direction
    print("Last carrefour: ",robot.node)
    return next_turn

def obstacleManagement(robot, final_node, G):
    global count_loops_obstacle 
    distanceObstacle = lectureDistance()
    if(distanceObstacle < distanceLimite and distanceObstacle > 3):
        count_loops_obstacle += 1
        ## Obstacle Detecté
        if count_loops_obstacle == 2:
            print("OBSTACLE DETECTED")
            #write_order(serial_file, Order.STOP)
            count_loops_obstacle = 0
            marcher(0,0)
            tournerFixe("droit", 100, 180)
            navigationObstacleManagement(robot, final_node, G)
    
def LigneManagement(cx, a):
    if cx< MAX_WIDTH//2 + tolerance and cx > MAX_WIDTH //2 - tolerance:
        cx = MAX_WIDTH//2
    def transf(a):
        if(a<0):
            return -a-1
        else:
            return -a+1
    factor = cx/MAX_WIDTH + transf(a)*gainInclination
    puissanceR = min(100, int(gain*(MAX_PUISSANCE-BASE_PUISSANCE)*(1-factor))+BASE_PUISSANCE)
    puissanceL = min(100, int(gain*(MAX_PUISSANCE-BASE_PUISSANCE)*(factor))+BASE_PUISSANCE)
    marcher(puissanceR, puissanceL)
    
def getInitialInfo():
    # Get input from the user through the terminal
    Depart = int(input("Départ: "))
    Arrivee = int(input("Arrivée: "))
    Orientation = input("Orientation du véhicule (Nord/Sud/L'est/L'oest): ")
    return Orientation, Depart, Arrivee


def main():
    global moves, path, path_index
    carrefourMoment = 0
    cornerRedundance = False

    ## Initializing
    connect_to_arduino()
    print("CONNECTED")
    camera.start_preview()
    rawCapture, frameSource = init_camera()
    print("CAMERA INITIATED")
    
    initial_direction, initial_node, final_node = getInitialInfo()

    ## Initialization du chemin
    G = createGrid()
    ###### Primera volta
    moves, path = shortest_path(initial_node, final_node, initial_direction, atTheNode=True, G=G)
    path_index = 0
    robot = Robot(initial_direction=moves.get(), initial_node=path[path_index], final_node=final_node)

    # detectedCarrefour = False
    # detectedObstacle = False
    
    
    while robot.node != final_node:
        # Obstacle
        obstacleManagement(robot, final_node, G)
        
        ## Camera
        image = prendre_photo(frameSource)

        ## Processing de l'image
        #debut = time.time() #DEBUG
        detectedLigne, detectedCorner, cx, a = LigneAndCornerDetection(image, debug)
        #fin = time.time() #DEBUG
        #print("processing time = ", fin - debut) #DEBUG
        rawCapture.truncate(0)

        ### Carrefour
        #if(detectedCorner == True):
        #    print("CARREFOUR DETECTE")
        #    if(suivreHuit == False and cornerRedundance == True):
        #        # O QUE FAZER NO CARREFOUR
        #        tournerPasFixe("gauche", 100, 90)
        #        #marcher(0,0)
        #        #sleep(10)
        #    else:
        #       marcher(0,0)
        #    cornerRedundance = not cornerRedundance
        if(detectedCorner == True and (time.time() - carrefourMoment) > delayCarrefour):
            countCarrefour +=1
            marcher(0,0)
            print("CARREFOUR DETECTE")
            if(suivreHuit == False and countCarrefour == 2):
                # O QUE FAZER NO CARREFOUR
                next_turn = navigationCarrefourManagement(robot)
                print("Virar para :", next_turn)
                if next_turn == "Droite" or next_turn == "Gauche":
                    tournerPasFixe(next_turn.lower(), 100, 90)
                elif next_turn == "Retour":
                    tournerFixe("droit", 100, 180)
                else:
                    carrefourMoment = time.time()
                countCarrefour = 0
                #marcher(0,0)
                #sleep(10)
                
        ## Suivre Ligne
        elif(detectedLigne == True):
            cornerRedundance = False
            countCarrefour = 0
            LigneManagement(cx, a)
            
        else:
            countCarrefour = 0
            cornerRedundance = False
            print("LIGNE PAS DETECTEE")

    print("ARRIVE")
    print('stop motors')
    marcher(0,0)
    sleep(2)
    ## Segunda volta
    
    tournerFixe("droit", 100, 180)
    navigationObstacleManagement(robot, final_node, G)
    
    moves, path = shortest_path(robot.node, initial_node, robot.direction, atTheNode=True, G=G)
    path_index = 0
    robot = Robot(initial_direction=moves.get(), initial_node=path[path_index], final_node=initial_node)

    # detectedCarrefour = False
    # detectedObstacle = False
    
    
    while robot.node != initial_node:
        # Obstacle
        obstacleManagement(robot, final_node, G)
        
        ## Camera
        image = prendre_photo(frameSource)

        ## Processing de l'image
        #debut = time.time() #DEBUG
        detectedLigne, detectedCorner, cx, a = LigneAndCornerDetection(image, debug)
        #fin = time.time() #DEBUG
        #print("processing time = ", fin - debut) #DEBUG
        rawCapture.truncate(0)

        ### Carrefour
        #if(detectedCorner == True):
        #    print("CARREFOUR DETECTE")
        #    if(suivreHuit == False and cornerRedundance == True):
        #        # O QUE FAZER NO CARREFOUR
        #        tournerPasFixe("gauche", 100, 90)
        #        #marcher(0,0)
        #        #sleep(10)
        #    else:
        #       marcher(0,0)
        #    cornerRedundance = not cornerRedundance
        if(detectedCorner == True and (time.time() - carrefourMoment) > delayCarrefour):
            countCarrefour +=1
            marcher(0,0)
            print("CARREFOUR DETECTE")
            if(suivreHuit == False and countCarrefour == 2):
                # O QUE FAZER NO CARREFOUR
                next_turn = navigationCarrefourManagement(robot)
                print("Virar para :", next_turn)
                if next_turn == "Droite" or next_turn == "Gauche":
                    tournerPasFixe(next_turn.lower(), 100, 90)
                elif next_turn == "Retour":
                    tournerFixe("droit", 100, 180)
                else:
                    carrefourMoment = time.time()
                countCarrefour = 0
                #marcher(0,0)
                #sleep(10)
                
        ## Suivre Ligne
        elif(detectedLigne == True):
            cornerRedundance = False
            countCarrefour = 0
            LigneManagement(cx, a)
            
        else:
            countCarrefour = 0
            cornerRedundance = False
            print("LIGNE PAS DETECTEE")

    print("ARRIVE")
    print('stop motors')
    marcher(0,0)
    camera.stop_preview()
    
main()


    