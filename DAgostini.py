from UnfoldMethod import UnfoldMethod
from utils import DataOutput
from utils import FileUsage


class DAgostini(UnfoldMethod):
    def __init__(self):
        super().__init__()
        self.result_array = None

    def real_init(self, migration_path, data_path, custom_bins=0, splitting=0):
        self.values = FileUsage.read_file(migration_path, False)
        super().set_bins(custom_bins, True)

        super().set_pre_migration_matrix(False)
        super().set_migration_matrix(False)

        self.values = FileUsage.read_file(data_path, False)

        if splitting == 0:
            super().set_bins(custom_bins, True)
            super().set_arrays(True)
            self.result_array = set_result(self.migration_matrix, self.measured_array, self.bins)
        else:
            self.result_array = [0] * self.bins
            more_values = super().split_values(splitting)
            for i in range(splitting):
                self.values = more_values[i]
                super().set_bins(custom_bins, True)
                super().set_arrays(True)
                # self.result_array = set_result(self.migration_matrix, self.measured_array, self.bins)
                pre_result = set_result(self.migration_matrix, self.measured_array, self.bins)
                for j in range(self.bins):
                    self.result_array[j] += pre_result[j]
            self.values = FileUsage.read_file(data_path, False)
            super().set_bins(custom_bins, True)
            super().set_arrays(True)


def set_result(migration_matrix, measured_array, bins):
    efficiency_array = [0] * bins
    get_efficiency_array(efficiency_array, migration_matrix, bins, True)

    distribution = [1 / bins] * bins
    statistics_new = 100
    statistics_old = 101
    result_array = []
    while statistics_old > statistics_new > 0.05:
        unfolding_matrix = [[0] * bins for _ in range(bins)]
        get_unfolding_matrix(unfolding_matrix, migration_matrix, distribution, bins, False)

        expected_array = [0] * bins
        get_expected_array(expected_array, efficiency_array, unfolding_matrix, measured_array, bins, False, True)

        result_array = expected_array
        old_distribution = distribution.copy()

        expected_sum = sum(expected_array)
        for j in range(bins):
            distribution[j] = expected_array[j] / expected_sum

        statistics_old = statistics_new
        statistics_new = diy_chisquare(distribution, old_distribution, bins)
        print(f"statistics_old={statistics_old}, statistics_new={statistics_new}")

        if True:
            DataOutput.print_array("Distribution:", distribution, 2)
            print()

    return result_array


def get_unfolding_matrix(unfolding_matrix, migration_matrix, distribution, bins, print_result):
    for i in range(bins):
        for j in range(bins):
            numerator = migration_matrix[i][j] * distribution[i]
            denominator = 0

            for k in range(bins):
                sum_l = 0
                for l in range(bins):
                    sum_l += migration_matrix[k][l] * distribution[l]
                denominator += migration_matrix[k][j] * sum_l

            if denominator != 0:
                unfolding_matrix[j][i] = numerator / denominator

    if print_result:
        DataOutput.print_matrix(unfolding_matrix, bins, True)


def get_efficiency_array(efficiency_array, migration_matrix, bins, print_result):
    for j in range(bins):
        efficiency = 0
        for k in range(bins):
            efficiency += migration_matrix[k][j]
        efficiency_array[j] = efficiency

    if print_result:
        DataOutput.print_array("Efficiency:", efficiency_array, 2)
        print()


def get_expected_array(expected_array, efficiency_array, unfolding_matrix, measured_array, bins, use_eff, print_result):
    for i in range(bins):
        expected = 0
        for j in range(bins):
            expected += unfolding_matrix[j][i] * measured_array[j]
        if use_eff and efficiency_array[i] != 0:
            expected_array[i] = (1 / efficiency_array[i]) * expected
        else:
            expected_array[i] = expected

    if print_result:
        DataOutput.print_array("Expected:", expected_array, 2)


def diy_chisquare(observed, expected, bins):
    statistic = 0
    for i in range(bins):
        if expected[i] != 0:
            statistic += ((observed[i] - expected[i]) ** 2) / expected[i]
    return statistic
