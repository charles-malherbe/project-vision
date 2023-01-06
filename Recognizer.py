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
            features = 0
            files.append((name.capitalize(), image, features))
        return files


    def compare(self):
        self.type = "AUCUN LOGO RECONNU"
        for index in self.library:
            name = index[0].capitalize()
            image = index[1]
            features = index[2]