import cv2
import numpy as np
from skimage.metrics import mean_squared_error

img1 = cv2.imread('known_people/Anthony.jpg') 
img2 = cv2.imread('known_people/Laura.jpg')

img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) 
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

mse = mean_squared_error(img1_gray, img2_gray)

print("MSE value:", mse)
diff = np.abs(img1_gray - img2_gray)

cv2.imshow('Difference', diff) 
cv2.waitKey(0) 
cv2.destroyAllWindows()