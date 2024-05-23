import random

from utils import DataOutput, FileUsage


class UnfoldMethod:
    def __init__(self):
        self.values = None  # Массив объектов с двумя полями trueVal и measuredVal
        self.bins = None  # Количество бинов
        self.intervals = None  # Значения верхних границ интервалов (бинов)
        self.pre_migration_matrix = None  # Матрица до деления
        self.migration_matrix = None  # Матрица после деления
        self.measured_array = None  # Массив с количеством событий, зарегестрированных в каждом бине
        self.true_array = None  # Массив с количеством событий, которые должны были попость в каждый бин

    def init_migration_part(self, migration_path, custom_bins, baron_style):
        self.values = FileUsage.read_file(migration_path, False)
        self.bins = custom_bins
        self.set_bins(True)
        self.do_binning(custom_bins)
        self.set_pre_migration_matrix(False)
        self.set_migration_matrix(baron_style, False)

    # Используются: values, bins. Изменяются: true_array, measured_array, pre_migration_matrix
    def set_pre_migration_matrix(self, print_result):
        self.true_array = [0] * self.bins
        self.measured_array = [0] * self.bins
        self.pre_migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for value in self.values:
            self.true_array[value.trueVal] += 1
            self.measured_array[value.measuredVal] += 1
            self.pre_migration_matrix[value.trueVal][value.measuredVal] += 1

        self.print_results("set_pre_migration_matrix", print_result)

    # Используются: values, bins, true_array или measured_array, pre_migration_matrix. Изменяются: migration_matrix
    def set_migration_matrix(self, baron_style, print_result):
        self.migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for i in range(self.bins):
            for j in range(self.bins):
                if not baron_style:
                    if self.true_array[i] > 0:
                        self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.true_array[i]
                else:
                    if self.measured_array[j] > 0:
                        self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.measured_array[j]

        self.print_results("set_migration_matrix", print_result)

    # Используются: values, bins. Изменяются: true_array, measured_array
    def set_arrays(self, print_result):
        self.true_array = [0] * self.bins
        self.measured_array = [0] * self.bins
        for value in self.values:
            self.true_array[value.trueVal] += 1
            self.measured_array[value.measuredVal] += 1

        self.print_results("set_arrays", print_result)

    # Задание бинов. Используется, может сортироваться: values. Изменяются: bins, intervals
    def set_bins(self, print_result):
        max_measured = 0
        max_true = 0
        for value in self.values:
            max_measured = max(max_measured, value.measuredVal)
            max_true = max(max_true, value.trueVal)
        max_val = max(int(max_measured), int(max_true)) + 1

        if self.bins == 0:
            self.bins = max_val
        else:
            elements_in_interval = int(len(self.values) / self.bins)
            interval_counter = elements_in_interval
            intervals = []
            for i in range(self.bins):
                intervals.append(interval_counter)
                interval_counter += elements_in_interval

            quick_sort(self.values, 0, len(self.values) - 1)

            for i in range(self.bins):
                intervals[i] = self.values[intervals[i]].measuredVal
            intervals[self.bins - 1] = max_val

            self.intervals = intervals

        self.print_results("set_bins", print_result)

    def split_values(self, splitting):
        more_values = []
        for i in range(splitting):
            more_values.append([])
            for value in self.values:
                if random.randint(0, 1) == 1:
                    more_values[i].append(value)
        return more_values

    # Замена значений на номера бинов в values. Может использоваться: intervals. Изменяется: values
    def do_binning(self, custom_bins):
        if custom_bins == 0:
            self.old_binning()
        else:
            self.binning()

    def binning(self):
        for value in self.values:
            value.measuredVal = find_interval(value.measuredVal, self.intervals)
            value.trueVal = find_interval(value.trueVal, self.intervals)

    def old_binning(self):
        for value in self.values:
            value.measuredVal = int(value.measuredVal)
            value.trueVal = int(value.trueVal)

    def print_results(self, case, print_result):
        if not print_result:
            return
        if case == "set_pre_migration_matrix":
            DataOutput.print_matrix(self.pre_migration_matrix, self.bins, False)
            self.print_results("set_arrays", True)
        elif case == "set_migration_matrix":
            DataOutput.print_matrix(self.migration_matrix, self.bins, True)
        elif case == "set_arrays":
            DataOutput.print_array("True:", self.true_array)
            DataOutput.print_array("Meas:", self.measured_array)
            print()
        elif case == "set_bins":
            print("\n\n")
            print(f"Bins={self.bins}")
            if self.intervals is not None:
                DataOutput.print_array("Intervals:", self.intervals)
            print()


def find_interval(value, intervals):
    for i, n in enumerate(intervals):
        if value <= n:
            return i
    return len(intervals) - 1


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
