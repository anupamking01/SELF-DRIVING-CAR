import numpy as np
from random import shuffle
import os

'''
Now that we have our training data balanced, we can combine all our batches
into one single file. This would make it easier for us to train our CNN.
'''

# enter the maximum of training data batch number.
n = int(input('Enter the no. of batches: '))
final = []

for i in range(n):
    if not os.path.isfile(f'training_data_{i+1}.npy'):
        i = i+1
    file = list(np.load(f'training_data_{i+1}.npy',allow_pickle=True))
    print(f'Loaded {i+1}')
    final.extend(file)
    print(f'Extended {i+1}')

shuffle(final)
print('Data Shuffled!')

np.save('combined_data.npy', final)
print("done")
print('Saved! Length of data: ', len(final))