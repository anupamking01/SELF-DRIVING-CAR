import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle


# enter 1, then run the script again and enter 2, and keep incrementing it.
n = int(input("Enter the batch number: "))
train_data = np.load('training_data_{}.npy'.format(n),allow_pickle=True)

print('Training Data: ' + str(len(train_data)))
df = pd.DataFrame(train_data)
print(df.head())
print('\n')
print(Counter(df[1].apply(str)))
print('\n')

lefts = []
rights = []
forwards = []

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1, 0, 0]:
        lefts.append([img, choice])
    elif choice == [0, 1, 0]:
        forwards.append([img, choice])
    elif choice == [0, 0, 1]:
        rights.append([img, choice])
    else:
        print('no matches!!!')

if len(lefts) > len(rights):
    forwards = forwards[:len(rights)]
else:
    forwards = forwards[:len(lefts)]

lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

final_data = forwards + lefts + rights
shuffle(final_data)

print('Final Balanced Data: ' + str(len(final_data)))

df = pd.DataFrame(final_data)
print(df.head())
print('\n')
print(Counter(df[1].apply(str)))

np.save('training_data_{}_balanced.npy'.format(n), final_data)
print('\n')
print('Data Balanced and Saved!')