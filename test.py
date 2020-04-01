from grabscreen import grab_screen
from directkeys import PressKey,ReleaseKey, W, A, S, D
from getkeys import key_check
from collections import deque, Counter
import random
from statistics import mode,mean
import numpy as np
import time
import cv2
import numpy as np

from random import shuffle
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.applications.inception_v3 import decode_predictions
from keras.models import Model
from keras.layers import Dense, Activation, Flatten, Dropout, GlobalAveragePooling2D
from keras.preprocessing import image
from keras.models import load_model


GAME_WIDTH = 800
GAME_HEIGHT = 600

WIDTH = 86
HEIGHT = 56
LR = 1e-3
EPOCHS = 10

def straight():
    print('straight')
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    print('left')
    PressKey(W)
    PressKey(A)
    time.sleep(0.09)
    ReleaseKey(A)


def right():
    print('right')
    PressKey(W)
    PressKey(D)
    time.sleep(0.09)
    ReleaseKey(D)



# base_model = InceptionV3(weights='imagenet', include_top=False)
# x = base_model.output
# # x = Flatten()(x)
# x = GlobalAveragePooling2D()(x)
# x = Dense(256,activation='relu')(x)
# x = Dropout(0.5)(x)
# prediction = Dense(9, activation='softmax')(x)
# model = Model(inputs=base_model.input, outputs=prediction)
# for layer in base_model.layers:
#   layer.trainable = False
model = load_model('testmodel.h5')

def main():
    last_time = time.time()
    
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
        
    paused = False
    mode_choice = 0
    while(True):
            
        if not paused:
            screen = grab_screen(region=(8,30,GAME_WIDTH+8,GAME_HEIGHT+30))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            last_time = time.time()
            screen = cv2.resize(screen, (200,150))
            screen = np.asarray(screen)
            prediction = model.predict([screen.reshape(1,200,150,3)])[0]
            prediction = np.array(prediction) * [0.009, 5, 0.009]
            mode_choice = np.argmax(prediction)

            if mode_choice == 0:
                left()
                choice_picked = 'left'
                
            elif mode_choice == 1:
                straight()
                choice_picked = 'straight'
                
            elif mode_choice == 2:
                right()
                choice_picked = 'right'

            print(choice_picked)
        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

main()


