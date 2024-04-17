import numpy as np
import matplotlib.pyplot as plt
import math

x = np.arange(0, 256)
y = np.arange(0, 256)
arr1 = np.zeros((y.size, x.size))
arr2 = np.zeros((y.size, x.size))


cx1 = 64 # x position
cy1 = 64  # y position
r1 = 30   # radius of circle
cx2 = 150
cy2 = 150
r2 = 30

intensity1 = (x[np.newaxis,:]-cx1)**2 + (y[:,np.newaxis]-cy1)**2 < r1**2
intensity2 = (x[np.newaxis,:]-cx2)**2 + (y[:,np.newaxis]-cy2)**2 < r2**2
arr1[intensity1] = 50
arr2[intensity2] = 200
arr_total = arr1+arr2

f = plt.figure(1)
plt.imshow(arr_total)
print(arr1, arr1.max(), arr1.min())
print(arr2, arr2.max(), arr2.min())
# print(arr1[intensity1])
#print(arr2[intensity2])
#plt.figure(figsize=(5, 5))
# plt.pcolormesh(x, y, arr1)
plt.show()