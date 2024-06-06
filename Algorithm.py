from tkinter import *
from tkinter import messagebox as mb

from MigrationPart import MigrationPart
from UnfoldingPart import UnfoldingPart
from utils import DataOutput


class Algorithm:
    def __init__(self):
        self.have_result = False
        self.migration_part = None
        self.unfolding_part = None

    def run(self, params):
        if params.migration_path == "":
            mb.showinfo("Информация", "Сначала укажите файл c данными\nдля построения матрицы миграций")
            return
        elif params.unfolding_path == "":
            mb.showinfo("Информация", "Сначала укажите файл c данными\nдля обратной свёртки")
            return

        try:
            user_custom_bins = abs(int(params.custom_bins.get()))
            user_split_max = abs(int(params.split_max.get()))
            user_remove_min = abs(int(params.remove_min.get()))
            user_accuracy = abs(float(params.accuracy.get()))
            user_splitting = abs(int(params.splitting.get()))
        except ValueError:
            mb.showinfo("Информация", "Ошибка в полях ввода")
            return

        if user_custom_bins + user_split_max - user_remove_min < 1:
            mb.showinfo("Информация", "Неправильно заданы бины")
            return

        if user_custom_bins == 0:
            mb.showinfo("Информация", "Одинаковых бинов должно быть больше чем 0")
            return

        self.migration_part = MigrationPart(user_custom_bins, user_split_max, user_remove_min, params)
        if self.migration_part.bins is None:
            mb.showinfo("Информация", "Неправильно заданы интервалы")
            return

        self.unfolding_part = UnfoldingPart(self.migration_part, user_splitting, user_accuracy, params)
        self.have_result = True

        if not params.hand_intervals.get():
            params.intervals_entry.delete(0, END)
            params.intervals_entry.insert(0, DataOutput.array_to_string("", self.migration_part.intervals))
        self.text_result(params.text_area, self.migration_results_to_string(params))

    def text_result(self, text_area, migration_results_string):
        text = migration_results_string + self.unfolding_part.result_string
        if text != "":
            text += "\n"
        text_area.insert(END, text)

    def show_result(self, result_style):
        if self.check_not_ready():
            return

        if result_style.get():
            DataOutput.show_bar_charts(
                [self.migration_part.prior_measured_array, self.migration_part.prior_true_array,
                 self.unfolding_part.measured_array, self.unfolding_part.true_array, self.unfolding_part.result_array],
                ["Апр. Изм.", "Апр. Ист.", "Апост. Изм.", "Апост. Ист.", "Результат"],
                "Бины", "События", 0)
        else:
            DataOutput.show_bar_charts(
                [self.unfolding_part.measured_array, self.unfolding_part.true_array, self.unfolding_part.result_array],
                ["Апост. Изм.", "Апост. Ист.", "Результат"],
                "Бины", "События", 1
            )

    def show_iterations(self):
        if self.check_not_ready():
            return

        arrays = [[]]
        names = ["Апост. Изм."]
        for j in range(self.unfolding_part.bins):
            arrays[0].append(abs(self.unfolding_part.true_array[j] - self.unfolding_part.measured_array[j]))

        for i in range(len(self.unfolding_part.results)):
            names.append(f"{i}")
            arrays.append([])
            for j in range(self.unfolding_part.bins):
                arrays[i + 1].append(abs(self.unfolding_part.true_array[j] - self.unfolding_part.results[i][j]))

        DataOutput.show_bar_charts(arrays, names, "Бины", "Ошибочные события", 1)

    def show_migration_matrix(self):
        if self.check_not_ready():
            return
        DataOutput.show_matrix(self.migration_part.migration_matrix, self.migration_part.bins, False)

    def show_pre_migration_matrix(self):
        if self.check_not_ready():
            return
        DataOutput.show_matrix(self.migration_part.pre_migration_matrix, self.migration_part.bins, True)

    def show_intervals_stem(self):
        if self.check_not_ready():
            return
        bins_array = []
        for i in range(self.migration_part.bins):
            bins_array.append(i)
        DataOutput.show_stem(self.migration_part.intervals, bins_array, "Значения", "Бины")

    def calculate_fault(self):
        if self.check_not_ready():
            return

        sum_of_differences_result = 0
        sum_of_differences_measured = 0
        for i in range(self.unfolding_part.bins):
            sum_of_differences_result += abs(self.unfolding_part.result_array[i] - self.unfolding_part.true_array[i])
            sum_of_differences_measured += abs(
                self.unfolding_part.measured_array[i] - self.unfolding_part.true_array[i])
        result_fault = round(sum_of_differences_result / self.unfolding_part.bins, 4)
        measured_fault = round(sum_of_differences_measured / self.unfolding_part.bins, 4)
        if measured_fault != 0:
            efficiency = result_fault / (measured_fault / 100)
            efficiency = int(100 - round(efficiency, 0))
        else:
            efficiency = 0

        mb.showinfo("Погрешность",
                    f"Погрешность результата: {result_fault} событий\n" +
                    f"Погрешность измерения: {measured_fault} событий\n" +
                    f"Эффективность: {efficiency}%"
                    )

    def check_not_ready(self):
        if self.have_result is False:
            mb.showinfo("Информация", "Сначала укажите все параметры,\nнажмите пуск и дождитесь выполнения")
            return True
        else:
            return False

    def migration_results_to_string(self, params):
        result = ""
        if params.inter.get():
            result += f"Бины: {self.migration_part.bins}\n"
            result += DataOutput.array_to_string("Интервалы:", self.migration_part.intervals, 2)
            result += "\n"
        if params.prior_arr.get():
            result += DataOutput.array_to_string("Апр. ист.:", self.migration_part.prior_true_array)
            result += DataOutput.array_to_string("Апр. изм.:", self.migration_part.prior_measured_array)
            result += "\n"
        if params.pre_mig.get():
            result += DataOutput.matrix_to_string(
                self.migration_part.pre_migration_matrix, self.migration_part.bins, True)
        if params.mig.get():
            result += DataOutput.matrix_to_string(self.migration_part.migration_matrix, self.migration_part.bins, True)
        return result

