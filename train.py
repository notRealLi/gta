from PIL import ImageGrab
import cv2
import numpy as np
import time
import os.path
import utils
filename = utils.test_filename

def process_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges_image = cv2.Canny(gray_image, threshold1=200, threshold2=300) # TODO: learn; tweak min and max

    vertices = np.array([[0,640], [800,640], [800,350], [570,200], [230,200], [0,350]])
    roi_image = religion_of_interest(image=edges_image, vertices=[vertices])

    lines = cv2.HoughLinesP(roi_image, 1, np.pi/180, 180, 20, 15)
    try:
        for line in lines:
            coords = line[0]
            cv2.line(roi_image, (coords[0], coords[1]), (coords[2], coords[3]), 255, 3)
    except Exception as e:
        print(e)
        pass

    return roi_image

def religion_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    
    return cv2.bitwise_and(mask, image)

##############################Script Starts##############################
last_time = time.time()
frame_count = 0
if os.path.isfile(filename):
    training_data = list(np.load(filename))
else:
    training_data = []

# for i in range(1,6)[::-1]:
#     print(i)
#     time.sleep(1)

while(True):
    frame = ImageGrab.grab(bbox=(0, 40, 800, 600))
    frame = np.array(frame)
    processed_frame = process_image(frame)

    cv2.imshow('image', processed_frame)

    processed_frame = cv2.resize(processed_frame, (80, 64))
    training_data.append(processed_frame)
    
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

