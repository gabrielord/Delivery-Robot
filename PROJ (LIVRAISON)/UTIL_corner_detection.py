import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_functions import *

#expected_corners = 3
filename = "./codes_arch/PROJ/raw/raw44.png"
# Example using OpenCV
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(6, 6))
clahe_img = clahe.apply(img)
equalized_img = cv2.equalizeHist(clahe_img)

plot_image(equalized_img)

# Criar uma máscara do mesmo tamanho que a imagem
mascara = np.zeros(equalized_img.shape[:2], dtype=np.uint8)

# Definir a região que você deseja iluminar na máscara (por exemplo, um retângulo branco)
cv2.rectangle(mascara, (100, 100), (200, 200), (255), thickness=cv2.FILLED)

# Adicionar a máscara à imagem original
imagem_iluminada = cv2.add(equalized_img, np.zeros_like(equalized_img), mask=mascara)

plot_image(imagem_iluminada)

blur = cv2.medianBlur(equalized_img, 5)

plot_image(blur)

hsv = cv2.cvtColor(cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2HSV)
# plot_image(hsv)

lower_white = np.array([0, 0, 170])
upper_white = np.array([172, 110, 255])

# Create a binary mask based on the threshold
mask = cv2.inRange(hsv, lower_white, upper_white)
plot_image(mask)

kernel_dilate = np.ones((3, 3), np.uint8)
dilated_mask = cv2.dilate(mask, kernel_dilate, iterations=1)

# plot_image(dilated_mask)

kernel_erode = np.ones((12, 12), np.uint8)
eroded_mask = cv2.erode(dilated_mask, kernel_erode, iterations=2)

plot_image(eroded_mask)
kernel_erode = np.ones((4, 4), np.uint8)
eroded_mask = cv2.erode(eroded_mask, kernel_erode, iterations=2)

#plot_image(eroded_mask)
#kernel_dilate = np.ones((8, 8), np.uint8)
#dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

# gray = np.float32(eroded_mask)
# plot_image(gray)

# Find the different contours
contours, hierarchy = cv2.findContours(eroded_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# Sort by area (keep only the biggest one)
#im2 = dilated_mask.copy()
#im2 = cv2.drawContours(im2, contours, -1, (0, 255, 0), 3)
#plot_image(im2)

# Select the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Create a mask of the largest contour
mask = np.zeros_like(img)
cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

plot_image(mask)

# Apply edge detection (if necessary)
edges = cv2.Canny(mask, 50, 150, apertureSize=3)
plot_image(edges)
# contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Use Hough Line Transform to detect lines
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=50)

list_a = []

for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    list_a.append(abs(a))
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

print(max(list_a) - min(list_a) >= 0.2)
print(list_a)

plot_image(img)

#intersections = []

# for i in range(len(lines)):
#     for j in range(i + 1, len(lines)):
#         rho1, theta1 = lines[i][0]
#         rho2, theta2 = lines[j][0]

#         # Solve for intersection point
#         A = np.array([[np.cos(theta1), np.sin(theta1)],
#                       [np.cos(theta2), np.sin(theta2)]])
#         b = np.array([rho1, rho2])
#         intersection = np.linalg.solve(A, b)

#         # Check if the intersection point is within the image boundaries
#         if 0 <= intersection[0] < img.shape[1] and 0 <= intersection[1] < img.shape[0]:
#             intersections.append((int(intersection[0]), int(intersection[1])))