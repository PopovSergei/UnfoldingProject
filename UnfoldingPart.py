import random

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
            self.d_agostini_algorithm(accuracy, params)
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

        # x = np.arange(0, self.bins, 1)
        # max_meas = self.measured_array.index(max(self.measured_array))
        #
        # sr_znach = sum(self.measured_array) / self.bins
        # bolsh = 0
        # for i in range(self.bins):
        #     if self.measured_array[i] > sr_znach:
        #         bolsh += 1
        # obsh = bolsh / self.bins * 10
        #
        # smf_str = self.bins / 1
        # self.distribution_array = norm.pdf(x, max_meas, smf_str)

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

    def print_algorithm_results(self, params, old_chi_square, new_chi_square):
        if params.unf.get():
            self.result_string += DataOutput.matrix_to_string(self.unfolding_matrix, self.bins, True)
        if params.res.get():
            self.result_string += DataOutput.array_to_string("Результат:", self.result_array, 2)
        if params.dis.get():
            self.result_string += DataOutput.array_to_string("Распределение:", self.distribution_array, 2)
        if params.chi.get():
            self.result_string += \
                f"Старый хи квадрат: {round(old_chi_square, 4)}, новый хи квадрат: {round(new_chi_square, 4)}\n\n"

    def find_chi_square(self, old_distribution):
        chi_square = 0
        for i in range(self.bins):
            if old_distribution[i] != 0:
                chi_square += ((self.distribution_array[i] - old_distribution[i]) ** 2) / old_distribution[i]
        return chi_square


def find_interval(value, intervals):
    for i, n in enumerate(intervals):
        if value <= n:
            return i
    return len(intervals) - 1
