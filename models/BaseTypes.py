from enum import IntEnum
import cv2
import numpy as np
from random import randint

class TrainingDataType(IntEnum):
    
    SRC = 0 # raw unsorted
    DST = 1
    
    SRC_YAW_SORTED = 2 # sorted by yaw
    DST_YAW_SORTED = 3
    
    SRC_YAW_SORTED_AS_DST = 4 #sorted by yaw but included only yaws which exist in DST_YAW_SORTED also automatic mirrored
    
    DST_YAW_SORTED_AS_SRC = 5 #<- actually you dont need it, because we are swapping face only in src->dst way
    
    SRC_YAW_SORTED_AS_DST_WITH_NEAREST = 6 #same as SRC_YAW_SORTED_AS_DST but samples can return get_random_nearest_target_sample()
    
    DST_YAW_SORTED_AS_SRC_WITH_NEAREST = 7 #<- actually you dont need it, because we are swapping face only in src->dst way

    QTY = 8
    
class TrainingDataSample(object):

    def __init__(self, filename=None, shape=None, landmarks=None, yaw=None, mirror=None, nearest_target_list=None):
        self.filename = filename
        self.shape = shape
        self.landmarks = np.array(landmarks)
        self.yaw = yaw
        self.mirror = mirror
        self.nearest_target_list = nearest_target_list
        
    def copy_and_set(self, filename=None, shape=None, landmarks=None, yaw=None, mirror=None, nearest_target_list=None):
        return TrainingDataSample( 
            filename=filename if filename is not None else self.filename, 
            shape=shape if shape is not None else self.shape, 
            landmarks=landmarks if landmarks is not None else self.landmarks.copy(), 
            yaw=yaw if yaw is not None else self.yaw, 
            mirror=mirror if mirror is not None else self.mirror, 
            nearest_target_list=nearest_target_list if nearest_target_list is not None else self.nearest_target_list)
    
    def load_image(self):
        img = cv2.imread (self.filename).astype(np.float32) / 255.0
        if self.mirror:
            img = img[:,::-1].copy()
        return img
        
    def load_image_hsv(self):
        return cv2.cvtColor( self.load_image(), cv2.COLOR_BGR2HSV )
    
        img = cv2.cvtColor( cv2.imread (self.filename) , cv2.COLOR_BGR2HSV ) / 255.0
        if self.mirror:
            img = img[:,::-1].copy()
        return img
        
    def get_random_nearest_target_sample(self):
        if self.nearest_target_list is None:
            return None
        return self.nearest_target_list[randint (0, len(self.nearest_target_list)-1)]