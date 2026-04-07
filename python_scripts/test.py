import csv
import time
import numpy as np
import sys

arguments = sys.argv
print(arguments)

data_path = 'data/' + arguments[1]

runtime = int(arguments[2])

file = open(data_path, 'w', newline = None)
csvwriter = csv.writer(file, delimiter = ',')

meta = ['time', 'data']

csvwriter.writerow(meta)

for i in range(runtime):
    time.sleep(1)
    now = time.time
    value = np.random.random()
    csvwriter.writerow([now, value])

file.close()
