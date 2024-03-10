from PROJ_header import *
from image_functions import*

def init_camera():
    global camera
    camera.resolution = CAMERA_RESOLUTION
    #camera.mode = CAMERA_MODE
    rawCapture = PiRGBArray(camera,size=camera.resolution)
    frameSource = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
    return (rawCapture,frameSource)

def prendre_photo(frameSource):
    
    #my_file = open('tmp.jpg', 'wb')
    ##sleep(1)
    #image = camera.capture(my_file)
    ## At this point my_file.flush() has been called, but the file has
    ## not yet been closed
    #my_file.close()
    #image = cv2.imread("tmp.jpg")
    
    #sleep(0.1)
    frame = next(frameSource)
    image = frame.array
    
    return image

def ligneDetection(image):
    gray_image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(6, 6))
    clahe_img = clahe.apply(gray_image)
    # equalized_img = cv2.equalizeHist(clahe_img)

    # Define a linear contrast adjustment function
    def adjust_contrast(image, factor):
        return np.clip(image * factor, 0, 255).astype(np.uint8)

    # Set the contrast adjustment factor (adjust as needed)
    contrast_factor = 0.98

    # Apply the contrast adjustment
    blur = adjust_contrast(clahe_img, contrast_factor)

    hsv = cv2.cvtColor(cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 140])
    upper_white = np.array([172, 110, 255])

    # Create a binary mask based on the threshold
    mask = cv2.inRange(hsv, lower_white, upper_white)

    kernel_dilate = np.ones((4, 4), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel_dilate, iterations=1)

    kernel_erode = np.ones((12, 12), np.uint8)
    eroded_mask = cv2.erode(dilated_mask, kernel_erode, iterations=2)

    # plot_image(eroded_mask)
    kernel_erode = np.ones((5, 5), np.uint8)
    eroded_mask = cv2.erode(eroded_mask, kernel_erode, iterations=2)

    #plot_image(eroded_mask)
    kernel_dilate = np.ones((8, 8), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

    # Find the different contours
    (im2, contours, hierarchy) = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #im2 = dilated_mask
    # Sort by area (keep only the biggest one)

    #cv2.imwrite('out_test.png', im2)
    #print (len(contours))
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    if len(contours) > 0:
        M = cv2.moments(contours[0])
        # Centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print("Centroid of the biggest area: ({}, {})".format(cx, cy))
        return (True, cx, cy)
    else:
        return (False, 0, 0)

def ligneDetection_copy(image):
    # Input Image
    h, w = image.shape[:2]
    #print (w,h)

    # Convert to HSV color space
    blur = cv2.blur(image,(5,5))
    #ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    ret,thresh1 = cv2.threshold(blur,168,255,cv2.THRESH_BINARY)
    hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)

    # Define range of white color in HSV
    lower_white = np.array([0, 0, 168]) #168 é bom para o dia
    upper_white = np.array([172, 111, 255])
    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower_white, upper_white)
    #cv2.imwrite('out_test.png', mask)
    # Remove noise
    kernel_erode = np.ones((6,6), np.uint8)

    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((4,4), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

    # Find the different contours
    (im2, contours, hierarchy) = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #im2 = dilated_mask
    # Sort by area (keep only the biggest one)

    #cv2.imwrite('out_test.png', im2)
    #print (len(contours))
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    if len(contours) > 0:
        M = cv2.moments(contours[0])
        # Centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print("Centroid of the biggest area: ({}, {})".format(cx, cy))
        return (True, cx, cy)
    else:
        return (False, 0, 0)
    
def detect_corners(img):
    gray_image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(6, 6))
    clahe_img = clahe.apply(gray_image)
    # equalized_img = cv2.equalizeHist(clahe_img)

    # Define a linear contrast adjustment function
    def adjust_contrast(image, factor):
        return np.clip(image * factor, 0, 255).astype(np.uint8)

    # Set the contrast adjustment factor (adjust as needed)
    contrast_factor = 0.98

    # Apply the contrast adjustment
    blur = adjust_contrast(clahe_img, contrast_factor)

    hsv = cv2.cvtColor(cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 140])
    upper_white = np.array([172, 110, 255])

    # Create a binary mask based on the threshold
    mask = cv2.inRange(hsv, lower_white, upper_white)

    kernel_dilate = np.ones((4, 4), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel_dilate, iterations=1)

    kernel_erode = np.ones((12, 12), np.uint8)
    eroded_mask = cv2.erode(dilated_mask, kernel_erode, iterations=2)

    # plot_image(eroded_mask)
    kernel_erode = np.ones((4, 4), np.uint8)
    eroded_mask = cv2.erode(eroded_mask, kernel_erode, iterations=2)

    #plot_image(eroded_mask)
    kernel_dilate = np.ones((8, 8), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

    # Find the different contours
    im2, contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Select the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a mask of the largest contour
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

    # plot_image(mask)

    # Apply edge detection (if necessary)
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    # plot_image(edges)
    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=50)

    list_a = []
    
    try:
    
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            list_a.append(abs(a))
            # b = np.sin(theta)
            # x0 = a * rho
            # y0 = b * rho
            # x1 = int(x0 + 1000 * (-b))
            # y1 = int(y0 + 1000 * (a))
            # x2 = int(x0 - 1000 * (-b))
            # y2 = int(y0 - 1000 * (a))
            # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return (max(list_a) - min(list_a) >= 0.2)
    except:
        return False


