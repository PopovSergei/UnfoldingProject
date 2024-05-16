import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
from tkinter import ttk
import numpy as np

from DAgostini import DAgostini
from utils import DataOutput

migration_path = "resources/first_part2.txt"
data_path = "resources/second_part2.txt"

d_agostini = "Д\'Агостини"
baron = "Барон"

algorithm = None
chk_btn_enabled = None

is_ready = False

DAgostini = DAgostini()

# bg_color = "#5d5780"
# text_color = "#99FD83"
# btn_bg_color = "#352D60"
# btn_text_color = "#FAE08D"
# active_btn_bg_color = "#443e66"
# active_btn_text_color = "#FAE08D"

bg_color = "#f1fafd"
text_color = "#313e43"
btn_bg_color = "#4A7AA5"
btn_text_color = "#B3E5F4"
active_btn_bg_color = "#6e95b7"
active_btn_text_color = "#B3E5F4"

custom_font = ("Comic Sans MS", 15, "bold")  # Arial


def find_migration_data():
    filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
    if filepath != "":
        global migration_path
        migration_path = filepath


def find_data_to_unfold():
    filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
    if filepath != "":
        global data_path
        data_path = filepath


def find_result():
    global migration_path, data_path, is_ready
    if migration_path != "" and data_path != "":
        DAgostini.real_init(migration_path, data_path, 0)
        is_ready = True
    elif migration_path == "":
        mb.showinfo("Информация", "Сначала укажите файл c данными\nдля построения матрицы миграций")
    elif data_path == "":
        mb.showinfo("Информация", "Сначала укажите файл c данными\nдля обратной свёртки")


def show_result():
    if is_ready:
        if algorithm.get() == d_agostini:
            DataOutput.show_bar_chart(
                DAgostini.measured_array, DAgostini.result_array, DAgostini.true_array,
                'Measured', 'Result', 'True',
                'Bins', 'Events', DAgostini.bins
            )
    else:
        mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")


def show_migration_matrix():
    if is_ready:
        if algorithm.get() == d_agostini:
            DataOutput.show_matrix(DAgostini.migration_matrix, DAgostini.bins)
    else:
        mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")

def draw_widgets():
    global algorithm, chk_btn_enabled
    algorithm = StringVar(value=d_agostini)
    chk_btn_enabled = IntVar(value=1)

    Label(
        text="Выберите данные для:", font=custom_font,
        bg=bg_color, fg=text_color
    ).grid(row=0, column=0, ipadx=6, ipady=6, padx=5, pady=5)
    Button(
        text="Матрицы миграций", border=0, font=custom_font, command=find_migration_data,
        bg=btn_bg_color, fg=btn_text_color, activebackground=active_btn_bg_color,
        activeforeground=active_btn_text_color
    ).grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=5)
    Button(
        text="Обратной свёртки", border=0, font=custom_font, command=find_data_to_unfold,
        bg=btn_bg_color, fg=btn_text_color, activebackground=active_btn_bg_color,
        activeforeground=active_btn_text_color
    ).grid(row=1, column=1, ipadx=6, ipady=6, padx=5, pady=5)

    Label(
        text="Выберите алгоритм: ", font=custom_font,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=2, column=0, ipadx=6, ipady=6, padx=5, pady=5)
    Radiobutton(
        text=d_agostini, font=custom_font, value=d_agostini, variable=algorithm,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=3, column=0, ipadx=6, ipady=6, padx=5, pady=5)
    Radiobutton(
        text=baron, font=custom_font, value=baron, variable=algorithm,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=3, column=1, ipadx=6, ipady=6, padx=5, pady=5)

    Label(
        text="Количество бинов (0-авто): ", font=custom_font,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=4, column=0, ipadx=6, ipady=6, padx=5, pady=5)

    Button(
        text="Пуск", border=0, font=custom_font, command=find_result,
        bg=btn_bg_color, fg=btn_text_color, activebackground=active_btn_bg_color,
        activeforeground=active_btn_text_color
    ).grid(row=5, column=0, ipadx=6, ipady=6, padx=5, pady=5)

    Button(
        text="Гистограмма результата", border=0, font=custom_font, command=show_result,
        bg=btn_bg_color, fg=btn_text_color, activebackground=active_btn_bg_color,
        activeforeground=active_btn_text_color
    ).grid(row=6, column=0, ipadx=6, ipady=6, padx=5, pady=5)
    Button(
        text="Матрица миграций", border=0, font=custom_font, command=show_migration_matrix,
        bg=btn_bg_color, fg=btn_text_color, activebackground=active_btn_bg_color,
        activeforeground=active_btn_text_color
    ).grid(row=6, column=1, ipadx=6, ipady=6, padx=5, pady=5)

    Checkbutton(
        text="Сравнить с истинным", font=custom_font, variable=chk_btn_enabled,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=7, column=0, ipadx=6, ipady=6, padx=5, pady=5)


class Window(Tk):
    def __init__(self, width, height, title="MyWindow", resizable=(False, False)):
        super().__init__()
        self.title(title)
        # self.geometry(f"{width}x{height}")
        self.geometry("500x400")
        self.resizable(resizable[0], resizable[1])
        self.config(bg=bg_color)

        for c in range(2):
            self.columnconfigure(index=c, weight=1)
        for r in range(8):
            self.rowconfigure(index=r, weight=1)

    def run(self):
        draw_widgets()
        self.mainloop()
