from PROJ_header import *
from PROJ_mouvements import *
from PROJ_image import *

def main():
    connect_to_arduino()
    global distanceDunQuart
    tournerFixe("droit",100, 180)

main()