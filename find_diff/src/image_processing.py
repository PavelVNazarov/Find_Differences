# src/image_processing.py - обработка изображений
# image_processing.py
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def load_and_preprocess(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def resize_to_match(img1, img2):
    h1, w1 = img1.shape[:2]
    return cv2.resize(img2, (w1, h1))

def find_differences(img1, img2, method='combined'):
    # Приведение к одинаковому размеру
    img2 = resize_to_match(img1, img2)

    # Конвертация в grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

    # Размытие для уменьшения шума
    gray1 = cv2.bilateralFilter(gray1, 9, 75, 75)
    gray2 = cv2.bilateralFilter(gray2, 9, 75, 75)

    # Вычисление разницы
    if method == 'ssim':
        score, diff = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype("uint8")
    else:
        diff = cv2.absdiff(gray1, gray2)

    # Пороговая обработка
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Морфологические операции
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Поиск контуров
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Рисование контуров
    img_with_contours = img2.copy()
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img_with_contours, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return thresh, img_with_contours, len(contours) > 0


