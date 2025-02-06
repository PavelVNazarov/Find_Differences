
import cv2
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image

class ImageComparator:
    def __init__(self):
        self.model = VGG16(weights='imagenet', include_top=False, pooling='avg')

    def extract_features(self, img):
        img = cv2.resize(img, (224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        features = self.model.predict(img)
        return features.flatten()

    def compare(self, img1, img2, threshold=0.9):
        features1 = self.extract_features(img1)
        features2 = self.extract_features(img2)
        similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
        return similarity > threshold

