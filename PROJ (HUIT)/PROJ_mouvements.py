from PROJ_header import *

def marcher(puissanceR, puissanceL):
    global delay
    print("Moving forward at " + str(puissanceR) + ", " + str(puissanceL) + "%...")
    write_order(serial_file, Order.MOTOR)
    write_i8(serial_file, puissanceR) #valeur moteur droit
    write_i8(serial_file, puissanceL) #valeur moteur gauche
    time.sleep(delay)
    #print('stop motors')
    #write_order(serial_file, Order.STOP)
    #write_i8(serial_file, max(puissanceR//2,MIN_PUISSANCE)) #valeur moteur droit
    #write_i8(serial_file, max(puissanceL//2,MIN_PUISSANCE)) #valeur moteur gauche

## Donnee par la discipline
def lectureCodeurGauche():
    write_order(serial_file, Order.READENCODERl)
    while True:
       try:
           g = read_i16(serial_file)
           break
       except struct.error:
           pass
       except TimeoutError:
           write_order(serial_file, Order.READENCODERl)
           pass
    return g

## Donnee par la discipline
def lectureCodeurDroit():
    write_order(serial_file, Order.READENCODERr)
    while True:
       try:
           d = read_i16(serial_file)
           break
       except struct.error:
           pass
       except TimeoutError:
           write_order(serial_file, Order.READENCODERr)
           pass
    return d

def lectureDistance():
    write_order(serial_file, Order.READDISTANCE)
    while True:
       try:
           distance = read_i8(serial_file)
           break
       except struct.error:
           pass
       except TimeoutError:
           write_order(serial_file, Order.READENCODERr)
           pass
    return distance

def tournerPasFixe(direction, puissance, degrees):
    b = (1.8-2.5)/(100-80) #2.5 pour 80 et 1.8 pour 100
    a = 1.8 - 100*b
    correcteur = a + b*puissance  
    limiteCorrige = degrees * np.pi / 180 * 15 * correcteur #r=15cm
    
    if direction == "droit":
        coefL = 1
        coefR = 0
    else:
        coefL = 0
        coefR = 1

    ## debut du mouvement
    write_order(serial_file, Order.STOP)
    write_order(serial_file, Order.RESETENC)
    print("Forward " + direction + " at " + str(puissance) + "%...")
    write_order(serial_file, Order.MOTOR)
    write_i8(serial_file, puissance*coefR) #valeur moteur droit
    write_i8(serial_file, puissance*coefL) #valeur moteur gauche
    
    ## condition pour attendre
    instantActuel = time.time()
    if(coefL == 1):
        vitesseActuel = lectureCodeurGauche()
    else:
        vitesseActuel = lectureCodeurDroit() 
    distance = 0.0
    while (distance < limiteCorrige):
        instantPasse = instantActuel
        vitessePasse = vitesseActuel
        instantActuel = time.time()
        if(coefL == 1):
            vitesseActuel = lectureCodeurGauche()
        else:
            vitesseActuel = lectureCodeurDroit()  
        # integration numerique par trapeze
        #print(vitesseActuel) #########
        distance += (instantActuel-instantPasse)*(vitesseActuel+vitessePasse)/2

    ## Arret du mouvement
    print('stop motors')
    write_order(serial_file, Order.STOP)

def tournerFixe(direction, puissance, degrees):
    b = 0#(1.8-2.5)/(100-80) #2.5 pour 80 et 1.8 pour 100
    a = 0.9#1.8 - 100*b
    correcteur = a + b*puissance  
    limiteCorrige = degrees * np.pi / 180 * 15 * correcteur #r=10cm
    
    if direction == "droit":
        coefL = 1
        coefR = -1
    else:
        coefL = -1
        coefR = 1

    ## debut du mouvement
    write_order(serial_file, Order.STOP)
    write_order(serial_file, Order.RESETENC)
    print("Turn " + direction + " at " + str(puissance) + "%...")
    write_order(serial_file, Order.MOTOR)
    write_i8(serial_file, puissance*coefR) #valeur moteur droit
    write_i8(serial_file, puissance*coefL) #valeur moteur gauche
    
    ## condition pour attendre
    instantActuel = time.time()
    if(coefL == 1):
        vitesseActuel = lectureCodeurGauche()
    else:
        vitesseActuel = lectureCodeurDroit() 
    distance = 0.0
    while (distance < limiteCorrige):
        instantPasse = instantActuel
        vitessePasse = vitesseActuel
        instantActuel = time.time()
        if(coefL == 1):
            vitesseActuel = lectureCodeurGauche()
        else:
            vitesseActuel = lectureCodeurDroit()  
        # integration numerique par trapeze
        #print(vitesseActuel) #########
        distance += (instantActuel-instantPasse)*(vitesseActuel+vitessePasse)/2

    ## Arret du mouvement
    print('stop motors')
    write_order(serial_file, Order.STOP)

class Direction():
    """
    This class will create the direction that the robot must follow. For it, the turn command must be
    relative to the robot's current position.
    """
    def __init__(self, initial_direction:str):
        self.direction = initial_direction
        
    def turn(self, turn:str):
        if self.direction == "Nord":
            if turn == "droite":
                self.next_direction = "L'est"
            elif turn == "gauche":
                self.next_direction = "L'oest"
            elif turn == "retour":
                self.next_direction = "Sud"
        elif self.direction == "L'est":
            if turn == "droite":
                self.next_direction = "Sud"
            elif turn == "gauche":
                self.next_direction = "Nord"
            elif turn == "retour":
                self.next_direction = "L'oest"
        elif self.direction == "L'oest":
            if turn == "droite":
                self.next_direction = "Nord"
            elif turn == "gauche":
                self.next_direction = "Sud"
            elif turn == "retour":
                self.next_direction = "L'est"
        else:
            if turn == "droite":
                self.next_direction = "L'oest"
            elif turn == "gauche":
                self.next_direction = "L'est"
            elif turn == "retour":
                self.next_direction = "Nord"


def connect_to_arduino():
    global serial_file
    try:
        # Open serial port (for communication with Arduino)
        serial_file = open_serial_port(baudrate=BAUDRATE)
    except Exception as e:
        print('exception')
        raise e

    is_connected = False
    # Initialize communication with Arduino
    while not is_connected:
        print("Trying connection to Arduino...")
        write_order(serial_file, Order.HELLO)
        bytes_array = bytearray(serial_file.read(1))
        if not bytes_array:
            time.sleep(2)
            continue
        byte = bytes_array[0]
        if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
            is_connected = True

    time.sleep(2)
    c = 1
    while (c!=b''):
        c = serial_file.read(1)

