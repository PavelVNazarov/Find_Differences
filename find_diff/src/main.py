# python main.py

# src/main.py - основное приложение
# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
from image_processing import load_and_preprocess, find_differences
from difference_visualization import DifferenceVisualizer


class ImageComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Difference Analyzer")
        self.root.geometry("1200x800")

        self.img1 = None
        self.img2 = None
        self.result_data = None

        self.create_widgets()
        self.set_styles()

    def set_styles(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')

        self.root.configure(bg='#f0f0f0')

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, fill=tk.X)

        self.btn_load1 = ttk.Button(control_frame, text="Изображение 1", command=self.load_image1)
        self.btn_load1.pack(side=tk.LEFT, padx=5)

        self.btn_load2 = ttk.Button(control_frame, text="Изображение 2", command=self.load_image2)
        self.btn_load2.pack(side=tk.LEFT, padx=5)

        self.btn_compare = ttk.Button(control_frame, text="Найти отличия",
                                      command=self.compare_images, state=tk.DISABLED)
        self.btn_compare.pack(side=tk.LEFT, padx=5)

        self.btn_save = ttk.Button(control_frame, text="Сохранить",
                                   command=self.save_result, state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Label(self.root, text="Готово", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_frame = ttk.Frame(self.root)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

    def load_image(self, target_var):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if file_path:
            try:
                img = load_and_preprocess(file_path)
                target_var = img
                self.update_status(f"Loaded: {file_path}")
                return img
            except Exception as e:
                messagebox.showerror("Error", f"Не удалось загрузить: {str(e)}")
        return None

    def load_image1(self):
        self.img1 = self.load_image(1)
        self.check_ready_state()

    def load_image2(self):
        self.img2 = self.load_image(2)
        self.check_ready_state()

    def check_ready_state(self):
        if self.img1 is not None and self.img2 is not None:
            self.btn_compare.config(state=tk.NORMAL)
            self.show_thumbnails()

    def show_thumbnails(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        thumb_size = (300, 300)

        img1_thumb = Image.fromarray(self.img1).resize(thumb_size)
        img2_thumb = Image.fromarray(self.img2).resize(thumb_size)

        self.tk_img1 = ImageTk.PhotoImage(img1_thumb)
        self.tk_img2 = ImageTk.PhotoImage(img2_thumb)

        label1 = ttk.Label(self.image_frame, image=self.tk_img1)
        label2 = ttk.Label(self.image_frame, image=self.tk_img2)

        label1.pack(side=tk.LEFT, padx=10)
        label2.pack(side=tk.LEFT, padx=10)

    def compare_images(self):
        try:
            diff_mask, result_img, has_diff = find_differences(self.img1, self.img2)

            for widget in self.image_frame.winfo_children():
                widget.destroy()

            self.result_data = (self.img1, self.img2, diff_mask, result_img)
            DifferenceVisualizer(self.image_frame, *self.result_data)

            self.btn_save.config(state=tk.NORMAL)
            self.update_status(f"Differences found: {has_diff}")

        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed: {str(e)}")

    def save_result(self):
        if self.result_data:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    cv2.imwrite(file_path, cv2.cvtColor(self.result_data[3], cv2.COLOR_RGB2BGR))
                    self.update_status(f"Result saved to: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Save failed: {str(e)}")

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageComparatorApp(root)
    root.mainloop()

