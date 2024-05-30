import math
import random

from utils import DataOutput, FileUsage


class UnfoldMethod:
    def __init__(self):
        # self.values = None  # Массив объектов с двумя полями trueVal и measuredVal
        self.bins = None  # Количество бинов
        self.intervals = None  # Значения верхних границ интервалов (бинов)
        self.migration_measured_array = None  # Массив с количеством событий, зарегестрированных в каждом бине (априор)
        self.migration_true_array = None  # Массив с количеством событий, которые должны были попость в каждый бин (апр)
        self.pre_migration_matrix = None  # Матрица до деления
        self.migration_matrix = None  # Матрица после деления
        self.measured_array = None  # Массив с количеством событий, зарегестрированных в каждом бине (апостериор)
        self.true_array = None  # Массив с количеством событий, которые должны были попость в каждый бин (апостериор)

    def init_migration_part(self, migration_path, binning_type, custom_bins, baron_style):
        # Получение априорных данных из файла, запись в values. Изменяется: values
        measured_val_array = []
        true_val_array = []
        self.values = FileUsage.read_file(migration_path, measured_val_array, true_val_array, False)
        self.bins = custom_bins
        self.set_intervals(binning_type, measured_val_array, true_val_array, True)
        self.binning()
        self.set_pre_migration_matrix(False)
        self.set_migration_matrix(baron_style, False)

    # Используются: values, bins. Изменяются: true_array, measured_array, pre_migration_matrix
    def set_pre_migration_matrix(self, print_result):
        self.migration_true_array = [0] * self.bins
        self.migration_measured_array = [0] * self.bins
        self.pre_migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for value in self.values:
            self.migration_true_array[value.trueVal] += 1
            self.migration_measured_array[value.measuredVal] += 1
            self.pre_migration_matrix[value.trueVal][value.measuredVal] += 1

        self.print_results("set_pre_migration_matrix", print_result)

    # Используются: values, bins, true_array или measured_array, pre_migration_matrix. Изменяются: migration_matrix
    def set_migration_matrix(self, baron_style, print_result):
        self.migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for i in range(self.bins):
            for j in range(self.bins):
                if not baron_style:
                    if self.migration_true_array[i] > 0:
                        self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.migration_true_array[i]
                else:
                    if self.migration_measured_array[j] > 0:
                        self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.migration_measured_array[j]

        self.print_results("set_migration_matrix", print_result)

    # Используются: values, bins. Изменяются: true_array, measured_array
    def set_arrays(self, print_result):
        self.true_array = [0] * self.bins
        self.measured_array = [0] * self.bins
        for value in self.values:
            self.true_array[value.trueVal] += 1
            self.measured_array[value.measuredVal] += 1

        self.print_results("set_arrays", print_result)

    # Задание интервалов. Используется, может сортироваться: values. Изменяются: bins, intervals
    def set_intervals(self, binning_type, measured_val_array, true_val_array, print_result):
        min_val = 100
        max_val = 0
        for value in self.values:
            min_val = min(min_val, value.measuredVal, value.trueVal)
            max_val = max(max_val, value.measuredVal, value.trueVal)
        min_val = math.floor(min_val)
        max_val = math.ceil(max_val)

        if self.bins == 0:
            self.bins = 40

        intervals = []
        interval = (max_val - min_val) / (math.ceil(self.bins / 2 * 1))
        interval_counter = interval + min_val

        while interval_counter <= max_val:
            intervals.append(interval_counter)
            interval_counter += interval

        for i in range(math.floor(self.bins / 2 * 1)):
            util_values = measured_val_array.copy()
            util_binning(util_values, intervals)

            measured_array = [0] * len(intervals)
            for value in util_values:
                measured_array[value] += 1
            max_interval = measured_array.index(max(measured_array))

            # max_interval = find_max_interval(util_values, intervals)
            interval_val = intervals[max_interval]
            if max_interval != 0:
                pre_interval_val = intervals[max_interval - 1]
            else:
                pre_interval_val = min_val
            pre_interval_val += (interval_val - pre_interval_val) / 2
            intervals.insert(max_interval, pre_interval_val)

        self.intervals = intervals
        self.print_results("set_intervals", print_result)

    def split_values(self, splitting):
        more_values = []
        for i in range(splitting):
            more_values.append([])
            for value in self.values:
                if random.randint(0, 2) < 2:
                    more_values[i].append(value)
        return more_values

    # Замена значений на номера бинов в values. Используется: intervals. Изменяется: values
    def binning(self):
        for value in self.values:
            value.measuredVal = find_interval(value.measuredVal, self.intervals)
            value.trueVal = find_interval(value.trueVal, self.intervals)

    def print_results(self, case, print_result):
        if not print_result:
            return
        if case == "set_pre_migration_matrix":
            DataOutput.print_matrix(self.pre_migration_matrix, self.bins, False)
            DataOutput.print_array("MigrationTrue:", self.migration_true_array)
            DataOutput.print_array("MigrationMeas:", self.migration_measured_array)
            print()
        elif case == "set_migration_matrix":
            DataOutput.print_matrix(self.migration_matrix, self.bins, True)
        elif case == "set_arrays":
            DataOutput.print_array("True:", self.true_array)
            DataOutput.print_array("Meas:", self.measured_array)
            print()
        elif case == "set_intervals":
            print("\n\n")
            print(f"Bins={self.bins}")
            DataOutput.print_array("Intervals:", self.intervals, 2)
            print()


def find_interval(value, intervals):
    for i, n in enumerate(intervals):
        if value <= n:
            return i
    return len(intervals) - 1


def find_max_interval(values, intervals):
    measured_array = [0] * len(intervals)
    for value in values:
        measured_array[value.measuredVal] += 1
    return measured_array.index(max(measured_array))


def util_binning(values, intervals):
    for i, value in enumerate(values):
        values[i] = find_interval(value, intervals)


def quick_sort(values, first, last):
    if first >= last:
        return
    i, j = first, last
    pivot = values[random.randint(first, last)]
    while i <= j:
        while values[i].measuredVal < pivot.measuredVal:
            i += 1
        while values[j].measuredVal > pivot.measuredVal:
            j -= 1
        if i <= j:
            values[i], values[j] = values[j], values[i]
            i, j = i + 1, j - 1
    quick_sort(values, first, j)
    quick_sort(values, i, last)
