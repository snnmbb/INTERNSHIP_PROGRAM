import cv2
import matplotlib.pyplot as plt


image= cv2.imread(r"C:\Users\Asus\Desktop\Dot.png")
original_image= image

gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)


contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)

item= sorted_contours[0]


#largest item
R= cv2.moments(item)


coordinate_center= int(R['m10']/R['m00'])


print("x center coordinate ", str(coordinate_center))

print("")


plt.imshow(image)
plt.show()