def LigneAndCornerDetection(img, debug=False):
    ligneDetected = False
    cornerDetected = False
    Cx = 0
    a = 0

    if debug:
        plot_image(img, name='Originale')

    ## Traitement des Images
    gray_image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(6, 6))
    clahe_img = clahe.apply(gray_image)
    # equalized_img = cv2.equalizeHist(clahe_img)

    # Define a linear contrast adjustment function
    def adjust_contrast(image, factor):
        return np.clip(image * factor, 0, 255).astype(np.uint8)

    # Set the contrast adjustment factor (adjust as needed)
    contrast_factor = 0.98


    # Apply the contrast adjustment
    contrast_img = adjust_contrast(clahe_img, contrast_factor)
    if debug:
        plot_image(contrast_img, name='Blur')
    
    blur = cv2.GaussianBlur(contrast_img, (3,3), cv2.BORDER_DEFAULT)
    
    
    
    if debug:
        plot_image(blur, name='Blur')
    
    hsv = cv2.cvtColor(cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 150])
    upper_white = np.array([172, 110, 255])

    # Create a binary mask based on the threshold
    mask = cv2.inRange(hsv, lower_white, upper_white)

    kernel_dilate = np.ones((4, 4), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel_dilate, iterations=1)

    kernel_erode = np.ones((12, 12), np.uint8)
    eroded_mask = cv2.erode(dilated_mask, kernel_erode, iterations=2)

    # plot_image(eroded_mask)
    kernel_erode = np.ones((5, 5), np.uint8)
    eroded_mask = cv2.erode(eroded_mask, kernel_erode, iterations=2)

    ##plot_image(eroded_mask)
    #kernel_dilate = np.ones((8, 8), np.uint8)
    #dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

    if debug:
        plot_image(eroded_mask, name='Eroded')

    # Find the different contours
    im2, contours, hierarchy = cv2.findContours(eroded_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    if len(contours) > 0:
        # Select the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        #print(type(M))
        # Centroid
        #print(M['m00'])
        #print(M['m10'])
        try: 
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            ligneDetected = True
            Cx=cx
        except Exception as e:
            mask = np.zeros_like(img)
            cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)
            cv2.imwrite("MNulo.png", mask)
            print(e)
            ligneDetected = False 
        #print("Centroid of the biggest area: ({}, {})".format(cx, cy))
        
    else:
        print("tem contorno")
        ligneDetected = False
        return ligneDetected, cornerDetected, Cx, a

    #print(ligneDetected) #####
    
    # Create a mask of the largest contour
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

    #plot_image(mask)
    if debug:
        plot_image(mask, name='Mask')

    # Apply edge detection (if necessary)
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    # plot_image(edges)
    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if debug:
        plot_image(edges, name='Edges')

    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=50)

    list_a = []
    try:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            list_a.append(a)
            if(debug):
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        maxA = max(np.abs(list_a))
        cornerDetected = (maxA - min(np.abs(list_a)) >= 0.2) or maxA <= 0.4
        a = np.mean(list_a)
    except Exception as e:
        print("O erro é: ", e)
        #ligneDetected = False
        a = 1
        return ligneDetected, cornerDetected, Cx, a
    
    #print("dentro2")
    #print(ligneDetected) #####
    if debug:
        plot_image(img, name='Lines')
    return ligneDetected, cornerDetected, Cx, a
    
