import cv2
import matplotlib.pyplot as plt


image= cv2.imread(r"C:\Users\Asus\Desktop\Dot\Dot2.png")
original_image= image

gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edges= cv2.Canny(gray, 50,200)

try:  
    contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)

    dot1= sorted_contours[0]
    dot2= sorted_contours[1]


    #dot1
    R1= cv2.moments(dot1)

    coordinate_center1= int(R1['m10']/R1['m00'])


    print("center coordinate : ", str(coordinate_center1))

    print("")

    #dot2
    R2= cv2.moments(dot2)

    coordinate_center2= int(R2['m10']/R2['m00'])


    print("center coordinate : ", str(coordinate_center2))

    print("")

    distance = coordinate_center1 - coordinate_center2

    print("Distance between dot1 and dot2 : " , str(distance))

    plt.imshow(image)
    plt.show()
except:
    print ("Circles are overlapping")

#ใช้กับรูปที่วงกลมซ้อนทับกันกึ่งกลางไม้ได้