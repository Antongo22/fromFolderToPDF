import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from natsort import natsorted


def create_pdf_from_photos(folder_path, output_folder):
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in natsorted(files):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, filename))

    if len(image_files) == 0:
        print("В выбранной папке и ее подпапках нет фотографий.")
        return

    pdf_filename = os.path.join(output_folder, os.path.basename(folder_path) + '.pdf')

    pdf_images = []
    for image_file in image_files:
        image = Image.open(image_file)
        pdf_images.append(image.convert('RGB'))

    pdf_images[0].save(pdf_filename, save_all=True, append_images=pdf_images[1:])
    print("PDF-файл успешно создан:", pdf_filename)


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Выберите папку с фотографиями")
    if folder_path:
        parent_folder = os.path.dirname(folder_path)
        output_folder = os.path.join(parent_folder, os.path.basename(folder_path) + " PDF")
        os.makedirs(output_folder, exist_ok=True)

        for root, dirs, files in os.walk(folder_path):
            for folder in dirs:
                subfolder_path = os.path.join(root, folder)
                create_pdf_from_photos(subfolder_path, output_folder)


def main():
    select_folder()


if __name__ == '__main__':
    main()
