from PIL import ImageGrab
import cv2
import numpy as np
import time
import os.path
import utils
filename = utils.test_filename

def religion_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    
    return cv2.bitwise_and(mask, img)

last_time = time.time()
frame_count = 0
if os.path.isfile(filename):
    training_data = list(np.load(filename))
else:
    training_data = []

for i in range(1,6)[::-1]:
    print(i)
    time.sleep(1)

while(True):
    screen = ImageGrab.grab(bbox=(0, 40, 800, 600))
    screen_np = np.array(screen)
    screen_np_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    vertices = np.array([[0,640], [800,640], [800,300], [570,200], [230,200], [0,300]])
    screen_np_gray = religion_of_interest(img = screen_np_gray,vertices = [vertices])
    cv2.imshow('image', screen_np_gray)

    screen_np_gray = cv2.resize(screen_np_gray, (80, 64))
    training_data.append(screen_np_gray)
    
    frame_count += 1
    if frame_count == 20:
        avg_time_elapsed = (time.time() - last_time) / 20
        print('FPS: ' + str(int(1/avg_time_elapsed)))
        last_time = time.time()
        frame_count = 0

    if cv2.waitKey(20) & 0xFF == ord('q'): #?
        np.save(filename, training_data)
        cv2.destroyAllWindows()
        break

