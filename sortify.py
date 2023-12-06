import os
import sys
import json
import shutil
import customtkinter
import tkinter as tk
from PIL import Image  
from tkinter import filedialog
from tkinter import messagebox


class Sortify(customtkinter.CTk):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Sortify")
        self.root.iconbitmap("ico.ico")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.subfolders = tk.BooleanVar()
        self.open_after_organize = tk.BooleanVar()
        self.show_alert = tk.BooleanVar()
        self.config_file = "cfg.json"
        self.success_message_displayed = False  # Flag para verificar si se ha mostrado el mensaje de éxito

        self.load_config()

        if self.show_alert.get():
            self.show_alert_message()

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        image1 = customtkinter.CTkImage(light_image=Image.open(os.path.join('image.jpeg')), size=(150, 150))
        self.img = customtkinter.CTkLabel(root, image=image1, text="1")
        self.img.grid(row=0, column=0, rowspan=3, padx=20, pady=20,)

        self.subfolders_checkbox = customtkinter.CTkCheckBox(
            root, text="Analizar Subcarpetas", variable=self.subfolders, text_color="#050505"
        )
        self.subfolders_checkbox.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        self.open_folder_checkbox = customtkinter.CTkCheckBox(
            root, text="Abrir carpeta al finalizar", variable=self.open_after_organize, text_color="#050505"
        )
        self.open_folder_checkbox.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        self.organize_button = customtkinter.CTkButton(
            root, text="Organizar", command=self.organize_files
        )
        self.organize_button.grid(row=2, column=1, padx=20, pady=20, sticky="ns")

    def on_close(self):
        print("Cerrando la aplicación")
        self.root.destroy()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as config_file:
                config_data = json.load(config_file)
                self.subfolders.set(config_data.get("subfolders", False))
                self.open_after_organize.set(config_data.get("open_after_organize", False))
                self.show_alert.set(config_data.get("show_alert", True))

    def save_config(self):
        config_data = {
            "subfolders": self.subfolders.get(),
            "open_after_organize": self.open_after_organize.get(),
            "show_alert": self.show_alert.get()
        }
        with open(self.config_file, "w") as config_file:
            json.dump(config_data, config_file)

    def organize_files(self):
        folder_to_organize = filedialog.askdirectory()
        if folder_to_organize:
            self.save_config()
            self.organize_files_in_folder(folder_to_organize)
            if self.open_after_organize.get():
                self.open_sortify_folder()

    def organize_files_in_folder(self, folder_path):
        extensions_mapping = {
            "Audios": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".mwa", ".aiff", ".midi"],
            "Video": [".mp4", ".mov", ".avi", ".mkv", ".fvl", ".webm", ".mpeg"],
            "Imágenes": [".png", ".jpg", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".jpeg"],
            "Documentos de Texto": [".pdf", ".docx", ".txt", ".rft", ".odt"],
            "Hojas de Cálculo": [".xlsx", ".csv", ".ods"],
            "Presentaciones": [".pptx", ".odp"],
            "Comprimidos": [".rar", ".zip", ".7z"],
            "Ejecutables": [".exe", ".bat", ".apk"],
            "Archivos de Datos": [".json", ".xml", ".csv"],
            "Proyectos": [".psd", ".ai", ".indd", ".veg", ".pdn", ".flp"],
        }

        for root_folder, _, files in os.walk(folder_path):
            for file in files:
                _, extension = os.path.splitext(file)
                for folder, valid_extensions in extensions_mapping.items():
                    if extension in valid_extensions:
                        destination_folder = os.path.join(os.getcwd(), folder)
                        os.makedirs(destination_folder, exist_ok=True)
                        file_path = os.path.join(root_folder, file)
                        self.move_file_with_unique_name(file_path, destination_folder)
                        break

        if self.subfolders.get():
            for root_folder, subfolders, _ in os.walk(folder_path):
                for subfolder in subfolders:
                    self.organize_files_in_folder(os.path.join(root_folder, subfolder))

        if not self.success_message_displayed:
            messagebox.showinfo("Éxito", "¡Organización de archivos completada con éxito!")
            self.success_message_displayed = True

    def move_file_with_unique_name(self, source, destination_folder):
        base_name = os.path.basename(source)
        destination_path = os.path.join(destination_folder, base_name)

        # add a number to the filename if it already exists
        count = 1
        while os.path.exists(destination_path):
            file_name, file_extension = os.path.splitext(base_name)
            new_base_name = f"{file_name}_{count}{file_extension}"
            destination_path = os.path.join(destination_folder, new_base_name)
            count += 1

        shutil.move(source, destination_path)

    def open_sortify_folder(self):
        os.startfile(os.getcwd())

    def show_alert_message(self):
        messagebox.showinfo("¡Advertencia!", "Este software, Sortify, se proporciona sin garantía y no puede ser vendido ni redistribuido. El programa tiene la capacidad de modificar la estructura de archivos y carpetas en tu computadora, lo que podría afectar el funcionamiento de otros programas, se recomienda usar con responsabilidad.")

    def on_close(self):
        print("Cerrando la aplicación")
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = Sortify(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
