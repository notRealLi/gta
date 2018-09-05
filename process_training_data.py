import numpy as np
import cv2
import utils
filename = 'data/test_data.npy'

def region_of_interest(img):
    return

training_data = np.load(filename)

for frame in training_data:
    frame = cv2.resize(frame, (800, 640))
    frame = cv2.Canny(frame, 40, 80) # TODO: learn; tweak min and max
    cv2.line(frame, (230,220), (570,220), 255, 5)
    cv2.line(frame, (0,640),   (800,640), 255, 5)
    cv2.line(frame, (0,640),   (0,440), 255, 5)
    cv2.line(frame, (800,640), (800,440), 255, 5)
    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
