# src/image_processing.py - обработка изображений

import cv2
import numpy as np


def load_images(image_path1, image_path2):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    if img1 is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path1}")
    if img2 is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path2}")

    return img1, img2

def find_differences(img1, img2):
    # Преобразуем изображения в оттенки серого
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Применяем адаптивное сглаживание для уменьшения шума
    gray1 = cv2.bilateralFilter(gray1, 9, 75, 75)
    gray2 = cv2.bilateralFilter(gray2, 9, 75, 75)

    # Применяем CLAHE для улучшения контрастности
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray1 = clahe.apply(gray1)
    gray2 = clahe.apply(gray2)

    # Вычисляем абсолютную разницу между изображениями
    diff = cv2.absdiff(gray1, gray2)

    # Применяем порог для выделения отличий
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Применяем Canny для выделения контуров
    edges = cv2.Canny(thresh.astype(np.uint8), 100, 200)

    # Находим контуры отличий
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Рисуем контуры на изображении с отличиями
    img_with_contours = img2.copy()  # Копируем второе изображение для рисования контуров
    for contour in contours:
        cv2.drawContours(img_with_contours, [contour], -1, (0, 255, 0), 2)  # Зеленый цвет для контуров

    return thresh, img_with_contours  # Возвращаем изображение с контурами
