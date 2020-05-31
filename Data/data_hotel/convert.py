import os
import pandas as pd

dirpath_pos = './train/pos'
dirpath_neg = './train/neg'
output = './train.csv'

f_output = open(output, "a")
f_output.write('\t'.join(['id', 'text', 'label']) + '\n')

def writeToCSV(dirpath = './', prefix_id = 'train_' ,label = '1', index = 0):
    files = [os.path.join(dirpath, fname) for fname in os.listdir(dirpath)]
    for filename in sorted(files):
        f = open(filename,"r+")
        comment = '. '.join(f.read().split('\n'))
        id = prefix_id + '0' * (6 - len(str(index))) + str(index)
        index = index + 1
        f_output.write('\t'.join([id, comment, label]) + '\n')
        
    return index

index = 0
index = writeToCSV(dirpath_pos, 'train_', '1', index)
index = writeToCSV(dirpath_neg, 'train_', '0', index)