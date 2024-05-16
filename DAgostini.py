from utils import DataOutput
from utils import FileUsage
from utils import Utils


class DAgostini:
    def __init__(self):
        self.values = None
        self.bins = None
        self.pre_migration_matrix = None
        self.migration_matrix = None
        self.true_values = None
        self.measured_values = None
        self.measured_array = None
        self.true_array = None
        self.result_array = None

    def real_init(self, migration_path, data_path, bins_count):
        self.values = FileUsage.read_migration_file(migration_path, False)
        self.bins = Utils.find_bins(self.values, True)
        self.pre_migration_matrix = set_pre_migration_matrix(self.values, self.bins, False)
        self.migration_matrix = set_migration_matrix(self.values, self.pre_migration_matrix, self.bins, False)

        self.true_values = []
        self.measured_values = []
        FileUsage.read_data_file(data_path, self.true_values, self.measured_values)

        self.measured_array = set_array("Meas:", self.measured_values, self.bins, True)
        self.true_array = set_array("True:", self.true_values, self.bins, True)

        self.result_array = set_result(self.migration_matrix, self.measured_array, self.bins)


def set_pre_migration_matrix(values, bins, print_result):
    pre_migration_matrix = [[0] * bins for _ in range(bins)]
    for value in values:
        pre_migration_matrix[value.trueVal][value.measuredVal] = pre_migration_matrix[value.trueVal][value.measuredVal] + 1

    if print_result:
        DataOutput.print_matrix(pre_migration_matrix, bins, False)

    return pre_migration_matrix


def set_migration_matrix(values, migration_matrix, bins, print_result):
    true_array = [0] * bins
    # meas_array = [0] * bins

    for value in values:
        true_array[value.trueVal] = true_array[value.trueVal] + 1
        # meas_array[value.measuredVal] = true_array[value.measuredVal] + 1

    for i in range(bins):
        for j in range(bins):
            # if meas_array[j] > 0 and migration_matrix[i][j] > 0:
            #     value = migration_matrix[i][j] / meas_array[j]
            if true_array[i] > 0 and migration_matrix[i][j] > 0:
                value = migration_matrix[i][j] / true_array[i]
                migration_matrix[i][j] = value

    if print_result:
        DataOutput.print_array("True:", true_array)
        print()
        DataOutput.print_matrix(migration_matrix, bins, True)
        DataOutput.show_matrix(migration_matrix, bins)

    return migration_matrix


def set_array(name, values, bins, print_result):
    array = [0] * bins
    for value in values:
        array[value] = array[value] + 1

    if print_result:
        DataOutput.print_array(name, array)
        print()

    return array


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
