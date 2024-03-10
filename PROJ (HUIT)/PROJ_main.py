from PROJ_header import *
from PROJ_mouvements import *
from PROJ_image import *

gainInclination = 0.0
debug = True
suivreLigne = True

countObstacle = 0

def ObstacleMenagement():
    global countObstacle
    distanceObstacle = lectureDistance()
    print(distanceObstacle)
    if(distanceObstacle < distanceLimite and distanceObstacle > 2):
        countObstacle += 1
        if countObstacle == 2:
            print("OBSTACLE DETECTED")
            ## Obstacle Detecté
            #write_order(serial_file, Order.STOP)
            marcher(0,0)
            tournerFixe("droit", 100, 180)
            countObstacle = 0
    else:
        countObstacle = 0

def LigneMenagement(cx, a):
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
    

def main():
    connect_to_arduino()
    camera.start_preview()
    rawCapture, frameSource = init_camera()

    while(True):
        ## Obstacle
        ObstacleMenagement()
        
        ## Camera
        image = prendre_photo(frameSource)

        ## Processing de l'image
        debut = time.time() #DEBUG
        detectedLigne, detectedCorner, cx, a = LigneAndCornerDetection(image, debug)
        #print(detectedLigne) #####
        fin = time.time() #DEBUG
        print("processing time = ", fin - debut) #DEBUG
        rawCapture.truncate(0)

        ## Carrefour
        if(detectedCorner == True):
            print("CARREFOUR DETECTE")
            if(suivreLigne == False):
                tournerPasFixe("droit", 100, 90)

        ## Suivre Ligne
        elif(detectedLigne == True):
            LigneMenagement(cx, a)
        else:
            print("LIGNE PAS DETECTEE")
        
    print('stop motors')
    write_order(serial_file, Order.STOP)
    camera.stop_preview()
    
main()


    