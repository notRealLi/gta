from PIL import ImageGrab
import cv2
import numpy as np

while(True):
    screen = ImageGrab.grab(bbox=(0, 40, 800, 600))
    screen_np = np.array(screen)
    screen_np_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image', screen_np_gray)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


