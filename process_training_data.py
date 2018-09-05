import numpy as np
import cv2
import utils
filename = 'data/test_data.npy'

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    mask = cv2.bitwise_and(mask, img)
    return mask

training_data = np.load(filename)

for frame in training_data:
    frame = cv2.resize(frame, (800, 640))
    frame = cv2.Canny(frame, 40, 80) # TODO: learn; tweak min and max
    vertices = np.array([[0,640], [800,640], [800,300], [570,200], [230,200], [0,300]])
    frame = region_of_interest(frame, [vertices])
    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
