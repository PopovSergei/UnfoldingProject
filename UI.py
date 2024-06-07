from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import threading

from Algorithm import Algorithm


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Обратная свёртка")
        self.geometry("1000x780")
        self.resizable(False, False)

        for c in range(5):
            self.columnconfigure(index=c, weight=1)
        for r in range(14):
            self.rowconfigure(index=r, weight=1)

        self.algorithm = Algorithm()
        self.params = AlgorithmParams()

        self.bg_color = "#f1fafd"
        self.text_color = "#313e43"
        self.btn_bg_color = "#4A7AA5"
        self.btn_text_color = "#B3E5F4"
        self.active_btn_bg_color = "#6e95b7"
        self.active_btn_text_color = "#B3E5F4"

        self.custom_font = ("Comic Sans MS", 14, "bold")  # Arial  Comic Sans MS  Tahoma
        self.text_area_font = ("Comic Sans MS", 10, "bold")  # Arial  Comic Sans MS  Tahoma
        self.ipad_x = 2
        self.ipad_y = 2

    def run(self):
        self.draw_menu()
        self.draw_widgets()
        self.mainloop()

    def draw_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        app_menu = Menu(menu, tearoff=0)
        app_menu.add_checkbutton(label="Отдельный поток", variable=self.params.thread)
        app_menu.add_separator()
        app_menu.add_command(label="Светлая тема", command=lambda: self.set_theme("light"))
        app_menu.add_command(label="Тёмная тема", command=lambda: self.set_theme("dark"))

        algorithm_menu = Menu(menu, tearoff=0)
        algorithm_menu.add_checkbutton(label="Подробный результат", variable=self.params.result_style)
        algorithm_menu.add_separator()
        algorithm_menu.add_checkbutton(label="Бины и интервалы", variable=self.params.inter)
        algorithm_menu.add_checkbutton(label="Апр. массивы", variable=self.params.prior_arr)
        algorithm_menu.add_checkbutton(label="Матрица премиграций", variable=self.params.pre_mig)
        algorithm_menu.add_checkbutton(label="Матрица миграций", variable=self.params.mig)
        algorithm_menu.add_separator()
        algorithm_menu.add_checkbutton(label="Апост. массивы", variable=self.params.post_arr)
        algorithm_menu.add_checkbutton(label="Матрица обр. свёртки", variable=self.params.unf)
        algorithm_menu.add_checkbutton(label="Результат", variable=self.params.res)
        algorithm_menu.add_checkbutton(label="Распределение", variable=self.params.dis)
        algorithm_menu.add_checkbutton(label="Хи квадрат", variable=self.params.chi)
        algorithm_menu.add_separator()
        algorithm_menu.add_command(label="Очистить", command=lambda: self.params.text_area.delete(1.0, END))

        intervals_menu = Menu(menu, tearoff=0)
        intervals_menu.add_checkbutton(label="Ручные интервалы", variable=self.params.hand_intervals)
        intervals_menu.add_separator()
        intervals_menu.add_command(label="Очистить", command=lambda: self.params.intervals_entry.delete(0, END))

        menu.add_cascade(label="Приложение", menu=app_menu)
        menu.add_cascade(label="Вывод алгоритма", menu=algorithm_menu)
        menu.add_cascade(label="Интервалы", menu=intervals_menu)

    def draw_widgets(self):
        self.config(bg=self.bg_color)

        # Column 0, 1

        self.draw_label("Выберите данные для:", 0, 0, 2)

        self.draw_button("Мат. миграций", 1, 0, self.find_migration_path)
        self.draw_button("Обр. свёртки", 1, 1, self.find_unfolding_path)

        self.draw_label("Одинаковые бины:", 2, 0)
        self.draw_entry(2, 1, self.params.custom_bins)

        self.draw_label("Разбить макс. бин:", 3, 0)
        self.draw_entry(3, 1, self.params.split_max)

        self.draw_label("Сложить мин. бин:", 4, 0)
        self.draw_entry(4, 1, self.params.remove_min)

        self.draw_label("Хи квадрат:", 5, 0)
        self.draw_entry(5, 1, self.params.accuracy)

        self.draw_label("Усреднение (0-без):", 6, 0)
        self.draw_entry(6, 1, self.params.splitting)

        self.draw_label("Интервалы:", 7, 0)
        self.params.intervals_entry = Entry(font=self.text_area_font)
        self.params.intervals_entry.grid(row=7, column=1, columnspan=2,
                                         ipadx=self.ipad_x, ipady=self.ipad_x, padx=5, pady=5, sticky=EW)
        x_scroll = ttk.Scrollbar(orient="horizontal", command=self.params.intervals_entry.xview)
        x_scroll.grid(row=8, column=1, columnspan=2, sticky=EW)
        self.params.intervals_entry["xscrollcommand"] = x_scroll.set

        # Column 2, 3

        self.draw_label("Округление вывода (0-без):", 0, 2, 2)

        self.draw_label("Интервалы:", 1, 2)
        self.draw_entry(1, 3, self.params.round_intervals)

        self.draw_label("Мат. миграций:", 2, 2)
        self.draw_entry(2, 3, self.params.round_mig_matrix)

        self.draw_label("Мат. обр. свёртки:", 3, 2)
        self.draw_entry(3, 3, self.params.round_unf_matrix)

        self.draw_label("Результат:", 4, 2)
        self.draw_entry(4, 3, self.params.round_result)

        self.draw_label("Распределение:", 5, 2)
        self.draw_entry(5, 3, self.params.round_distribution)

        self.draw_label("Хи квадрат:", 6, 2)
        self.draw_entry(6, 3, self.params.round_chi)

        self.params.start_btn = Button(
            text="Старт", border=0, font=self.custom_font, command=self.start_thread,
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        )
        self.params.start_btn.grid(row=7, column=3, ipadx=self.ipad_x, ipady=self.ipad_y, padx=5, pady=5, sticky=EW)

        # Column 4

        self.draw_label("Результаты:", 0, 4)

        self.draw_button("Интервалы", 1, 4, self.algorithm.show_intervals_stem)

        self.draw_button("Матрица премигр.", 2, 4, self.algorithm.show_pre_migration_matrix)

        self.draw_button("Матрица миграций", 3, 4, self.algorithm.show_migration_matrix)

        self.draw_button("Матрица обр. свёртки", 4, 4, self.algorithm.show_unfolding_matrix)

        self.draw_button("Общая погрешность", 5, 4, self.algorithm.calculate_fault)

        self.draw_button("Гист. итераций", 6, 4, self.algorithm.show_iterations)

        self.draw_button("Гист. результата", 7, 4, lambda: self.algorithm.show_result(self.params.result_style))

        # Text area

        self.params.text_area = Text(width=150, height=15, wrap="none", font=self.text_area_font)
        self.params.text_area.bind("<Key>", lambda event: self.ctrl_event(event))
        self.params.text_area.grid(row=9, column=0, rowspan=4, columnspan=5,
                                   ipadx=self.ipad_x, ipady=self.ipad_x, padx=6, pady=6, sticky=NW)
        ys = ttk.Scrollbar(orient="vertical", command=self.params.text_area.yview)
        ys.grid(row=9, column=5, rowspan=4, sticky=NS)
        xs = ttk.Scrollbar(orient="horizontal", command=self.params.text_area.xview)
        xs.grid(row=14, column=0, columnspan=5, sticky=EW)
        self.params.text_area["yscrollcommand"] = ys.set
        self.params.text_area["xscrollcommand"] = xs.set

    def draw_label(self, text, row, column, column_span=1):
        Label(
            text=text, font=self.custom_font, bg=self.bg_color, fg=self.text_color
        ).grid(row=row, column=column, columnspan=column_span,
               ipadx=self.ipad_x, ipady=self.ipad_y, padx=5, pady=5, sticky=EW)

    def draw_button(self, text, row, column, command):
        Button(
            text=text, border=0, font=self.custom_font, command=command,
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        ).grid(row=row, column=column, ipadx=self.ipad_x, ipady=self.ipad_y, padx=5, pady=5, sticky=EW)

    def draw_radio_button(self, text, row, column, value, variable):
        Radiobutton(
            text=text, font=self.custom_font, value=value, variable=variable,
            bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color
        ).grid(row=row, column=column, ipadx=self.ipad_x, ipady=self.ipad_y, padx=5, pady=5)

    def draw_entry(self, row, column, text_var):
        Entry(
            font=self.custom_font, textvariable=text_var, width=10
        ).grid(row=row, column=column, ipadx=self.ipad_x, ipady=self.ipad_y, padx=5, pady=5, sticky=EW)

    def ctrl_event(self, event):
        if event.state == 4 and event.keysym == 'c':
            content = self.params.text_area.selection_get()
            self.clipboard_clear()
            self.clipboard_append(content)
        return "break"

    def find_migration_path(self):
        filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
        if filepath != "":
            self.params.migration_path = filepath

    def find_unfolding_path(self):
        filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
        if filepath != "":
            self.params.unfolding_path = filepath

    def set_theme(self, theme):
        if theme == "light":
            self.bg_color = "#f1fafd"
            self.text_color = "#313e43"
            self.btn_bg_color = "#4A7AA5"
            self.btn_text_color = "#B3E5F4"
            self.active_btn_bg_color = "#6e95b7"
            self.active_btn_text_color = "#B3E5F4"
        else:
            self.bg_color = "#1E1E2E"
            self.text_color = "#F8C471"
            self.btn_bg_color = "#E74C3C"
            self.btn_text_color = "#2C3E50"
            self.active_btn_bg_color = "#C0392B"
            self.active_btn_text_color = "#2C3E50"

        intervals_entry_text = self.params.intervals_entry.get().strip()
        text_area_text = self.params.text_area.get(0.1, END).strip()
        if text_area_text != "":
            text_area_text += "\n\n\n"
        self.draw_widgets()
        self.params.intervals_entry.insert(0, intervals_entry_text)
        self.params.text_area.insert(0.1, text_area_text)

    def start_thread(self):
        if self.params.thread.get():
            self.params.start_btn.config(state=DISABLED)
            thread = threading.Thread(target=self.start_algorithm)
            thread.start()
            self.check_thread(thread)
        else:
            self.start_algorithm()

    def start_algorithm(self):
        self.algorithm.run(self.params)

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.params.start_btn.config(state=NORMAL)


