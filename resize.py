import argparse
import glob
import cv2
import numpy as np
import csv


class ColorDescriptor:
    def __init__(self, bins):
        # store the number of bins for the 3D histogram
        self.bins = bins

    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        features = []

        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        segments = [(0, cX, 0, cY), (cX, w, 0, cY),
                    (cX, w, cY, h), (0, cX, cY, h)]

        (axesX, axesY) = (int((w * 0.75) / 2), int((h * 0.75) / 2))
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        for (startX, endX, startY, endY) in segments:
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)

            hist = self.histogram(image, cornerMask)
            features.extend(hist)

        hist = self.histogram(image, ellipMask)
        features.extend(hist)

        return features

    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 180, 0, 256, 0, 256])

        cv2.normalize(hist,hist)
        hist = hist.flatten()

        return hist

path_to_csv = 'data.csv'
path_to_dataset = 'dataset';
cd = ColorDescriptor((8, 12, 3))
# open the output index file for writing
output = open(path_to_csv, "w")
for imagePath in glob.glob(path_to_dataset + "/*.jpg"):
    imageID = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)
    features = cd.describe(image)
    # write the features to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imageID, ",".join(features)))
# close the index file
output.close()


class Searcher:
    def __init__(self, indexPath):
  	    # store our index path
  	    self.indexPath = indexPath
  
    def search(self, queryFeatures, limit = 10):
        # initialize our dictionary of results
        results = {}
            # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)
            # loop over the rows in the index
            for row in reader:
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)
                results[row[0]] = d
            # close the reader
            f.close()

        results = sorted([(v, k) for (k, v) in results.items()])
        # return our (limited) results
        return results[:limit]
  	
    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])
        # return the chi-squared distance
        return d

cd = ColorDescriptor((8, 12, 3))
inputImg = 'dataset/test.jpg'
query = cv2.imread(inputImg)
features = cd.describe(query)
# perform the search
searcher = Searcher(path_to_csv)
results = searcher.search(features)
# display the query
cv2.imshow("Query", query)
# loop over the results
path_to_result = 'dataset'
"""for (score, resultID) in results:
	# load the result image and display it
	result = cv2.imread(resultID)
	cv2.imshow('Result', result)
	cv2.waitKey(0)"""

animals = [resultID for (score, resultID) in results ] 
print('animals : ',animals)

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
"""animals = glob.glob('dataset/*.jpg')
print(animals)"""
# reading the files from our animals directory

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

#cv2.imshow('input image',cv2.imread(inputImg))
cv2.imshow('result', cv2.imread(result))
cv2.waitKey(0)

