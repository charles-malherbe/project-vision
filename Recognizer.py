import glob

import cv2


class Recognizer:
    def __init__(self, filename, images_path):
        self.image = self.charge_image(filename)
        self.library = self.charge_library(images_path)
        self.type = "Aucunes correspondances"
        self.compare()

    def get_bw_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        final = cv2.GaussianBlur(image, (5,5), 0)
        cv2.imshow("Original", final)
        return image

    def charge_image(self, filename):
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)
        return image

    def charge_library(self, images_path):
        files = []
        for file in glob.glob(images_path.get() + "/*.png"):
            image = cv2.imread(file, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
            name = file.split("/")[-1].split(".")[0]
            files.append((name, image))
        return files

    def create_detector(self):
        detector = cv2.ORB_create()
        return detector

    def create_matcher(self):
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        return matcher

    def detect_logo(self, name, logo):

        detector = self.create_detector()
        matcher = self.create_matcher()
        kp_logo, des_logo = detector.detectAndCompute(self.get_bw_image(logo), None)
        kp_image, des_image = detector.detectAndCompute(self.get_bw_image(self.image), None)
        matches = matcher.match(des_logo, des_image)
        matches = sorted(matches, key=lambda x: x.distance)
        final = cv2.drawMatches(logo, kp_logo, self.image, kp_image, matches[:10], None, flags=2)
        cv2.imshow("Comparaison", final)

    def compare(self):
        for index in self.library:
            name = index[0].split("\\")[-1].split(".")[0].upper()
            self.detect_logo(name, index[1])
