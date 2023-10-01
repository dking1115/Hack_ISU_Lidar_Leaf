from Leaf_Diff import Leaf_Ident
from Luxonis import get_img
import cv2

if __name__=="__main__":
    while True:
        img,cor_img=get_img()
        if img is None:
            print("img is none")
        width,height,channels=img.shape
        print(f"B {img[int(width/2),int(height/2),0]} G {img[int(width/2),int(height/2),1]} R {img[int(width/2),int(height/2),2]}")
        cv2.imshow("img",img)
        cv2.waitKey(1)
        Leaf_Ident(img,cor_img,debug=True)
