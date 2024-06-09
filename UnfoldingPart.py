import math
import random
from tkinter import messagebox as mb

from utils import FileUsage, DataOutput
import numpy as np
from scipy.stats import norm


class UnfoldingPart:
    def __init__(self, migration_part, splitting, accuracy, params):
        # Массив апостериорных объектов с (двумя) полями (trueVal) и measuredVal
        self.posterior_values = FileUsage.read_file(params.unfolding_path)
        self.bins = migration_part.bins
        self.intervals = migration_part.intervals
        self.migration_matrix = migration_part.migration_matrix
        self.posterior_binning()

        self.result_string = ""

        # Массив с количеством апостериорных событий, зарегестрированных в каждом бине
        self.measured_array = [0] * self.bins
        # Массив с количеством апостериорных событий, которые должны были попость в каждый бин
        self.true_array = [0] * self.bins
        self.set_posterior_arrays(params.post_arr.get())

        self.unfolding_matrix = None
        self.result_array = None
        self.distribution_array = None
        self.results = []

        if splitting == 0:
            # params.norm_dis.set(value=False)
            self.d_agostini_algorithm(accuracy, params)
            # ravn_res = self.result_array.copy()
            # params.norm_dis.set(value=True)
            # self.d_agostini_algorithm(accuracy, params)
            # norm_res = self.result_array.copy()
            # arrays = [[]]
            # names = ["Измеренное"]
            # for j in range(self.bins):
            #     arrays[0].append(abs(self.true_array[j] - self.measured_array[j]))
            #
            # names.append("Нормальное")
            # arrays.append([])
            # for i in range(self.bins):
            #     arrays[1].append(abs(self.true_array[i] - norm_res[i]))
            # names.append("Равномерное")
            # arrays.append([])
            # for i in range(self.bins):
            #     arrays[2].append(abs(self.true_array[i] - ravn_res[i]))
            #
            # DataOutput.show_bar_charts(arrays, names, "Бины", "Ошибочные события", 1)
        else:
            util_measured_array = self.measured_array.copy()
            results_array = [0] * self.bins

            measured_vals = self.split_measured_vals(splitting)
            for i in range(splitting):
                measured_vals_array = measured_vals[i]
                self.set_measured_array(measured_vals_array, params.post_arr.get())
                self.d_agostini_algorithm(accuracy, params)
                for j in range(self.bins):
                    results_array[j] += self.distribution_array[j]

            for i in range(self.bins):
                self.result_array[i] = results_array[i] / splitting * len(self.posterior_values)
                self.measured_array[i] = util_measured_array[i]

    # Замена значений на номера бинов в values. Используется: intervals.
    def posterior_binning(self):
        for value in self.posterior_values:
            value.measuredVal = find_interval(value.measuredVal, self.intervals)
            value.trueVal = find_interval(value.trueVal, self.intervals)
    
    # Используются: posterior_values, bins. Изменяются: true_array, measured_array
    def set_posterior_arrays(self, post_arr):
        for value in self.posterior_values:
            self.true_array[value.trueVal] += 1
            self.measured_array[value.measuredVal] += 1

        if post_arr:
            self.result_string += DataOutput.array_to_string("Апост. ист.:", self.true_array)
            self.result_string += DataOutput.array_to_string("Апост. изм.:", self.measured_array)
            self.result_string += "\n"

    def set_measured_array(self, measured_vals_array, post_arr):
        self.measured_array = [0] * self.bins
        for value in measured_vals_array:
            self.measured_array[value] += 1

        if post_arr:
            if post_arr:
                self.result_string += DataOutput.array_to_string("Апост. изм. усред.:", self.measured_array)
                self.result_string += "\n"

    def split_measured_vals(self, splitting):
        measured_vals = []
        for i in range(splitting):
            measured_vals.append([])
            for value in self.posterior_values:
                if random.randint(0, 1) < 1:
                    measured_vals[i].append(value.measuredVal)
        return measured_vals

    def d_agostini_algorithm(self, accuracy, params):
        self.distribution_array = [1 / self.bins] * self.bins

        if params.norm_dis.get():
            x = np.arange(0, self.bins, 1)
            loc = self.measured_array.index(max(self.measured_array))
            scale = math.floor(self.bins / 3)
            self.distribution_array = norm.pdf(x, loc, scale)

            # meas_dis = [0] * self.bins
            # for i in range(self.bins):
            #     meas_dis[i] = self.measured_array[i] / sum(self.measured_array)

            # DataOutput.show_bar_charts([meas_dis, self.distribution_array], ["Meas", "Norm"], "Bins", "Vals", 1)

            # print(sum(self.distribution_array))
            percent = sum(self.distribution_array) / 100
            for i in range(self.bins):
                self.distribution_array[i] = self.distribution_array[i] / percent / 100
            # print(sum(self.distribution_array))

            # DataOutput.show_bar_charts([meas_dis, self.distribution_array, [1 / self.bins] * self.bins],
            #                            ["Измеренное", "Нормальное", "Равномерное"],
            #                            "Бины", "Вероятности", 1)

        new_chi_square = 100
        old_chi_square = 101

        while old_chi_square > new_chi_square > accuracy:
            self.set_unfolding_matrix()

            self.set_result_array()
            self.results.append(self.result_array.copy())

            old_distribution_array = self.distribution_array.copy()
            self.set_distribution_array()

            old_chi_square = new_chi_square
            new_chi_square = self.find_chi_square(old_distribution_array)

            self.print_algorithm_results(params, old_chi_square, new_chi_square)

    def set_unfolding_matrix(self):
        self.unfolding_matrix = [[0] * self.bins for _ in range(self.bins)]
        for i in range(self.bins):
            for j in range(self.bins):
                numerator = self.migration_matrix[i][j] * self.distribution_array[i]
                denominator = 0

                for k in range(self.bins):
                    sum_l = 0
                    for l in range(self.bins):
                        sum_l += self.migration_matrix[k][l] * self.distribution_array[l]
                    denominator += self.migration_matrix[k][j] * sum_l

                if denominator != 0:
                    self.unfolding_matrix[j][i] = numerator / denominator

    def set_result_array(self):
        self.result_array = [0] * self.bins
        for i in range(self.bins):
            for j in range(self.bins):
                self.result_array[i] += self.unfolding_matrix[j][i] * self.measured_array[j]

    def set_distribution_array(self):
        result_array_sum = sum(self.result_array)
        for j in range(self.bins):
            self.distribution_array[j] = self.result_array[j] / result_array_sum

    def find_chi_square(self, old_distribution):
        chi_square = 0
        for i in range(self.bins):
            if old_distribution[i] != 0:
                chi_square += ((self.distribution_array[i] - old_distribution[i]) ** 2) / old_distribution[i]
        return chi_square

    def print_algorithm_results(self, params, old_chi_square, new_chi_square):
        if params.unf.get():
            round_unf_matrix = None
            try:
                round_unf_matrix = int(params.round_unf_matrix.get())
                if round_unf_matrix == 0:
                    round_unf_matrix = None
            except ValueError:
                mb.showinfo("Информация", "Неправильное значение округления\nматрицы обратной свёртки")
            self.result_string += DataOutput.matrix_to_string(self.unfolding_matrix, self.bins, True, round_unf_matrix)

        if params.res.get():
            round_result = None
            try:
                round_result = int(params.round_result.get())
                if round_result == 0:
                    round_result = None
            except ValueError:
                mb.showinfo("Информация", "Неправильное значение округления результата")
            self.result_string += DataOutput.array_to_string("Результат:", self.result_array, round_result)

        if params.dis.get():
            round_distribution = None
            try:
                round_distribution = int(params.round_distribution.get())
                if round_distribution == 0:
                    round_distribution = None
            except ValueError:
                mb.showinfo("Информация", "Неправильное значение округления распределения")
            self.result_string += DataOutput.array_to_string(
                "Распределение:", self.distribution_array, round_distribution)

        if params.chi.get():
            round_chi = None
            try:
                round_chi = int(params.round_chi.get())
            except ValueError:
                mb.showinfo("Информация", "Неправильное значение округления хи квадрат")
            if round_chi != 0 and round_chi is not None:
                self.result_string += (f"Старый хи квадрат: {round(old_chi_square, round_chi)}, "
                                       f"новый хи квадрат: {round(new_chi_square, round_chi)}\n\n")
            else:
                self.result_string += (f"Старый хи квадрат: {old_chi_square}, "
                                       f"новый хи квадрат: {new_chi_square}\n\n")


def find_interval(value, intervals):
    for i, n in enumerate(intervals):
        if value <= n:
            return i
    return len(intervals) - 1
