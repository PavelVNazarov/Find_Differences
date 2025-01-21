# src/main.py - основной файл
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from image_processing import load_images, find_differences
from difference_visualization import visualize_differences

def main():
    # Инициализация tkinter
    Tk().withdraw()  # Скрываем основное окно

    # Открываем диалог выбора файла для первого изображения
    img1_path = askopenfilename(title="Выберите первое изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not img1_path:
        print("Не выбрано первое изображение.")
        return

    # Открываем диалог выбора файла для второго изображения
    img2_path = askopenfilename(title="Выберите второе изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not img2_path:
        print("Не выбрано второе изображение.")
        return

    # Загрузка изображений
    img1, img2 = load_images(img1_path, img2_path)

    # Проверяем размеры и изменяем, если нужно
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Поиск отличий
    differences, img_with_contours = find_differences(img1, img2)

    # Визуализация результатов
    visualize_differences(img1, img2, differences, img_with_contours)

if __name__ == "__main__":
    main()

