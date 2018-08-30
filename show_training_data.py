import numpy as np
import cv2
import pickle

training_file = open('training_data.pickle', 'rb')
training_data = pickle.load(training_file)

for frame in training_data:
    cv2.imshow('training footage', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
