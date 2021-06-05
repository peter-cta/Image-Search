import imutils
import cv2
import numpy as np 
#import skimage.measure.compare_ssim
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error
import glob
import os 

#Here, we’re simply taking two image matrices and applying the formula for MSE, 
#as shown in the code above.
def mse(imageA, imageB):
    err= np.sum((imageA.astype("float") - imageB.astype("float"))**2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

# keep image similar size
def resize_images(image):
    dim = (1000, 1000)
    return cv2.resize(image, dim)

# convert color image to gray
def imgToGray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# an array of all the animals we have 
#animals = ["dog-1.png", "dog-2.png", "dog-3.png", "elephant-1.jpeg", "elephant-2.png", "elephant-3.jpeg"]
animals = glob.glob('dataset/*.jpg')
print(animals)
# reading the files from our animals directory
inputImg = 'dataset/a (41).jpg'
imageA = cv2.imread(inputImg)
#imageA = resize_images(imageA)
imageA = imgToGray(imageA)
# reading all the animals one by one and comparing them with the 
# fist animal in the array("dog-1.png")

result1 = ''
maxSSIM = 0

for animal in animals:
    imageB = cv2.imread(animal)
    #imageB = resize_images(imageB)
    imageB = imgToGray(imageB)
    (score, diff) = ssim(imageA, imageB, full=True)
    mse = mean_squared_error(imageA, imageB)
    print("For {} & {}, SSIM: {}, MSE: {}".format('Input Image', animal,score, mse))
    if(score>maxSSIM and score < 1):
        maxSSIM = score
        result = animal

cv2.imshow('input image',cv2.imread(inputImg))
cv2.imshow('result', cv2.imread(result))
cv2.waitKey(0)


