#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import imutils 


# In[2]:


image = cv2.imread('body_rec_images/UPS_Driver/6bfdba017d.jpg') 


# In[3]:


image = imutils.resize(image, 
                       width=min(500, image.shape[1])) 


# In[4]:


hog = cv2.HOGDescriptor()  
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 


# In[5]:


(humans, _) = hog.detectMultiScale(image,  
                                     winStride=(8,8), padding=(32,32), scale=1.05)


# In[7]:


for (x, y, w, h) in humans: 
#     cv2.rectangle(image, (x, y),  
#                   (x + w, y + h),  
#                   (0, 0, 255), 2) 
    crop_img = image[y:y+h, x:x+w]


# In[ ]:


# Displaying the output Image 
cv2.imshow("Image", crop_img) 
cv2.waitKey(0) 
   
cv2.destroyAllWindows() 


# In[ ]:




