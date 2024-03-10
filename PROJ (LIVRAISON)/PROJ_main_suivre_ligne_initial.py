from PROJ_header import *
from PROJ_mouvements import *
from PROJ_image import *



def main():
    
    connect_to_arduino()
    camera.start_preview()
    rawCapture, frameSource = init_camera()

    

    for _ in range(0,500):
        debut = time.time()
        image = prendre_photo(frameSource)
        detected, cx, cy = ligneDetection(image)
        fin = time.time()
        print("processing time = ", fin - debut)
        rawCapture.truncate(0)
        
        if cx< MAX_WIDTH//2 + tolerance and cx > MAX_WIDTH //2 - tolerance:
            cx = MAX_WIDTH//2
        print(cx)
        if(detected == False):
            print("LIGNE PAS DETECTEE")
        else:
            marcher(int(gain*(MAX_PUISSANCE-BASE_PUISSANCE)*(1-cx/MAX_WIDTH))+BASE_PUISSANCE, int(gain*(MAX_PUISSANCE-BASE_PUISSANCE)*(cx/MAX_WIDTH))+BASE_PUISSANCE)
        
    print('stop motors')
    write_order(serial_file, Order.STOP)
    camera.stop_preview()

main()


    