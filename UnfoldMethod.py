import math
import random

from utils import DataOutput, FileUsage


class UnfoldMethod:
    def __init__(self):
        self.prior_values = None  # Массив априорных объектов с двумя полями trueVal и measuredVal
        self.posterior_values = None  # Массив апостериорных объектов с (двумя) полями (trueVal) и measuredVal
        self.bins = None  # Количество бинов
        self.intervals = None  # Значения верхних границ интервалов (бинов)
        self.prior_measured_array = None  # Массив с количеством событий, зарегестрированных в каждом бине (априор)
        self.prior_true_array = None  # Массив с количеством событий, которые должны были попость в каждый бин (апр)
        self.pre_migration_matrix = None  # Матрица до деления
        self.migration_matrix = None  # Матрица после деления
        self.measured_array = None  # Массив с количеством событий, зарегестрированных в каждом бине (апостериор)
        self.true_array = None  # Массив с количеством событий, которые должны были попость в каждый бин (апостериор)

    def init_migration_part(self, migration_path, binning_type, custom_bins, split_max, remove_min, baron_style):
        # Получение априорных данных из файла, запись в prior_values. Изменяется: prior_values
        self.prior_values = FileUsage.read_file(migration_path, False)
        self.bins = custom_bins
        self.set_intervals(binning_type, split_max, remove_min)
        self.binning(self.prior_values)
        self.set_pre_migration_matrix()
        self.set_migration_matrix(baron_style)

        self.print_migration_results(True, False, False)

    # Используются: prior_values, bins. Изменяются: prior_true_array, prior_measured_array, pre_migration_matrix
    def set_pre_migration_matrix(self):
        self.prior_true_array = [0] * self.bins
        self.prior_measured_array = [0] * self.bins
        self.pre_migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for value in self.prior_values:
            self.prior_true_array[value.trueVal] += 1
            self.prior_measured_array[value.measuredVal] += 1
            self.pre_migration_matrix[value.trueVal][value.measuredVal] += 1

    # Используются: bins, prior_true_array или prior_measured_array, pre_migration_matrix. Изменяются: migration_matrix
    def set_migration_matrix(self, baron_style):
        self.migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for i in range(self.bins):
            for j in range(self.bins):
                if not baron_style:
                    if self.prior_true_array[i] > 0:
                        self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.prior_true_array[i]
                else:
                    if self.prior_measured_array[j] > 0:
                        self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.prior_measured_array[j]

    # Используются: posterior_values, bins. Изменяются: true_array, measured_array
    def set_posterior_arrays(self, print_result):
        self.true_array = [0] * self.bins
        self.measured_array = [0] * self.bins
        for value in self.posterior_values:
            self.true_array[value.trueVal] += 1
            self.measured_array[value.measuredVal] += 1

        if print_result:
            DataOutput.print_array("True:", self.true_array)
            DataOutput.print_array("Meas:", self.measured_array)
            print()

    # Задание интервалов. Используется: prior_values. Изменяются: bins, intervals
    def set_intervals(self, binning_type, split_max, remove_min):
        min_val = 100
        max_val = 0
        for value in self.prior_values:
            min_val = min(min_val, value.measuredVal, value.trueVal)
            max_val = max(max_val, value.measuredVal, value.trueVal)
        min_val = math.floor(min_val)
        max_val = math.ceil(max_val)

        intervals = []
        interval = (max_val - min_val) / self.bins
        interval_counter = interval + min_val

        self.bins = self.bins + split_max - remove_min

        while round(interval_counter, 5) <= max_val:
            intervals.append(interval_counter)
            interval_counter += interval

        for i in range(split_max):
            intervals_correction("split", self.prior_values, intervals, min_val)

        for i in range(remove_min):
            intervals_correction("remove", self.prior_values, intervals, min_val)

        self.intervals = intervals

    def split_values(self, splitting):
        more_values = []
        for i in range(splitting):
            more_values.append([])
            for value in self.posterior_values:
                if random.randint(0, 2) < 2:
                    more_values[i].append(value)
        return more_values

    # Замена значений на номера бинов в values. Используется: intervals.
    def binning(self, values):
        for value in values:
            value.measuredVal = find_interval(value.measuredVal, self.intervals)
            value.trueVal = find_interval(value.trueVal, self.intervals)

    def print_migration_results(self, inter, pre_mig, mig):
        if inter:
            print("\n\n")
            print(f"Bins={self.bins}")
            DataOutput.print_array("Intervals:", self.intervals, 2)
            print()
        if pre_mig:
            DataOutput.print_matrix(self.pre_migration_matrix, self.bins, False)
            DataOutput.print_array("MigrationTrue:", self.prior_true_array)
            DataOutput.print_array("MigrationMeas:", self.prior_measured_array)
            print()
        if mig:
            DataOutput.print_matrix(self.migration_matrix, self.bins, True)


def find_interval(value, intervals):
    for i, n in enumerate(intervals):
        if value <= n:
            return i
    return len(intervals) - 1


def util_binning(values, intervals):
    for i, value in enumerate(values):
        values[i] = find_interval(value, intervals)


def get_measured_vals_array(values):
    measured_val_array = []
    for value in values:
        measured_val_array.append(value.measuredVal)
    return measured_val_array


def intervals_correction(case, prior_values, intervals, min_val):
    measured_vals_array = get_measured_vals_array(prior_values)
    util_binning(measured_vals_array, intervals)

    measured_array = [0] * len(intervals)
    for value in measured_vals_array:
        measured_array[value] += 1
    max_interval = measured_array.index(max(measured_array))
    min_interval = measured_array.index(min(measured_array))

    if case == "split":
        split_max_interval(intervals, max_interval, min_val)
    elif case == "remove":
        remove_min_interval(intervals, min_interval, measured_array)


def remove_min_interval(intervals, min_interval, measured_array):
    if min_interval == 0:
        intervals.pop(0)
    elif min_interval == len(intervals) - 1:
        intervals.pop(-2)
    elif measured_array[min_interval - 1] < measured_array[min_interval + 1]:
        intervals.pop(min_interval - 1)
    else:
        intervals.pop(min_interval)


def split_max_interval(intervals, max_interval, min_val):
    interval_val = intervals[max_interval]
    if max_interval != 0:
        pre_interval_val = intervals[max_interval - 1]
    else:
        pre_interval_val = min_val
    pre_interval_val += (interval_val - pre_interval_val) / 2
    intervals.insert(max_interval, pre_interval_val)