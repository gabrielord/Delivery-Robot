class Robot():
    """
    This class will create the direction that the robot must follow. For it, the turn command must be
    relative to the robot's current position.
    """
    def __init__(self, initial_direction:str, initial_node:str, final_node:str):
        self.direction = initial_direction
        self.node = initial_node
        self.final_node = final_node
    
    # l'entrée next_direction est la sortie l'algorithime de l'itinéraire
    def get_next_turn(self, next_direction):
        if self.direction == "Nord":
            if next_direction == "Nord":
                return None
            elif next_direction == "L'est":
                return "Droite"
            elif next_direction == "L'oest":
                return "Gauche"
            else:
                return "Retour"
                
        elif self.direction == "L'est":
            if next_direction == "Nord":
                return "Gauche"
            elif next_direction == "L'est":
                return None
            elif next_direction == "L'oest":
                return "Retour"
            else:
                return "Droite"
        
        elif self.direction == "L'oest":
            if next_direction == "Nord":
                return "Droite"
            elif next_direction == "L'est":
                return "Retour"
            elif next_direction == "L'oest":
                return None
            else:
                return "Gauche"
            
        else:
            if next_direction == "Nord":
                return "Retour"
            elif next_direction == "L'est":
                return "Gauche"
            elif next_direction == "L'oest":
                return "Droite"
            else:
                return None
                
    def directionHalfTurn(self):
        # faire le demi-tour
        if self.direction == "Nord":
            self.direction = "Sud"
        elif self.direction == "L'est":
            self.direction = "L'oest"
        elif self.direction == "L'oest":
            self.direction = "L'est"
        else:
            self.direction = "Nord"
            
    def getNextNode(self):
        if self.direction == "Nord":
            return self.node + 5
        elif self.direction == "L'est":
            return self.node + 1
        elif self.direction == "L'oest":
            return self.node - 1
        else:
            return self.node - 5