__author__ = 'infosense'
import sys
sys.path.append("/data2/home/jw1498/.conda/envs/myvpy/lib/python2.7/site-packages")
import numpy as np
from datetime import datetime
import urllib,json,os,csv,cv2

def download_photo(img_url,path,filename):
    try:
        image_on_web = urllib.urlopen(img_url)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            file_path = os.path.join(path, filename)
            downloaded_image = open(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            #print(img_url)
            return False
    except:
        return False
    return True

class ColorDescriptor:
    def __init__(self, bins):
        # store the number of bins for the 3D histogram
        self.bins = bins

    def describe(self, image):
        # convert the image to the HSV color space and initialize
        # the features used to quantify the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        # grab the dimensions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        # divide the image into four rectangles/segments (top-left,
        # top-right, bottom-right, bottom-left)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),(0, cX, cY, h)]

        # construct an elliptical mask representing the center of the image
        (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
        ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        # loop over the segments
        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting
			# the elliptical center from it
            cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)

            # extract a color histogram from the image, then update the feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)

        # extract a color histogram from the elliptical region and
        #  update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)

        # return the feature vector
        return features

    def histogram(self, image, mask):
        # extract a 3D color histogram from the masked region of the
        # image, using the supplied number of bins per channel; then
        # normalize the histogram
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,[0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist,hist).flatten()
        # return the histogram
        return hist

class Searcher:
    def __init__(self, indexPath):
        # store our index path
        self.indexPath = indexPath

    def search(self, queryFeatures, limit = 50):
        # initialize our dictionary of results
        results = {}

        # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)
            # loop over the rows in the index
	    start = datetime.now()
            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                # and our query features
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)
                # now that we have the distance between the two feature
                # vectors, we can udpate the results dictionary -- the
                # key is the current image ID in the index and the
                # value is the distance we just computed, representing
                # how 'similar' the image in the index is to our query
                results[row[0]] = d
            # close the reader
            f.close()
	    print((datetime.now()-start).seconds)
        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        results = sorted([(v, k) for (k, v) in results.items()])

        # return our (limited) results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])
        # return the chi-squared distance
        return d

if __name__ == "__main__" :
    #system call from IndriSearchInterface::performSearch with 'python image_search.py'
    queried_img_path = "image_log" #cache queried downloaded images
    with open("img_url_log") as f:
        #everytime a image query is performed, the image url is written into the last line of the imgLog file first.
        lines = f.readlines()
        if lines:
            query_img_url = lines[-1]
            if download_photo(query_img_url,"./","query"):
                # initialize the image descriptor
                cd = ColorDescriptor((8, 12, 3))
                # load the query image and describe it
                query = cv2.imread("query")
		features = cd.describe(query)
                # perform the search
                searcher = Searcher("a.csv")
		#start = datetime.now()
                results = searcher.search(features)
		#print((datetime.now()-start).seconds)
                # display the query
                #cv2.imshow("Query", query)
		results = map(lambda k:k[1].split(".")[0].split("_")[0],results)
                # loop over the results
                for resultID in list(set(results)):
                    #load the result image and display it
		    print(resultID)
                    # result = cv2.imread(args["result_path"] + "/" + resultID)
                    # cv2.imshow("Result", result)
                    # cv2.waitKey(0)
		os.system("rm -f query")
