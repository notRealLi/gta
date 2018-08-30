from PIL import ImageGrab
import cv2
import numpy as np
import time

last_time = time.time()
frame_count = 0
while(True):
    screen = ImageGrab.grab(bbox=(0, 40, 800, 600))
    screen_np = np.array(screen)
    screen_np_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image', screen_np_gray)
    
    frame_count += 1
    if frame_count == 20:
        avg_time_elapsed = (time.time() - last_time) / 20
        print('The frame took ' + str(avg_time_elapsed) + ' s.')
        last_time = time.time()
        frame_count = 0

    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


