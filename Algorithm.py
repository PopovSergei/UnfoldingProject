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

    def run(self, migration_path, data_path, custom_bins, split_max, remove_min, accuracy, splitting, text_area,
            inter, prior_arr, pre_mig, mig, post_arr, unf, res, dis, chi, hand_intervals, intervals_entry
            ):
        if migration_path == "":
            mb.showinfo("Информация", "Сначала укажите файл c данными\nдля построения матрицы миграций")
            return
        elif data_path == "":
            mb.showinfo("Информация", "Сначала укажите файл c данными\nдля обратной свёртки")
            return

        try:
            user_custom_bins = abs(int(custom_bins.get()))
            user_split_max = abs(int(split_max.get()))
            user_remove_min = abs(int(remove_min.get()))
            user_accuracy = abs(float(accuracy.get()))
            user_splitting = abs(int(splitting.get()))
        except ValueError:
            mb.showinfo("Информация", "Ошибка в полях ввода")
            return

        if user_custom_bins + user_split_max - user_remove_min < 1:
            mb.showinfo("Информация", "Неправильно заданы бины")
            return

        if user_custom_bins == 0:
            mb.showinfo("Информация", "Одинаковых бинов должно быть больше чем 0")
            return

        self.migration_part = MigrationPart(migration_path, user_custom_bins, user_split_max, user_remove_min,
                                            hand_intervals, intervals_entry)
        self.unfolding_part = UnfoldingPart(
            data_path, self.migration_part.bins, self.migration_part.intervals, self.migration_part.migration_matrix,
            user_splitting, user_accuracy, post_arr, unf, res, dis, chi)
        self.have_result = True

        if not hand_intervals:
            intervals_entry.delete(0, END)
            intervals_entry.insert(0, DataOutput.array_to_string("", self.migration_part.intervals))
        self.text_result(text_area, self.migration_results_to_string(inter, prior_arr, pre_mig, mig))

    def text_result(self, text_area, migration_results_string):
        text_area.insert(END, migration_results_string + self.unfolding_part.result_string)

    def show_result(self, result_style):
        if self.check_not_ready():
            return

        if result_style.get():
            DataOutput.show_bar_charts(
                [self.migration_part.prior_measured_array, self.migration_part.prior_true_array,
                 self.unfolding_part.measured_array, self.unfolding_part.true_array, self.unfolding_part.result_array],
                ["Априор. Изм.", "Априор. Ист.", "Измеренные", "Истинные", "Результат"],
                "Бины", "События", 0)
        else:
            DataOutput.show_bar_charts(
                [self.unfolding_part.measured_array, self.unfolding_part.true_array, self.unfolding_part.result_array],
                ["Измеренные", "Истинные", "Результат"],
                "Бины", "События", self.unfolding_part.bins
            )

    def show_iterations(self):
        if self.check_not_ready():
            return

        arrays = [[]]
        names = ["Измеренные"]
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
        DataOutput.show_stem(self.migration_part.intervals, bins_array, "Интервалы", "Бины")

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

    def migration_results_to_string(self, inter, prior_arr, pre_mig, mig):
        result = ""
        if inter:
            result += f"Бины: {self.migration_part.bins}\n"
            result += DataOutput.array_to_string("Интервалы:", self.migration_part.intervals, 2)
            result += "\n"
        if prior_arr:
            result += DataOutput.array_to_string("Апр. ист.:", self.migration_part.prior_true_array)
            result += DataOutput.array_to_string("Апр. изм.:", self.migration_part.prior_measured_array)
            result += "\n"
        if pre_mig:
            result += DataOutput.matrix_to_string(
                self.migration_part.pre_migration_matrix, self.migration_part.bins, True)
        if mig:
            result += DataOutput.matrix_to_string(self.migration_part.migration_matrix, self.migration_part.bins, True)
        return result

