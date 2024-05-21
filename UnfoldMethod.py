from utils import DataOutput


class UnfoldMethod:
    def __init__(self):
        self.values = None  # Массив объектов с двумя полями trueVal и measuredVal
        self.bins = None  # Количество бинов
        self.pre_migration_matrix = None  # Матрица до деления
        self.migration_matrix = None  # Матрица после деления
        self.measured_array = None  # Массив с количеством событий, зарегестрированных в каждом бине
        self.true_array = None  # Массив с количеством событий, которые должны были попость в каждый бин

    def set_pre_migration_matrix(self, print_result):
        self.true_array = [0] * self.bins
        self.measured_array = [0] * self.bins
        self.pre_migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for value in self.values:
            self.true_array[value.trueVal] = self.true_array[value.trueVal] + 1
            self.measured_array[value.measuredVal] = self.measured_array[value.measuredVal] + 1
            self.pre_migration_matrix[value.trueVal][value.measuredVal] = self.pre_migration_matrix[value.trueVal][
                                                                              value.measuredVal] + 1
        if print_result:
            DataOutput.print_matrix(self.pre_migration_matrix, self.bins, False)
            DataOutput.print_array("True:", self.true_array)
            DataOutput.print_array("Meas:", self.measured_array)
            print()

    def set_migration_matrix(self, print_result):
        self.migration_matrix = [[0] * self.bins for _ in range(self.bins)]
        for i in range(self.bins):
            for j in range(self.bins):
                if self.true_array[i] > 0:
                    self.migration_matrix[i][j] = self.pre_migration_matrix[i][j] / self.true_array[i]  # meas_array[j]

        if print_result:
            DataOutput.print_matrix(self.migration_matrix, self.bins, True)

    def set_arrays(self, print_result):
        self.true_array = [0] * self.bins
        self.measured_array = [0] * self.bins
        for value in self.values:
            self.true_array[value.trueVal] = self.true_array[value.trueVal] + 1
            self.measured_array[value.measuredVal] = self.measured_array[value.measuredVal] + 1

        if print_result:
            DataOutput.print_array("True:", self.true_array)
            DataOutput.print_array("Meas:", self.measured_array)
            print()

    def set_bins(self, custom_bins, print_result):
        max_measured = 0
        max_true = 0
        for value in self.values:
            max_measured = max(max_measured, value.measuredVal)
            max_true = max(max_true, value.trueVal)
        max_val = max(int(max_measured), int(max_true)) + 1

        if custom_bins == 0:
            for value in self.values:
                value.measuredVal = int(value.measuredVal)
                value.trueVal = int(value.trueVal)

            self.bins = max_val
            if print_result:
                print(f"maxMeasured={max_measured}, maxTrue={max_true}, bins={self.bins}")
                print()
        else:
            interval = max_val / custom_bins
            interval_counter = interval
            intervals = []
            while interval_counter <= max_val:
                intervals.append(interval_counter)
                interval_counter += interval

            for value in self.values:
                value.measuredVal = find_interval(value.measuredVal, intervals)
                value.trueVal = find_interval(value.trueVal, intervals)

            self.bins = custom_bins
            if print_result:
                print(f"maxMeasured={max_measured}, maxTrue={max_true}, max_val={self.bins}, bins={custom_bins}")
                DataOutput.print_array("Intervals:", intervals)
                print()


def find_interval(value, intervals):
    for i, n in enumerate(intervals):
        if value <= n:
            return i
    return len(intervals)
