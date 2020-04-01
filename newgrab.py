import numpy as np
import cv2
import time
from grabscreen import grab_screen
from getkeys import key_check
import os

a = [1,0,0]
w = [0,1,0]
d = [0,0,1]

starting_value = 1

def keys_to_output(keys):

    output = [0, 0, 0]

    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1

    return output


def checkScreen():
    while True:
        screen = grab_screen(region=(8,30,808,630))
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) == ord('q'):
            cv2.destroyAllWindows()
            break

while True:
    file_name = 'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        
        break

def main(file_name,starting_value):

    # Press Q if game is in screen
    file_name = file_name
    starting_value = starting_value


    # n = int(input('Enter the batch number: '))
    file_name = 'training_data_{}.npy'.format(starting_value)
    training_data = []

    # checkScreen()

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while True:

        if not paused:
            screen = grab_screen(region=(8, 30, 808, 630))
            screen = cv2.resize(screen, (200, 150))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])

            if len(training_data) % 100 == 0:
                print(len(training_data))
                
                if len(training_data) == 500:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = 'training_data_{}.npy'.format(starting_value)

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
        if 'G' in keys:
            training_data = []
            print('Last 500 frames scrapped\n')

main(file_name,starting_value)
