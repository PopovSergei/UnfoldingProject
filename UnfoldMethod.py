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
