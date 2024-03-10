from PROJ_header import *
from PROJ_mouvements import *
from PROJ_image import *

def main():
    
    rawCapture, frameSource = init_camera()
    camera.start_preview()

    i = 6
    take = False
    while(True):
        i+=1
        image = prendre_photo(frameSource)
        if input() == "k":
            cv2.imwrite("raw"+format(i)+".png", image)
        #cv2.imshow("raw"+format(i), image)
        cv2.imshow("raw", image)
        cv2.waitKey(1)
        rawCapture.truncate(0)
    
main()