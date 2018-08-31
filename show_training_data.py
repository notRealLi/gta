import numpy as np
import cv2
import utils
filename = utils.training_filename

training_data = np.load(filename)

for frame in training_data:
    cv2.imshow('training footage', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
