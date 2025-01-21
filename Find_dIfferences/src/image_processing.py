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

    # Вычисляем абсолютную разницу между изображениями
    diff = cv2.absdiff(gray1, gray2)

    # Применяем порог для выделения отличий
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Находим контуры отличий
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Рисуем контуры на оригинальном изображении
    for contour in contours:
        cv2.drawContours(img1, [contour], -1, (0, 255, 0), 2)  # Зеленый цвет для контуров

    return thresh, img1  # Возвращаем также изображение с контурами

