import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 32)
y = np.arange(0, 32)
arr1 = np.zeros((y.size, x.size))
arr2 = np.zeros((y.size, x.size))


cx1 = 16 # x position
cy1 = 16  # y position
r1 = 10   # radius of circle
cx2 = 4
cy2 = 4
r2 = 64

intensity1 = (x[np.newaxis,:]-cx1)**2 + (y[:,np.newaxis]-cy1)**2 < r1**2
intensity2 = (x[np.newaxis,:]-cx2)**2 + (y[:,np.newaxis]-cy2)**2 < r2**2
arr1[intensity1] = 50
arr2[intensity2] = 200

print(arr1, arr1.max(), arr1.min())
# print(arr1[intensity1])
#print(arr2[intensity2])
plt.figure(figsize=(5, 5))
# plt.pcolormesh(x, y, arr1)
plt.imshow(arr1)

#plt.pcolormesh(x, y, arr2)
#plt.title("Intensity", loc='right')
#plt.hist(arr1, bins = range(256))
plt.show()