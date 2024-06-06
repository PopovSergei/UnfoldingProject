import math
import random
from utils import FileUsage


class MigrationPart:
    def __init__(self, custom_bins, split_max, remove_min, params):
        # Массив априорных объектов с двумя полями trueVal и measuredVal
        self.prior_values = FileUsage.read_file(params.migration_path)
        self.bins = None  # Количество бинов
        self.intervals = None  # Значения верхних границ интервалов (бинов)
        if not params.hand_intervals.get():
            self.bins = custom_bins
            self.intervals = self.set_intervals(split_max, remove_min)
        else:
            if not self.find_bins_intervals(params.intervals_entry):
                return

        self.prior_binning()

        # Массив с количеством априорных событий, зарегестрированных в каждом бине
        self.prior_measured_array = [0] * self.bins
        # Массив с количеством априорных событий, которые должны были попость в каждый бин
        self.prior_true_array = [0] * self.bins
        # Матрица миграций до деления
        self.pre_migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        self.set_pre_migration_matrix()
        # Матрица миграций после деления
        self.migration_matrix = self.set_migration_matrix()

    # Используются: prior_values, bins. Изменяются: prior_true_array, prior_measured_array, pre_migration_matrix
    def set_pre_migration_matrix(self):
        for value in self.prior_values:
            self.prior_true_array[value.trueVal] += 1
            self.prior_measured_array[value.measuredVal] += 1
            self.pre_migration_matrix[value.trueVal][value.measuredVal] += 1

    # Используются: bins, prior_true_array или prior_measured_array, pre_migration_matrix. Изменяются: migration_matrix
    def set_migration_matrix(self):
        migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for i in range(self.bins):
            for j in range(self.bins):
                if self.prior_true_array[i] > 0:
                    migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.prior_true_array[i]
        return migration_matrix

    def find_bins_intervals(self, intervals_entry):
        intervals_string_array = intervals_entry.get().strip().split(" ")
        intervals = []
        try:
            for value in intervals_string_array:
                intervals.append(float(value))
        except ValueError:
            return False
        self.bins = len(intervals)
        self.intervals = intervals
        return True

    # Задание интервалов. Используется: prior_values. Изменяются: bins, intervals
    def set_intervals(self, split_max, remove_min):
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

        if split_max != 0 or remove_min != 0:
            measured_vals_array = get_measured_vals_array(self.prior_values)

            for i in range(split_max):
                intervals_correction("split", measured_vals_array.copy(), intervals, min_val)

            for i in range(remove_min):
                intervals_correction("remove", measured_vals_array.copy(), intervals, min_val)

        # Равномерный биннинг
        # elements_in_interval = int(len(self.prior_values) / self.bins)
        # interval_counter = elements_in_interval
        # for i in range(self.bins):
        #     intervals.append(interval_counter)
        #     interval_counter += elements_in_interval
        #
        # quick_sort(self.prior_values, 0, len(self.prior_values) - 1)
        #
        # for i in range(self.bins):
        #     intervals[i] = self.prior_values[intervals[i]].measuredVal
        # intervals[self.bins - 1] = max_val

        return intervals

    # Замена значений на номера бинов в values. Используется: intervals.
    def prior_binning(self):
        for value in self.prior_values:
            value.measuredVal = find_interval(value.measuredVal, self.intervals)
            value.trueVal = find_interval(value.trueVal, self.intervals)


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


def intervals_correction(case, measured_vals_array, intervals, min_val):
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
