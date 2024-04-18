import numpy as np
import matplotlib.pyplot as plt
import math

x = np.arange(0, 256)
y = np.arange(0, 256)
arr1 = np.zeros((y.size, x.size))
arr2 = np.zeros((y.size, x.size))


cx1 = 160# x center position
cy1 = 160  # y center position
r1 = 40   # radius of circle
cx2 = 140
cy2 = 140
r2 = 40

intensity1 = (x[np.newaxis,:]-cx1)**2 + (y[:,np.newaxis]-cy1)**2 < r1**2
intensity2 = (x[np.newaxis,:]-cx2)**2 + (y[:,np.newaxis]-cy2)**2 < r2**2
arr1[intensity1] = 50
arr2[intensity2] = 100
arr_total = arr1+arr2
counts, bins = np.histogram(arr_total)

distance_x = cx1-cx2
distance_y = cy1-cy2
fig = plt.figure(1)
plt.imshow(arr_total)

fig2 = plt.figure(2)
plt.hist(arr_total.flatten(), bins=30) #, bins='auto'
print(arr1, arr1.max(), arr1.min())
print(arr2, arr2.max(), arr2.min())
print(arr_total, arr_total.max(), arr_total.min())
print(distance_x)
print(distance_y)
plt.show()