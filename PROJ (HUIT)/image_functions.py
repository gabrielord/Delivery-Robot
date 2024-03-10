import cv2
import numpy as np
#import matplotlib.pyplot as plt
#from mpldatacursor import datacursor

def plot_image(img, name='image'):
    cv2.imshow(name,img)
    if (name == 'image'):
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()
    else: 
        cv2.waitKey(1)

#def plot_image_cursor(img):
#    # Display the image
    # fig, ax = plt.subplots()
    # ax.imshow(img)
    # # Add data cursor to display pixel values on hover
    # datacursor(display='multiple', draggable=True, bbox=dict(alpha=1, fc='w'))
    # plt.show()