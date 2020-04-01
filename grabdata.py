import numpy as np
import cv2
import time
from grabscreen import grab_screen
from getkeys import key_check
import os

w = [1,0,0]
s = [0,1,0]
a = [0,0,1]


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0,0,0]

    if 'W' in keys:
        output = w
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    return output

def checkScreen():
    while True:
        screen = grab_screen(region=(8,30,808,630))
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) == ord('q'):
            cv2.destroyAllWindows()
            break
        
        keys = key_check()
        if 'Q' in keys:
            training_data = training_data[0:-500]
            print('Last 500 frames scrapped\n')

def main():


    n = int(input('Enter the batch number: '))
    file_name = 'training_data_{}.npy'.format(n)

    # Press Q if game is in screen
    checkScreen()

    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name))
    else:
        print('File does not exist, starting fresh!')
        training_data = []
    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)


    if os.path.isfile(file_name):
        print('Existing Training Data:' + str(len(training_data)))
        print('Capturing Data!')
    else:
        print('Capturing Data Freshly!')

    paused = False
    while True:

        if not paused:
            screen = grab_screen(region=(8, 30, 808, 630))
            screen = cv2.resize(screen, (480, 270))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])


            if len(training_data) % 500 == 0:
                print('New Training Data: ' + str(len(training_data)))
                print('Saving Data!')
                np.save(file_name, training_data)
                print('Data saved succesfully! You can quit now.')
                print('Capturing data!')

        keys = key_check()

# Pausing

        if 'T' in keys:
            if paused:
                paused = False
                print('Unpaused!')
                time.sleep(1)
                print('Capturing Data!')
            else:
                paused = True
                print('Paused!')
                time.sleep(1)

    # Scratch last data
        if 'Q' in keys:
            training_data = training_data[0:-500]
            print('Last 500 frames scrapped\n')

main()
