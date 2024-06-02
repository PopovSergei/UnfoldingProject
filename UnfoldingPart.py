import random

from utils import FileUsage, DataOutput


class UnfoldingPart:
    def __init__(self, data_path, bins, intervals, migration_matrix, splitting, accuracy):
        # Массив апостериорных объектов с (двумя) полями (trueVal) и measuredVal
        self.posterior_values = FileUsage.read_file(data_path, False)
        self.bins = bins
        self.intervals = intervals
        self.migration_matrix = migration_matrix
        self.posterior_binning()

        # Массив с количеством апостериорных событий, зарегестрированных в каждом бине
        self.measured_array = [0] * self.bins
        # Массив с количеством апостериорных событий, которые должны были попость в каждый бин
        self.true_array = [0] * self.bins
        self.set_posterior_arrays(True)

        self.efficiency_array = self.set_efficiency_array()
        self.unfolding_matrix = None
        self.result_array = None
        self.distribution_array = [1 / self.bins] * self.bins
        self.results = []

        if splitting == 0:
            self.d_agostini_algorithm(accuracy)
        else:
            util_true_array = self.true_array.copy()
            util_measured_array = self.measured_array.copy()
            util_values_len = len(self.posterior_values)
            results_array = [0] * self.bins

            values_array = self.split_values(splitting)
            for i in range(splitting):
                self.posterior_values = values_array[i]
                self.set_posterior_arrays(True)
                self.d_agostini_algorithm(accuracy)
                for j in range(self.bins):
                    results_array[j] += self.distribution_array[j]

            for i in range(self.bins):
                self.result_array[i] = results_array[i] / splitting * util_values_len
                self.true_array[i] = util_true_array[i]
                self.measured_array[i] = util_measured_array[i]

    # Замена значений на номера бинов в values. Используется: intervals.
    def posterior_binning(self):
        for value in self.posterior_values:
            value.measuredVal = find_interval(value.measuredVal, self.intervals)
            value.trueVal = find_interval(value.trueVal, self.intervals)
    
    # Используются: posterior_values, bins. Изменяются: true_array, measured_array
    def set_posterior_arrays(self, print_result):
        for value in self.posterior_values:
            self.true_array[value.trueVal] += 1
            self.measured_array[value.measuredVal] += 1

        if print_result:
            DataOutput.print_array("True:", self.true_array)
            DataOutput.print_array("Meas:", self.measured_array)
            print()

    def split_values(self, splitting):
        more_values = []
        for i in range(splitting):
            more_values.append([])
            for value in self.posterior_values:
                if random.randint(0, 2) < 2:
                    more_values[i].append(value)
        return more_values

    def d_agostini_algorithm(self, accuracy):
        new_chi_square = 100
        old_chi_square = 101

        while old_chi_square > new_chi_square > accuracy:
            self.set_unfolding_matrix()
            self.set_result_array(False)
            self.results.append(self.result_array.copy())
            old_distribution_array = self.distribution_array.copy()

            result_array_sum = sum(self.result_array)
            for j in range(self.bins):
                self.distribution_array[j] = self.result_array[j] / result_array_sum

            old_chi_square = new_chi_square
            new_chi_square = self.find_chi_square(old_distribution_array)

            self.print_algorithm_results(False, False, True, True, True, old_chi_square, new_chi_square)

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

    def set_result_array(self, use_eff):
        self.result_array = [0] * self.bins
        for i in range(self.bins):
            expected = 0
            for j in range(self.bins):
                expected += self.unfolding_matrix[j][i] * self.measured_array[j]
            if use_eff and self.efficiency_array[i] != 0:
                self.result_array[i] = (1 / self.efficiency_array[i]) * expected
            else:
                self.result_array[i] = expected

    def set_efficiency_array(self):
        efficiency_array = [0] * self.bins
        for j in range(self.bins):
            efficiency = 0
            for k in range(self.bins):
                efficiency += self.migration_matrix[k][j]
            efficiency_array[j] = efficiency
        return efficiency_array

    def print_algorithm_results(self, eff, unf, res, dis, chi, old_chi_square, new_chi_square):
        if eff:
            DataOutput.print_array("Efficiency:", self.efficiency_array, 2)
        if unf:
            DataOutput.print_matrix(self.unfolding_matrix, self.bins, True)
        if res:
            DataOutput.print_array("Res:", self.result_array, 2)
        if dis:
            DataOutput.print_array("Distribution:", self.distribution_array, 2)
        if chi:
            print(f"old_chi_square={round(old_chi_square, 4)}, new_chi_square={round(new_chi_square, 4)}\n")

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