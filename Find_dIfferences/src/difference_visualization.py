# src/difference_visualization.py - визуализация отличий

import cv2
import matplotlib.pyplot as plt

def visualize_differences(img1, img2, differences, img_with_contours, has_differences):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 4, 1)
    plt.title('Image 1')
    plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.title('Image 2')
    plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.title('Differences')
    plt.imshow(differences, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 4, 4)
    plt.title('Image with Contours')
    plt.imshow(cv2.cvtColor(img_with_contours, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    # Добавляем текст о наличии отличий
    plt.figtext(0.5, 0.01, 'Есть отличия' if has_differences else 'Нет отличий', ha='center', fontsize=12)

    plt.show()
