# src/main.py - основное приложение

import cv2
from tkinter import Tk, Frame, Button, Label, filedialog, messagebox
from image_processing import load_images, find_differences
from difference_visualization import visualize_differences

class App:
    def __init__(self, master):
        self.master = master
        master.title("Сравнение изображений")
        self.label = Label(master, text="Добро пожаловать в программу сравнения изображений!")
        self.label.pack()
        self.load_img1_button = Button(master, text="Загрузить первое изображение", command=self.load_image1)
        self.load_img1_button.pack()
        self.load_img2_button = Button(master, text="Загрузить второе изображение", command=self.load_image2)
        self.load_img2_button.pack()
        self.find_differences_button = Button(master, text="Найти отличия", command=self.find_differences)
        self.find_differences_button.pack()
        self.img1_path = None
        self.img2_path = None
        self.img1 = None
        self.img2 = None

    def load_image1(self):
        self.img1_path = filedialog.askopenfilename(title="Выберите первое изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not self.img1_path:
            messagebox.showerror("Ошибка", "Не выбрано первое изображение.")
            return
        self.img1 = cv2.imread(self.img1_path)
        if self.img1 is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить первое изображение.")
            return
        messagebox.showinfo("Успех", "Первое изображение успешно загружено.")

    def load_image2(self):
        self.img2_path = filedialog.askopenfilename(title="Выберите второе изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not self.img2_path:
            messagebox.showerror("Ошибка", "Не выбрано второе изображение.")
            return
        self.img2 = cv2.imread(self.img2_path)
        if self.img2 is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить второе изображение.")
            return
        messagebox.showinfo("Успех", "Второе изображение успешно загружено.")

    def find_differences(self):
        if self.img1 is None or self.img2 is None:
            messagebox.showerror("Ошибка", "Необходимо загрузить оба изображения.")
            return
        # Проверяем размеры и изменяем, если нужно
        if self.img1.shape != self.img2.shape:
            self.img2 = cv2.resize(self.img2, (self.img1.shape[1], self.img1.shape[0]))
        # Поиск отличий
        differences, img_with_contours, has_differences = find_differences(self.img1, self.img2)
        # Визуализация результатов
        visualize_differences(self.img1, self.img2, differences, img_with_contours, has_differences)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()

