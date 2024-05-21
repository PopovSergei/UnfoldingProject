import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
from tkinter import ttk

from Baron import Baron
from DAgostini import DAgostini
from utils import DataOutput

migration_path = "resources/first_part2.txt"
data_path = "resources/second_part2.txt"
# migration_path = "resources/sim_p_2.txt"
# data_path = "resources/sim_p_2.txt"

d_agostini_str = "Д\'Агостини"
baron_str = "Барон"

algorithm = None
chk_btn_enabled = None
custom_bins = None

is_ready = False

d_agostini = DAgostini()
baron = Baron()

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
    global is_ready
    is_ready = False
    filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
    if filepath != "":
        global migration_path
        migration_path = filepath


def find_data_to_unfold():
    global is_ready
    is_ready = False
    filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
    if filepath != "":
        global data_path
        data_path = filepath


def find_result():
    global migration_path, data_path, is_ready
    try:
        user_custom_bins = int(custom_bins.get())

        if migration_path != "" and data_path != "":
            if algorithm.get() == d_agostini_str:
                d_agostini.real_init(migration_path, data_path, user_custom_bins)
            elif algorithm.get() == baron_str:
                baron.real_init(migration_path, data_path, user_custom_bins)
            is_ready = True
        elif migration_path == "":
            mb.showinfo("Информация", "Сначала укажите файл c данными\nдля построения матрицы миграций")
        elif data_path == "":
            mb.showinfo("Информация", "Сначала укажите файл c данными\nдля обратной свёртки")

    except ValueError:
        mb.showinfo("Информация", "Ошибка в задании бинов")


def show_result():
    if is_ready:
        if algorithm.get() == d_agostini_str:
            DataOutput.show_bar_chart(
                d_agostini.measured_array, d_agostini.result_array, d_agostini.true_array,
                'Measured', 'Result', 'True',
                'Bins', 'Events', d_agostini.bins
            )
    else:
        mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")


def show_migration_matrix():
    if is_ready:
        if algorithm.get() == d_agostini_str:
            DataOutput.show_matrix(d_agostini.migration_matrix, d_agostini.bins)
        elif algorithm.get() == baron_str:
            DataOutput.show_matrix(baron.migration_matrix, baron.bins)
    else:
        mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")


def draw_widgets():
    global algorithm, chk_btn_enabled, custom_bins
    algorithm = StringVar(value=d_agostini_str)
    chk_btn_enabled = IntVar(value=1)
    custom_bins = StringVar(value="0")

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
        text=d_agostini_str, font=custom_font, value=d_agostini_str, variable=algorithm,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=3, column=0, ipadx=6, ipady=6, padx=5, pady=5)
    Radiobutton(
        text=baron_str, font=custom_font, value=baron_str, variable=algorithm,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=3, column=1, ipadx=6, ipady=6, padx=5, pady=5)

    Label(
        text="Количество бинов (0-авто): ", font=custom_font,
        bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color
    ).grid(row=4, column=0, ipadx=6, ipady=6, padx=5, pady=5)

    Entry(
        font=custom_font, textvariable=custom_bins, width=10
    ).grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)

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
    def __init__(self):
        super().__init__()
        self.title("Обратная свёртка")
        self.geometry("500x400")
        self.resizable(False, False)
        self.config(bg=bg_color)

        for c in range(2):
            self.columnconfigure(index=c, weight=1)
        for r in range(8):
            self.rowconfigure(index=r, weight=1)

    def run(self):
        draw_widgets()
        self.mainloop()
