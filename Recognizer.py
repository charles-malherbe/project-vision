import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt

class Recognizer:
    def __init__(self, filename, images_path):
        self.img_original = self.charge_image(filename)
        self.library = self.charge_library(images_path)
        self.compare()

    def charge_image(self, filename):
        img_original = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        img_original = cv2.resize(img_original, (500, 500), interpolation = cv2.INTER_AREA)
        return img_original

    def charge_library(self, images_path):
        path = glob.glob(images_path + "/*.jpg")
        images = []
        for image in path:
            percentage = 0.00
            file = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
            file = cv2.resize(file, (500, 500), interpolation = cv2.INTER_AREA)
            name = image.split("\\")[-1].split(".")[0]
            name.capitalize()
            images.append((name, file, percentage))
        return images

    def compare(self):
        for index in self.library:
            name = index[0]
            image = index[1]
            percentage = index[2]
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(self.img_original, None)
            kp2, des2 = orb.detectAndCompute(image, None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.Match(des1, des2, k=2)
            good = []
            for m,n in matches:
                if m.distance < 0.75*n.distance:
                    good.append([m])
            percentage = len(good)
            comparaison = cv2.drawMatchesKnn(self.img_original, kp1, image, kp2, good, None, flags=2)
            index = (name, image, percentage, comparaison)
            print(index)
            plt.imshow(comparaison), plt.show()
