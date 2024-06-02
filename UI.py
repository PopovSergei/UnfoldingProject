from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from Baron import Baron
from DAgostini import DAgostini

# migration_path = "resources/test_1.txt"
# data_path = "resources/test_2.txt"
# migration_path = "resources/first_part2.txt"
# data_path = "resources/second_part2.txt"
# migration_path = "resources/sim_p_2.txt"
# data_path = "resources/sim_p_2.txt"
migration_path = "resources/first_half.txt"
data_path = "resources/second_half.txt"

d_agostini_str = "Д\'Агостини"
baron_str = "Барон"

d_agostini = DAgostini()
baron = Baron()


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


def write_smf(editor):
    editor.insert(END, "\nBye World")  # вставка в конец


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Обратная свёртка")
        self.geometry("950x470")
        self.resizable(False, False)

        for c in range(3):
            self.columnconfigure(index=c, weight=1)
        for r in range(10):
            self.rowconfigure(index=r, weight=1)

        self.algorithm = StringVar(value=d_agostini_str)
        self.custom_bins = StringVar(value="35")
        self.split_max = StringVar(value="5")
        self.remove_min = StringVar(value="0")
        self.accuracy = StringVar(value="0.05")
        self.splitting = StringVar(value="0")

        self.result_style = BooleanVar(value=True)

        self.inter = BooleanVar(value=True)
        self.pre_mig = BooleanVar(value=False)
        self.mig = BooleanVar(value=False)

        self.arr = BooleanVar(value=True)
        self.unf = BooleanVar(value=False)
        self.res = BooleanVar(value=True)
        self.dis = BooleanVar(value=True)
        self.chi = BooleanVar(value=True)

        self.bg_color = "#f1fafd"
        self.text_color = "#313e43"
        self.btn_bg_color = "#4A7AA5"
        self.btn_text_color = "#B3E5F4"
        self.active_btn_bg_color = "#6e95b7"
        self.active_btn_text_color = "#B3E5F4"

        self.custom_font = ("Comic Sans MS", 15, "bold")  # Arial  Comic Sans MS  Tahoma
        self.text_area_font = ("Comic Sans MS", 10)  # Arial  Comic Sans MS  Tahoma

        self.text_area = None

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
        algorithm_menu.add_checkbutton(label="Подробный результат", variable=self.result_style)
        algorithm_menu.add_separator()
        algorithm_menu.add_checkbutton(label="Бины и интервалы", variable=self.inter)
        algorithm_menu.add_checkbutton(label="Матрица премиграций", variable=self.pre_mig)
        algorithm_menu.add_checkbutton(label="Матрица миграций", variable=self.mig)
        algorithm_menu.add_separator()
        algorithm_menu.add_checkbutton(label="Массивы ист. изм.", variable=self.arr)
        algorithm_menu.add_checkbutton(label="Матрица обратной свёртки", variable=self.unf)
        algorithm_menu.add_checkbutton(label="Результат", variable=self.res)
        algorithm_menu.add_checkbutton(label="Распределение", variable=self.dis)
        algorithm_menu.add_checkbutton(label="Хи квадрат", variable=self.chi)

        menu.add_cascade(label="Приложение", menu=app_menu)
        menu.add_cascade(label="Вывод алгоритма", menu=algorithm_menu)

    def draw_widgets(self):
        self.config(bg=self.bg_color)

        self.draw_label("Выберите данные для:", 0, 0, 2)

        self.draw_button("Матрицы миграций", 1, 0, find_migration_data)
        self.draw_button("Обратной свёртки", 1, 1, find_data_to_unfold)

        # self.draw_label("Алгоритм:", 2, 0, 2)
        #
        # self.draw_radio_button(d_agostini_str, 3, 0, d_agostini_str, self.algorithm)
        # self.draw_radio_button(baron_str, 3, 1, baron_str, self.algorithm)

        self.draw_label("Одинаковые бины:", 2, 0)
        self.draw_entry(2, 1, self.custom_bins)

        self.draw_label("Разбить макс. бин:", 3, 0)
        self.draw_entry(3, 1, self.split_max)

        self.draw_label("Сложить мин. бин:", 4, 0)
        self.draw_entry(4, 1, self.remove_min)

        self.draw_label("Точность:", 5, 0)
        self.draw_entry(5, 1, self.accuracy)

        self.draw_label("Усреднение (0-без):", 6, 0)
        self.draw_entry(6, 1, self.splitting)

        self.draw_button("Пуск", 7, 0, lambda: d_agostini.run(
            migration_path, data_path, self.custom_bins, self.split_max, self.remove_min, self.accuracy, self.splitting,
            self.text_area, self.inter.get(), self.pre_mig.get(), self.mig.get(), self.arr.get(), self.unf.get(),
            self.res.get(), self.dis.get(), self.chi.get()
        ))
        self.draw_button("Гист итер", 7, 1, d_agostini.show_iterations)

        self.draw_button("Гистограмма результата", 8, 0, lambda: d_agostini.show_result(self.result_style))
        self.draw_button("Матрица миграций", 8, 1, d_agostini.show_migration_matrix)

        self.draw_button("Рассчитать погрешность", 9, 0, d_agostini.calculate_fault)
        self.draw_button("Матрица премигр.", 9, 1, d_agostini.show_pre_migration_matrix)

        self.text_area = Text(width=53, height=27, wrap="none", font=self.text_area_font)
        self.text_area.grid(row=0, column=2, rowspan=11, columnspan=2, ipadx=6, ipady=6, padx=23, pady=23, sticky=NW)
        ys = ttk.Scrollbar(orient="vertical", command=self.text_area.yview)
        ys.grid(row=0, column=3, rowspan=10, sticky=NS)
        xs = ttk.Scrollbar(orient="horizontal", command=self.text_area.xview)
        xs.grid(row=10, column=2, columnspan=2, sticky=EW)
        self.text_area["yscrollcommand"] = ys.set
        self.text_area["xscrollcommand"] = xs.set

    def draw_label(self, text, row, column, column_span=1):
        Label(
            text=text, font=self.custom_font, bg=self.bg_color, fg=self.text_color
        ).grid(row=row, column=column, columnspan=column_span, ipadx=6, ipady=6, padx=5, pady=5)

    def draw_button(self, text, row, column, command):
        Button(
            text=text, border=0, font=self.custom_font, command=command,
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=row, column=column, ipadx=6, ipady=6, padx=5, pady=5)

    def draw_radio_button(self, text, row, column, value, variable):
        Radiobutton(
            text=text, font=self.custom_font, value=value, variable=variable,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=row, column=column, ipadx=6, ipady=6, padx=5, pady=5)

    def draw_entry(self, row, column, text_var):
        Entry(
            font=self.custom_font, textvariable=text_var, width=10
        ).grid(row=row, column=column, ipadx=6, ipady=6, padx=5, pady=5)

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
