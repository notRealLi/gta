import time
training_filename = 'data/training_data.npy'
test_filename = 'data/test_data.npy'

def timer(seconds):
    for i in range(1,seconds+1)[::-1]:
        print(i)
        time.sleep(1)

def time_now():
    return time.time()