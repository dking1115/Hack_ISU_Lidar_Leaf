import numpy as np

class leaf():
    def __init__(self,point_cloud_in,img_mask):
        self.img_mask=img_mask
        self.point_cloud=point_cloud_in
        self.surface_area=0
        
        