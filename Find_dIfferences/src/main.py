# src/main.py - основной файл

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

    def load_image2(self):
        self.img2_path = filedialog.askopenfilename(title="Выберите второе изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not self.img2_path:
            messagebox.showerror("Ошибка", "Не выбрано второе изображение.")
            return
        self.img2 = cv2.imread(self.img2_path)

    def find_differences(self):
        if self.img1 is None or self.img2 is None:
            messagebox.showerror("Ошибка", "Необходимо загрузить оба изображения.")
            return

        # Проверяем размеры и изменяем, если нужно
        if self.img1.shape != self.img2.shape:
            self.img2 = cv2.resize(self.img2, (self.img1.shape[1], self.img1.shape[0]))

        # Поиск отличий
        differences, img_with_contours = find_differences(self.img1, self.img2)

        # Визуализация результатов
        visualize_differences(self.img1, self.img2, differences, img_with_contours)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()


# import cv2
# from tkinter import Tk, Frame, Button, Label, filedialog, Toplevel
# from image_processing import load_images, find_differences
# from difference_visualization import visualize_differences
#
# def load_image1():
#     global img1_path
#     img1_path = filedialog.askopenfilename(title="Выберите первое изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
#     if img1_path:
#         img1_label.config(text="Первое изображение загружено.")
#
# def load_image2():
#     global img2_path
#     img2_path = filedialog.askopenfilename(title="Выберите второе изображение", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
#     if img2_path:
#         img2_label.config(text="Второе изображение загружено.")
#
# def find_and_visualize():
#     if img1_path and img2_path:
#         img1, img2 = load_images(img1_path, img2_path)
#         if img1.shape != img2.shape:
#             img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
#         differences, img_with_contours = find_differences(img1, img2)
#         visualize_differences(img1, img2, differences, img_with_contours)
#     else:
#         print("Пожалуйста, загрузите оба изображения.")
#
# def open_main_window():
#     main_window = Toplevel(root)
#     main_window.title("Главное окно")
#     Label(main_window, text="Добро пожаловать в программу сравнения изображений!", padx=20, pady=20).pack()
#     Label(main_window, text="Выберите два изображения для сравнения.").pack()
#
#     Button(main_window, text="Загрузить первое изображение", command=load_image1).pack(pady=5)
#     global img1_label
#     img1_label = Label(main_window, text="Первое изображение не загружено.")
#     img1_label.pack()
#
#     Button(main_window, text="Загрузить второе изображение", command=load_image2).pack(pady=5)
#     global img2_label
#     img2_label = Label(main_window, text="Второе изображение не загружено.")
#     img2_label.pack()
#
#     Button(main_window, text="Найти отличия", command=find_and_visualize).pack(pady=20)
#
# # Инициализация tkinter
# root = Tk()
# # root.title("Сравнение изображений")
# root.geometry("400x300")
#
# open_main_window()
#
# root.mainloop()

