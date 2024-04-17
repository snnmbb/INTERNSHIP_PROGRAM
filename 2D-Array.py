import numpy as np
import matplotlib.pyplot as plt
import math

x = np.arange(0, 256)
y = np.arange(0, 256)
arr1 = np.zeros((y.size, x.size))
arr2 = np.zeros((y.size, x.size))


cx1 = 140# x position
cy1 = 140  # y position
r1 = 40   # radius of circle
cx2 = 150
cy2 = 150
r2 = 40

intensity1 = (x[np.newaxis,:]-cx1)**2 + (y[:,np.newaxis]-cy1)**2 < r1**2
intensity2 = (x[np.newaxis,:]-cx2)**2 + (y[:,np.newaxis]-cy2)**2 < r2**2
arr1[intensity1] = 50
arr2[intensity2] = 100
arr_total = arr1+arr2
counts, bins = np.histogram(arr_total)

fig = plt.figure(1)
plt.imshow(arr_total)
fig2 = plt.figure(2)
plt.hist(arr_total, bins='auto')
print(arr1, arr1.max(), arr1.min())
print(arr2, arr2.max(), arr2.min())
plt.show()