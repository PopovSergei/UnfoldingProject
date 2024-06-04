from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import threading

from Algorithm import Algorithm

# migration_path = "resources/test_1.txt"
# data_path = "resources/test_2.txt"
# migration_path = "resources/first_part2.txt"
# data_path = "resources/second_part2.txt"
# migration_path = "resources/sim_p_2.txt"
# data_path = "resources/sim_p_2.txt"


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Обратная свёртка")
        self.geometry("680x650")
        self.resizable(False, False)

        self.migration_path = "resources/first_half.txt"
        self.unfolding_path = "resources/second_half.txt"
        self.algorithm = Algorithm()

        for c in range(3):
            self.columnconfigure(index=c, weight=1)
        for r in range(11):
            self.rowconfigure(index=r, weight=1)

        self.custom_bins = StringVar(value="35")
        self.split_max = StringVar(value="5")
        self.remove_min = StringVar(value="0")
        self.accuracy = StringVar(value="0.05")
        self.splitting = StringVar(value="0")

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

        self.intervals_entry = None
        self.text_area = None
        self.start_btn = None

    def run(self):
        self.draw_menu()
        self.draw_widgets()
        self.mainloop()

    def draw_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        app_menu = Menu(menu, tearoff=0)
        app_menu.add_checkbutton(label="Отдельный поток", variable=self.thread)
        app_menu.add_separator()
        app_menu.add_command(label="Светлая тема", command=self.set_light_theme)
        app_menu.add_command(label="Тёмная тема", command=self.set_dark_theme)

        algorithm_menu = Menu(menu, tearoff=0)
        algorithm_menu.add_checkbutton(label="Подробный результат", variable=self.result_style)
        algorithm_menu.add_separator()
        algorithm_menu.add_checkbutton(label="Бины и интервалы", variable=self.inter)
        algorithm_menu.add_checkbutton(label="Апр. массивы", variable=self.prior_arr)
        algorithm_menu.add_checkbutton(label="Матрица премиграций", variable=self.pre_mig)
        algorithm_menu.add_checkbutton(label="Матрица миграций", variable=self.mig)
        algorithm_menu.add_separator()
        algorithm_menu.add_checkbutton(label="Апост. массивы", variable=self.post_arr)
        algorithm_menu.add_checkbutton(label="Матрица обр. свёртки", variable=self.unf)
        algorithm_menu.add_checkbutton(label="Результат", variable=self.res)
        algorithm_menu.add_checkbutton(label="Распределение", variable=self.dis)
        algorithm_menu.add_checkbutton(label="Хи квадрат", variable=self.chi)

        intervals_menu = Menu(menu, tearoff=0)
        intervals_menu.add_checkbutton(label="Ручные интервалы", variable=self.hand_intervals)
        intervals_menu.add_separator()
        intervals_menu.add_command(label="Очистить", command=lambda: self.intervals_entry.delete(0, END))

        menu.add_cascade(label="Приложение", menu=app_menu)
        menu.add_cascade(label="Вывод алгоритма", menu=algorithm_menu)
        menu.add_cascade(label="Интервалы", menu=intervals_menu)

    def draw_widgets(self):
        self.config(bg=self.bg_color)

        self.draw_label("Выберите данные для:", 0, 0, 2)
        self.draw_label("Результаты:", 0, 2)

        self.draw_button("Матрицы миграций", 1, 0, self.find_migration_path)
        self.draw_button("Обратной свёртки", 1, 1, self.find_unfolding_path)

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

        self.start_btn = Button(
            text="Пуск", border=0, font=self.custom_font, command=self.start_thread,
            bg=self.btn_bg_color, fg=self.btn_text_color, activebackground=self.active_btn_bg_color,
            activeforeground=self.active_btn_text_color
        )
        self.start_btn.grid(row=7, column=0, ipadx=self.ipad_x, ipady=self.ipad_y, padx=5, pady=5, sticky=EW)

        self.intervals_entry = Entry(font=self.text_area_font)
        self.intervals_entry.grid(row=7, column=1, columnspan=2,
                                  ipadx=self.ipad_x, ipady=self.ipad_x, padx=5, pady=5, sticky=EW)
        x_scroll = ttk.Scrollbar(orient="horizontal", command=self.intervals_entry.xview)
        x_scroll.grid(row=8, column=1, columnspan=2, sticky=EW)
        self.intervals_entry["xscrollcommand"] = x_scroll.set

        self.draw_button("Интервалы", 1, 2, self.algorithm.show_intervals_stem)

        self.draw_button("Матрица премигр.", 2, 2, self.algorithm.show_pre_migration_matrix)

        self.draw_button("Матрица миграций", 3, 2, self.algorithm.show_migration_matrix)

        self.draw_button("Общая погрешность", 4, 2, self.algorithm.calculate_fault)

        self.draw_button("Гист. итераций", 5, 2, self.algorithm.show_iterations)

        self.draw_button("Гист. результата", 6, 2, lambda: self.algorithm.show_result(self.result_style))

        self.text_area = Text(width=80, height=10, wrap="none", font=self.text_area_font)
        self.text_area.bind("<Key>", lambda event: self.ctrl_event(event))
        self.text_area.grid(row=9, column=0, rowspan=2, columnspan=3,
                            ipadx=self.ipad_x, ipady=self.ipad_x, padx=6, pady=6, sticky=NW)
        ys = ttk.Scrollbar(orient="vertical", command=self.text_area.yview)
        ys.grid(row=9, column=3, rowspan=2, sticky=NS)
        xs = ttk.Scrollbar(orient="horizontal", command=self.text_area.xview)
        xs.grid(row=11, column=0, columnspan=3, sticky=EW)
        self.text_area["yscrollcommand"] = ys.set
        self.text_area["xscrollcommand"] = xs.set

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
            content = self.text_area.selection_get()
            self.clipboard_clear()
            self.clipboard_append(content)
        return "break"

    def find_migration_path(self):
        filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
        if filepath != "":
            self.migration_path = filepath

    def find_unfolding_path(self):
        filepath = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
        if filepath != "":
            self.unfolding_path = filepath

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

    def start_thread(self):
        if self.thread.get():
            self.start_btn.config(state=DISABLED)
            thread = threading.Thread(target=self.start_algorithm)
            thread.start()
            self.check_thread(thread)
        else:
            self.start_algorithm()

    def start_algorithm(self):
        self.algorithm.run(
            self.migration_path, self.unfolding_path, self.custom_bins, self.split_max, self.remove_min, self.accuracy,
            self.splitting, self.text_area, self.inter.get(), self.prior_arr.get(), self.pre_mig.get(), self.mig.get(),
            self.post_arr.get(), self.unf.get(), self.res.get(), self.dis.get(), self.chi.get(),
            self.hand_intervals.get(), self.intervals_entry
        )

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.start_btn.config(state=NORMAL)
