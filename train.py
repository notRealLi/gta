from PIL import ImageGrab
import cv2
import numpy as np
import os.path
from utils import test_filename, training_filename, timer, time_now
from image_processing import process_image
filename = test_filename

if os.path.isfile(filename):
    training_data = list(np.load(filename))
else:
    training_data = []

timer(1)

last_time = time_now()
frame_count = 0
while(True):
    frame = ImageGrab.grab(bbox=(0, 40, 800, 600))
    frame = np.array(frame)
    processed_frame = process_image(frame)

    cv2.imshow('image', processed_frame)

    processed_frame = cv2.resize(processed_frame, (80, 64))
    training_data.append(processed_frame)
    
    frame_count += 1
    if frame_count == 20:
        avg_time_elapsed = (time_now() - last_time) / 20
        print('FPS: ' + str(int(1/avg_time_elapsed)))
        last_time = time_now()
        frame_count = 0

    if cv2.waitKey(20) & 0xFF == ord('q'): #?
        np.save(filename, training_data)
        cv2.destroyAllWindows()
        break

