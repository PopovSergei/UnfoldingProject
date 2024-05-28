from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb

from Baron import Baron
from DAgostini import DAgostini
from utils import DataOutput

# migration_path = "resources/test_1.txt"
# data_path = "resources/test_2.txt"
migration_path = "resources/first_part2.txt"
data_path = "resources/second_part2.txt"
# migration_path = "resources/sim_p_2.txt"
# data_path = "resources/sim_p_2.txt"

d_agostini_str = "Д\'Агостини"
baron_str = "Барон"

d_agostini = DAgostini()
baron = Baron()


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


def find_result(algorithm, binning_type, custom_bins, splitting):
    try:
        user_custom_bins = int(custom_bins.get())
        user_splitting = int(splitting.get())
    except ValueError:
        mb.showinfo("Информация", "Ошибка в задании бинов или усреднения")
        return

    if migration_path != "" and data_path != "":
        if algorithm.get() == d_agostini_str:
            d_agostini.real_init(migration_path, data_path, binning_type.get(), user_custom_bins, user_splitting)
        elif algorithm.get() == baron_str:
            baron.real_init(migration_path, data_path, user_custom_bins)
    elif migration_path == "":
        mb.showinfo("Информация", "Сначала укажите файл c данными\nдля построения матрицы миграций")
    elif data_path == "":
        mb.showinfo("Информация", "Сначала укажите файл c данными\nдля обратной свёртки")


def show_result(algorithm, result_style):
    if check_not_ready(algorithm.get()):
        return

    if algorithm.get() == d_agostini_str:
        if result_style.get():
            DataOutput.show_bar_chart_5(
                d_agostini.migration_measured_array, d_agostini.migration_true_array,
                d_agostini.measured_array, d_agostini.true_array, d_agostini.result_array,
                'MigMeasured', 'MigTrue',
                'Measured', 'True', 'Result',
                d_agostini.bins
            )
        else:
            DataOutput.show_bar_chart(
                d_agostini.measured_array, d_agostini.result_array, d_agostini.true_array,
                'Measured', 'Result', 'True',
                'Bins', 'Events', d_agostini.bins
            )


def show_migration_matrix(algorithm):
    if check_not_ready(algorithm.get()):
        return

    if algorithm.get() == d_agostini_str:
        DataOutput.show_matrix(d_agostini.migration_matrix, d_agostini.bins)
    elif algorithm.get() == baron_str:
        DataOutput.show_matrix(baron.migration_matrix, baron.bins)


def show_pre_migration_matrix(algorithm):
    if check_not_ready(algorithm.get()):
        return

    if algorithm.get() == d_agostini_str:
        DataOutput.show_matrix(d_agostini.pre_migration_matrix, d_agostini.bins)
    elif algorithm.get() == baron_str:
        DataOutput.show_matrix(baron.pre_migration_matrix, baron.bins)


def calculate_fault(algorithm):
    if check_not_ready(algorithm.get()):
        return

    if algorithm.get() == d_agostini_str:
        sum_of_differences_result = 0
        sum_of_differences_measured = 0
        for i in range(d_agostini.bins):
            sum_of_differences_result += abs(d_agostini.result_array[i] - d_agostini.true_array[i])
            sum_of_differences_measured += abs(d_agostini.measured_array[i] - d_agostini.true_array[i])
        result_fault = round(sum_of_differences_result / d_agostini.bins, 4)
        measured_fault = round(sum_of_differences_measured / d_agostini.bins, 4)
        efficiency = result_fault / (measured_fault / 100)
        efficiency = int(100 - round(efficiency, 0))
        mb.showinfo("Погрешность",
                    f"Погрешность результата: {result_fault} событий\n" +
                    f"Погрешность измерения: {measured_fault} событий\n" +
                    f"Эффективность: {efficiency}%"
                    )
    elif algorithm.get() == baron_str:
        mb.showinfo("Погрешность", "Пока нет")


