from UnfoldMethod import UnfoldMethod
from utils import DataOutput
from utils import FileUsage


class DAgostini(UnfoldMethod):
    def __init__(self):
        super().__init__()
        self.result_array = None
        self.results = None

    def real_init(self, migration_path, data_path, binning_type, custom_bins=0, splitting=0):
        super().init_migration_part(migration_path, binning_type, custom_bins, False)

        # Получение апостериорных данных из файла, запись в values. Изменяется: values
        measured_val_array = []
        true_val_array = []
        self.values = FileUsage.read_file(data_path, measured_val_array, true_val_array, False)
        super().binning()
        super().set_arrays(True)
        self.results = []

        if splitting == 0:
            self.result_array = d_agostini_algorithm(self.migration_matrix, self.measured_array, self.results, self.bins, True)
        else:
            util_true_array = self.true_array.copy()
            util_measured_array = self.measured_array.copy()
            util_values_len = len(self.values)
            self.result_array = [0] * self.bins

            values_array = super().split_values(splitting)
            for i in range(splitting):
                self.values = values_array[i]
                super().set_arrays(True)
                pre_result = d_agostini_algorithm(self.migration_matrix, self.measured_array, self.results, self.bins, False)
                for j in range(self.bins):
                    self.result_array[j] += pre_result[j]

            for i in range(self.bins):
                self.result_array[i] = self.result_array[i] / splitting * util_values_len
                self.true_array[i] = util_true_array[i]
                self.measured_array[i] = util_measured_array[i]


def d_agostini_algorithm(migration_matrix, measured_array, results, bins, return_values):
    efficiency_array = set_efficiency_array(migration_matrix, bins, False)
    distribution_array = [1 / bins] * bins
    result_array = [0] * bins
    new_chi_square = 100
    old_chi_square = 101

    while old_chi_square > new_chi_square > 0.05:
        unfolding_matrix = set_unfolding_matrix(migration_matrix, distribution_array, bins, False)
        result_array = set_result_array(efficiency_array, unfolding_matrix, measured_array, bins, False, True)
        results.append(result_array.copy())
        old_distribution_array = distribution_array.copy()

        result_array_sum = sum(result_array)
        for j in range(bins):
            distribution_array[j] = result_array[j] / result_array_sum

        old_chi_square = new_chi_square
        new_chi_square = find_chi_square(distribution_array, old_distribution_array, bins)

        print_results("Distribution:", distribution_array, True)
        print(f"old_chi_square={round(old_chi_square, 4)}, new_chi_square={round(new_chi_square, 4)}\n")

    if return_values:
        return result_array
    return distribution_array


def set_unfolding_matrix(migration_matrix, distribution, bins, print_result):
    unfolding_matrix = [[0] * bins for _ in range(bins)]
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

    return unfolding_matrix


def set_efficiency_array(migration_matrix, bins, print_result):
    efficiency_array = [0] * bins
    for j in range(bins):
        efficiency = 0
        for k in range(bins):
            efficiency += migration_matrix[k][j]
        efficiency_array[j] = efficiency

    print_results("Efficiency:", efficiency_array, print_result)
    return efficiency_array


def set_result_array(efficiency_array, unfolding_matrix, measured_array, bins, use_eff, print_result):
    result_array = [0] * bins
    for i in range(bins):
        expected = 0
        for j in range(bins):
            expected += unfolding_matrix[j][i] * measured_array[j]
        if use_eff and efficiency_array[i] != 0:
            result_array[i] = (1 / efficiency_array[i]) * expected
        else:
            result_array[i] = expected

    print_results("Res:", result_array, print_result)
    return result_array


def find_chi_square(distribution, old_distribution, bins):
    chi_square = 0
    for i in range(bins):
        if old_distribution[i] != 0:
            chi_square += ((distribution[i] - old_distribution[i]) ** 2) / old_distribution[i]
    return chi_square


def print_results(name, array, print_result):
    if not print_result:
        return
    DataOutput.print_array(name, array, 2)
