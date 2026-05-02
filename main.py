import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        # История паролей
        self.history = []
        self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля (8-64):").pack(pady=5)
        self.length_scale = ttk.Scale(
            self.root,
            from_=8,
            to=64,
            orient=tk.HORIZONTAL
        )
        self.length_scale.set(12)
        self.length_scale.pack(pady=5, fill=tk.X, padx=20)

        # Чекбоксы для выбора символов
        self.digits_var = tk.BooleanVar(value=True)
        self.letters_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.digits_var).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Буквы (a-Z)", variable=self.letters_var).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$%)", variable=self.special_var).pack(anchor=tk.W, padx=20)

        # Кнопка генерации
        self.generate_btn = ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_btn.pack(pady=10)

        # Поле отображения пароля
        self.password_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.password_var, font=("Courier", 12), state="readonly").pack(fill=tk.X, padx=20, pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(anchor=tk.W, padx=20, pady=(10, 0))
        columns = ("ID", "Пароль", "Длина", "Символы")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, padx=20, pady=5, expand=True)

        # Заполнение истории
        self.refresh_history_table()

    def generate_password(self):
        length = int(self.length_scale.get())

        # Проверка минимальной длины
        if length < 8:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 8 символов")
            return

        # Формирование набора символов
        chars = ""
        if self.digits_var.get():
            chars += string.digits
        if self.letters_var.get():
            chars += string.ascii_letters
        if self.special_var.get():
            chars += "!@#$%^&*"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавление в историю
        symbols_used = ""
        if self.digits_var.get(): symbols_used += "Цифры "
        if self.letters_var.get(): symbols_used += "Буквы "
        if self.special_var.get(): symbols_used += "Спец "

        self.history.append({
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "symbols": symbols_used.strip()
        })

        self.save_history()
        self.refresh_history_table()

    def refresh_history_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for record in self.history:
            self.tree.insert("", tk.END, values=(
                record["id"],
                record["password"],
                record["length"],
                record["symbols"]
            ))

    def save_history(self):
        with open("password_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def load_history(self):
        try:
            if os.path.exists("password_history.json"):
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
            self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