class AlgorithmParams:
    def __init__(self):
        # migration_path = "resources/test_1.txt"
        # data_path = "resources/test_2.txt"
        # migration_path = "resources/first_part2.txt"
        # data_path = "resources/second_part2.txt"
        # migration_path = "resources/sim_p_2.txt"
        # data_path = "resources/sim_p_2.txt"

        # self.migration_path = "resources/first_part2.txt"
        # self.unfolding_path = "resources/second_part2.txt"
        self.migration_path = "resources/first_half.txt"
        self.unfolding_path = "resources/second_half.txt"

        self.custom_bins = StringVar(value="35")
        self.split_max = StringVar(value="5")
        self.remove_min = StringVar(value="0")
        self.accuracy = StringVar(value="0.05")
        self.splitting = StringVar(value="0")

        self.round_intervals = StringVar(value="4")
        self.round_mig_matrix = StringVar(value="2")
        self.round_unf_matrix = StringVar(value="2")
        self.round_result = StringVar(value="2")
        self.round_distribution = StringVar(value="4")
        self.round_chi = StringVar(value="4")

        self.thread = BooleanVar(value=False)

        self.result_style = BooleanVar(value=True)
        self.hand_intervals = BooleanVar(value=False)

        self.inter = BooleanVar(value=True)
        self.prior_arr = BooleanVar(value=False)
        self.pre_mig = BooleanVar(value=False)
        self.mig = BooleanVar(value=False)

        self.post_arr = BooleanVar(value=True)
        self.unf = BooleanVar(value=False)
        self.res = BooleanVar(value=True)
        self.dis = BooleanVar(value=True)
        self.chi = BooleanVar(value=True)

        self.intervals_entry = Entry()
        self.text_area = Text()
        self.start_btn = Button()