def check_not_ready(algorithm):
    if algorithm == d_agostini_str:
        if d_agostini.bins is None:
            mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")
            return True
    elif algorithm == baron_str:
        if baron.bins is None:
            mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")
            return True
    return False


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Обратная свёртка")
        self.geometry("500x470")
        self.resizable(False, False)

        for c in range(2):
            self.columnconfigure(index=c, weight=1)
        for r in range(11):
            self.rowconfigure(index=r, weight=1)

        self.algorithm = StringVar(value=d_agostini_str)
        self.chk_btn_enabled = IntVar(value=1)
        self.custom_bins = StringVar(value="0")
        self.splitting = StringVar(value="0")
        self.result_style = BooleanVar(value=True)
        self.binning_type = BooleanVar(value=True)

        self.bg_color = "#f1fafd"
        self.text_color = "#313e43"
        self.btn_bg_color = "#4A7AA5"
        self.btn_text_color = "#B3E5F4"
        self.active_btn_bg_color = "#6e95b7"
        self.active_btn_text_color = "#B3E5F4"

        self.custom_font = ("Comic Sans MS", 15, "bold")  # Arial  Comic Sans MS  Tahoma

    def run(self):
        self.draw_menu()
        self.draw_widgets()
        self.mainloop()

    def draw_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        app_menu = Menu(menu, tearoff=0)
        app_menu.add_command(label="Светлая тема", command=self.set_light_theme)
        app_menu.add_command(label="Тёмная тема", command=self.set_dark_theme)

        algorithm_menu = Menu(menu, tearoff=0)
        algorithm_menu.add_checkbutton(label="Подробный результат", onvalue=1, offvalue=0, variable=self.result_style)

        menu.add_cascade(label="Приложение", menu=app_menu)
        menu.add_cascade(label="Алгоритм", menu=algorithm_menu)

    def draw_widgets(self):
        self.config(bg=self.bg_color)

        Label(
            text="Выберите данные для:", font=self.custom_font,
            bg=self.bg_color, fg=self.text_color
        ).grid(row=0, column=0, columnspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        Button(
            text="Матрицы миграций", border=0, font=self.custom_font,
            command=find_migration_data,
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Button(
            text="Обратной свёртки", border=0, font=self.custom_font,
            command=find_data_to_unfold,
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=1, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        Label(
            text="Алгоритм: ", font=self.custom_font,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=2, column=0, columnspan=2,  ipadx=6, ipady=6, padx=5, pady=5)
        Radiobutton(
            text=d_agostini_str, font=self.custom_font, value=d_agostini_str, variable=self.algorithm,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=3, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Radiobutton(
            text=baron_str, font=self.custom_font, value=baron_str, variable=self.algorithm,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=3, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        Label(
            text="Тип биннинга: ", font=self.custom_font,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=4, column=0, columnspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        Radiobutton(
            text="Одинаковый", font=self.custom_font, value=True, variable=self.binning_type,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=5, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Radiobutton(
            text="Равномерный", font=self.custom_font, value=False, variable=self.binning_type,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        Label(
            text="Бины (0-авто): ", font=self.custom_font,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=6, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Entry(
            font=self.custom_font, textvariable=self.custom_bins, width=10
        ).grid(row=6, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        Label(
            text="Усреднение (0-без): ", font=self.custom_font,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=7, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Entry(
            font=self.custom_font, textvariable=self.splitting, width=10
        ).grid(row=7, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        Button(
            text="Пуск", border=0, font=self.custom_font,
            command=lambda: find_result(self.algorithm, self.binning_type, self.custom_bins, self.splitting),
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=8, column=0, ipadx=6, ipady=6, padx=5, pady=5)

        Button(
            text="Гистограмма результата", border=0, font=self.custom_font,
            command=lambda: show_result(self.algorithm, self.result_style),
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=9, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Button(
            text="Матрица миграций", border=0, font=self.custom_font,
            command=lambda: show_migration_matrix(self.algorithm),
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=9, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        Button(
            text="Рассчитать погрешность", border=0, font=self.custom_font,
            command=lambda: calculate_fault(self.algorithm),
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=10, column=0, ipadx=6, ipady=6, padx=5, pady=5)
        Button(
            text="Матрица премигр.", border=0, font=self.custom_font,
            command=lambda: show_pre_migration_matrix(self.algorithm),
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=10, column=1, ipadx=6, ipady=6, padx=5, pady=5)

    def set_light_theme(self):
        self.bg_color = "#f1fafd"
        self.text_color = "#313e43"
        self.btn_bg_color = "#4A7AA5"
        self.btn_text_color = "#B3E5F4"
        self.active_btn_bg_color = "#6e95b7"
        self.active_btn_text_color = "#B3E5F4"
        self.draw_widgets()

    def set_dark_theme(self):
        self.bg_color = "#1E1E2E"
        self.text_color = "#F8C471"
        self.btn_bg_color = "#E74C3C"
        self.btn_text_color = "#2C3E50"
        self.active_btn_bg_color = "#C0392B"
        self.active_btn_text_color = "#2C3E50"
        self.draw_widgets()
