# src/difference_visualization.py - визуализация отличий
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class DifferenceVisualizer:
    def __init__(self, master, img1, img2, diff_mask, result_img):
        self.master = master
        self.figure = plt.figure(figsize=(12, 6))

        self.ax1 = self.figure.add_subplot(141)
        self.ax1.imshow(img1)
        self.ax1.set_title('Изображение 1')
        self.ax1.axis('off')

        self.ax2 = self.figure.add_subplot(142)
        self.ax2.imshow(img2)
        self.ax2.set_title('Изображение 2')
        self.ax2.axis('off')

        self.ax3 = self.figure.add_subplot(143)
        self.ax3.imshow(diff_mask, cmap='gray')
        self.ax3.set_title('Сравнение')
        self.ax3.axis('off')

        self.ax4 = self.figure.add_subplot(144)
        self.ax4.imshow(result_img)
        self.ax4.set_title('Результат')
        self.ax4.axis('off')

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def save_result(self, filename):
        self.figure.savefig(filename, bbox_inches='tight')
