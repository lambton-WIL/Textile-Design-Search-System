from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import glob
import csv
import os
import time

app = Flask(__name__, template_folder='files/templates', static_folder='files/static')


class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins

    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
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
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist, 0, 255, cv2.NORM_MINMAX).flatten()

        return hist

class Searcher:
    def __init__(self, indexPath):
        self.indexPath = indexPath

    def search(self, queryFeatures, limit=10):
        results = {}

        with open(self.indexPath) as f:
            reader = csv.reader(f)
            for row in reader:
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)
                results[row[0]] = d
            f.close()

        results = sorted([(v, k) for (k, v) in results.items()])

        return results[:limit]

    def chi2_distance(self, histA, histB, eps=1e-10):
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])
        return d


def index_images(dataset, index):
    cd = ColorDescriptor((8, 12, 3))
    with open(index, "a") as output:  # Use "a" mode to append to the existing index file
        for imagePath in glob.glob(dataset + "/*.jpg"):
            imageID = imagePath[imagePath.rfind("/") + 1:]
            # Check if the image is already indexed by searching for its ID in the index file
            if imageID not in get_indexed_images(index):
                try:
                    image = cv2.imread(imagePath)
                    # Check if the image was loaded successfully
                    if image is not None:
                        features = cd.describe(image)
                        features = [str(f) for f in features]
                        output.write("%s,%s\n" % (imageID, ",".join(features)))
                    else:
                        print(f"Failed to load image: {imagePath}")
                except cv2.error as e:
                    print(f"OpenCV Error: {e}")

def get_indexed_images(index):
    indexed_images = set()
    with open(index, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            imageID = row[0]
            indexed_images.add(imageID)
    return indexed_images

@app.route('/update_index')
def update_index():
    #dataset = 'files/static/dataset'
    dataset = 'files/static/dataset/'
    index = 'files/index.csv'

    indexed_images = get_indexed_images(index)
    for imagePath in glob.glob(dataset + "/*.jpg"):
        imageID = imagePath[imagePath.rfind("/") + 1:]
        if imageID not in indexed_images:
            # New file detected, index it
            image = cv2.imread(imagePath)
            features = cd.describe(image)
            features = [str(f) for f in features]
            with open(index, "a") as output:
                output.write("%s,%s\n" % (imageID, ",".join(features)))
    
    return 'Index update completed.'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the uploaded file from the request
    uploaded_file = request.files['file']
    limit = int(request.form['limit'])
    index = 'files/index.csv'

    # Save the uploaded file to a temporary location
    file_path = 'files/static/uploads/' + secure_filename(uploaded_file.filename)
    uploaded_file.save(file_path)

    # Perform the image search
    results = search_images(file_path, index, limit)

    # Remove the temporary uploaded file
    os.remove(file_path)

    return render_template('result.html', results=results)

@app.route('/index', methods=['POST'])
def index():
    dataset = 'files/static/dataset/'
    index = 'files/index.csv'

    index_images(dataset, index)

    return 'Image indexing completed.'


def search_images(query, index, limit=10):
    cd = ColorDescriptor((8, 12, 3))
    queryImage = cv2.imread(query)
    queryFeatures = cd.describe(queryImage)

    searcher = Searcher(index)
    results = searcher.search(queryFeatures, limit=limit)

    return results

if __name__ == '__main__':
    app.run(debug=True)
