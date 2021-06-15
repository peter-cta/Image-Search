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
        #print("cX : {} , cY : {} , (cX,cY) : {}".format(cX, cY, (cX, cY)))
        segments = [(0, cX, 0, cY), (cX, w, 0, cY),
                    (cX, w, cY, h), (0, cX, cY, h)]

        (axesX, axesY) = (int((w * 0.75) / 2), int((h * 0.75) / 2))
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        #print("ellipMask : {} , size : {}".format(ellipMask,len(ellipMask)))
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        #print("Value after calc ellipse : ",ellipMask)
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
        #print("hist : {} , length : {} ".format(hist,len(hist)))
        cv2.normalize(hist,hist)
        hist = hist.flatten()
        #print("hist.flatten : {} , length : {}".format(hist,len(hist)))
        return hist

def features_extract(path_to_csv,path_to_dataset):
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
  
    def search(self, queryFeatures, limit = 3):
        # initialize our dictionary of results
        results = {}
            # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)
            # loop over the rows in the index
            for row in reader:
                #print(len(row))
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


def search(img,path_to_csv):
    cd = ColorDescriptor((8, 12, 3))
    query = cv2.imread(img)
    features = cd.describe(query)
    #print("featues input : ",features)
    # perform the search
    searcher = Searcher(path_to_csv)
    results = searcher.search(features)
    
    cv2.imshow("Query", query)
    for (score, resultID) in results:
        img_result = cv2.imread(resultID)
        cv2.imshow('Result', img_result)
        cv2.waitKey(0)   
    cv2.destroyAllWindows()