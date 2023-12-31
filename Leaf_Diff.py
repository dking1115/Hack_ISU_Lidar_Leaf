import numpy as np
import cv2
import pcl2
from leaf_class import leaf

##lower_color = np.array([lower_blue, lower_green, lower_red])
##upper_color = np.array([upper_blue, upper_green, upper_red])

cap = cv2.VideoCapture(0)

lower_color = np.array([0, 10, 10])
upper_color = np.array([80, 255, 90])
min_area=15

def Leaf_Ident(img,correlated_img,debug=False):
    """Identifies leafs in the image and outputs an array of leaf objects"""
    #img is an np array of pixels with their RGB value and xyz cooridinates
    #leaf class output
    
    leaf_array=[]
    height,width,channels = img.shape
    i=0
    contour_mask= None
    # Create a binary mask of pixels within the specified color range
    mask = cv2.inRange(img, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_with_contours = cv2.drawContours(mask.copy(), contours, -1, (0, 255, 0), 2)
    filtered_contours = [contour for contour in contours if min_area < cv2.contourArea(contour)]
    for contour in filtered_contours:
        pc=np.empty((0,6))
        contour_mask=np.zeros_like(mask)
        cv2.drawContours(contour_mask,[contour],-1,255,thickness=cv2.FILLED)
        #print(f"area {cv2.contourArea(contour)}")
        for i in range(height):
            for j in range(width):
                if contour_mask[i,j]:
                    #print(f"i: {i} type {type(i)} j: {j} type {type(j)}")
                    #print(correlated_img.shape)
                    x,y,z,r,g,b=correlated_img[i,j]
                    row=[x,y,z,r,g,b]
                    #pc=np.vstack((pc,row))
        leaf_obj=leaf(pc,contour_mask)
        
        leaf_array.append(leaf_obj)


    

    if debug:
        cv2.imshow('Contorus',frame_with_contours)
        cv2.imshow('Mask',mask)
        if contour_mask is not None:
            cv2.imshow("Contour_Mask",contour_mask)
        cv2.waitKey(1)

    return leaf_array



if __name__=="__main__":
    #img=np.random.rand(100,100,3)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't recieve the image")
            break
        
        correlated_img=np.random.rand(480,640,6)
        out=Leaf_Ident(frame,correlated_img,debug=True)
        print(out[0].point_cloud)
    cv2.destroyAllWindows()


    