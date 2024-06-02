from tkinter import *
from tkinter import filedialog

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


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Обратная свёртка")
        self.geometry("500x470")
        self.resizable(False, False)

        for c in range(2):
            self.columnconfigure(index=c, weight=1)
        for r in range(10):
            self.rowconfigure(index=r, weight=1)

        self.algorithm = StringVar(value=d_agostini_str)
        self.chk_btn_enabled = IntVar(value=1)
        self.custom_bins = StringVar(value="35")
        self.split_max = StringVar(value="5")
        self.remove_min = StringVar(value="0")
        self.accuracy = StringVar(value="0.05")
        self.splitting = StringVar(value="0")
        self.result_style = BooleanVar(value=True)

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

        self.draw_label("Выберите данные для:", 0, 0, 2)

        self.draw_button("Матрицы миграций", 1, 0, find_migration_data)
        self.draw_button("Обратной свёртки", 1, 1, find_data_to_unfold)

        # self.draw_label("Алгоритм:", 2, 0, 2)
        #
        # self.draw_radio_button(d_agostini_str, 3, 0, d_agostini_str, self.algorithm)
        # self.draw_radio_button(baron_str, 3, 1, baron_str, self.algorithm)

        self.draw_label("Одинаковые бины:", 2, 0)
        self.draw_entry(2, 1, self.custom_bins)

        self.draw_label("Разбить макс. бин", 3, 0)
        self.draw_label("Сложить мин. бин", 3, 1)

        self.draw_entry(4, 0, self.split_max)
        self.draw_entry(4, 1, self.remove_min)

        self.draw_label("Точность:", 5, 0)
        self.draw_entry(5, 1, self.accuracy)

        self.draw_label("Усреднение (0-без):", 6, 0)
        self.draw_entry(6, 1, self.splitting)

        self.draw_button("Пуск", 7, 0, lambda: d_agostini.run(
            migration_path, data_path, self.custom_bins, self.split_max, self.remove_min, self.accuracy, self.splitting
        ))
        self.draw_button("Гист итер", 7, 1, d_agostini.show_iterations)

        self.draw_button("Гистограмма результата", 8, 0, lambda: d_agostini.show_result(self.result_style))
        self.draw_button("Матрица миграций", 8, 1, d_agostini.show_migration_matrix)

        self.draw_button("Рассчитать погрешность", 9, 0, d_agostini.calculate_fault)
        self.draw_button("Матрица премигр.", 9, 1, d_agostini.show_pre_migration_matrix)

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
