import cv2
import traceback
import glob
import numpy as np
from matplotlib import pyplot as plt


class Recognizer:
    def __init__(self, filename, images_path):
        self.image = self.charge_image(filename)
        self.library = self.charge_library(images_path)
        self.compare()

    def charge_image(self, filename):
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)
        return image

    def charge_library(self, images_path):
        path = glob.glob(images_path + "/*.png")
        files = []
        for file in path:
            image = cv2.imread(file, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)
            name = file.split("\\")[-1].split(".")[0]
            features = self.getFeatures(image)
            files.append((name.capitalize(), image, features))
        return files

    def createDetector(self):
        detector = cv2.ORB_create(nfeatures=2000)
        return detector

    def getFeatures(self, image):
        image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = self.createDetector()
        kps, descs = detector.detectAndCompute(image_bw, None)
        return kps, descs, image.shape[:2][::-1]

    def detectFeatures(self, image, features):
        def detectFeatures(image, features):
            train_kps, train_descs, shape = features
            # get features from input image
            kps, descs, _ = self.getFeatures(image)
            # check if keypoints are extracted
            if not kps:
                return None
            # now we need to find matching keypoints in two sets of descriptors (from sample image, and from current image)
            # knnMatch uses k-nearest neighbors algorithm for that
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            matches = bf.knnMatch(train_descs, descs, k=2)
            good = []
            # apply ratio test to matches of each keypoint
            # idea is if train KP have a matching KP on image, it will be much closer than next closest non-matching KP,
            # otherwise, all KPs will be almost equally far
            for m, n in matches:
                if m.distance < 0.8 * n.distance:
                    good.append([m])
            # stop if we didn't find enough matching keypoints
            if len(good) < 0.1 * len(train_kps):
                return None
            # estimate a transformation matrix which maps keypoints from train image coordinates to sample image
            src_pts = np.float32([train_kps[m[0].queryIdx].pt for m in good
                                  ]).reshape(-1, 1, 2)
            dst_pts = np.float32([kps[m[0].trainIdx].pt for m in good
                                  ]).reshape(-1, 1, 2)
            m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if m is not None:
                # apply perspective transform to train image corners to get a bounding box coordinates on a sample image
                scene_points = cv2.perspectiveTransform(
                    np.float32([(0, 0), (0, shape[0] - 1), (shape[1] - 1, shape[0] - 1), (shape[1] - 1, 0)]).reshape(-1,
                                                                                                                     1,
                                                                                                                     2),
                    m)
                rect = cv2.minAreaRect(scene_points)
                # check resulting rect ratio knowing we have almost square train image
                if rect[1][1] > 0 and 0.8 < (rect[1][0] / rect[1][1]) < 1.2:
                    return rect
            return None

    def compare(self):
        self.type = "AUCUN LOGO RECONNU"
        for index in self.library:
            name = index[0]
            image = index[1]
            features = index[2]
            region = self.detectFeatures(self.image, features)
            if region is not None:
                box = cv2.boxPoints(region)
                box = np.int0(box)
                #cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
            cv2.imshow(name, image)
