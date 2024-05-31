from UnfoldMethod import UnfoldMethod
from utils import DataOutput
from utils import FileUsage


class DAgostini(UnfoldMethod):
    def __init__(self):
        super().__init__()
        self.efficiency_array = None
        self.unfolding_matrix = None
        self.result_array = None
        self.distribution_array = None
        self.results = None

    def real_init(self, migration_path, data_path, binning_type, custom_bins=0, splitting=0):
        super().init_migration_part(migration_path, binning_type, custom_bins, False)

        # Получение апостериорных данных из файла, запись в posterior_values. Изменяется: posterior_values
        self.posterior_values = FileUsage.read_file(data_path, False)
        super().binning(self.posterior_values)
        super().set_posterior_arrays(True)

        if splitting == 0:
            self.d_agostini_algorithm()
        else:
            util_true_array = self.true_array.copy()
            util_measured_array = self.measured_array.copy()
            util_values_len = len(self.posterior_values)
            results_array = [0] * self.bins

            values_array = super().split_values(splitting)
            for i in range(splitting):
                self.posterior_values = values_array[i]
                super().set_posterior_arrays(True)
                self.d_agostini_algorithm()
                for j in range(self.bins):
                    results_array[j] += self.distribution_array[j]

            for i in range(self.bins):
                self.result_array[i] = results_array[i] / splitting * util_values_len
                self.true_array[i] = util_true_array[i]
                self.measured_array[i] = util_measured_array[i]

    def d_agostini_algorithm(self):
        self.results = []
        self.set_efficiency_array()
        self.distribution_array = [1 / self.bins] * self.bins
        new_chi_square = 100
        old_chi_square = 101

        while old_chi_square > new_chi_square > 0.05:
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
        self.efficiency_array = [0] * self.bins
        for j in range(self.bins):
            efficiency = 0
            for k in range(self.bins):
                efficiency += self.migration_matrix[k][j]
            self.efficiency_array[j] = efficiency

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
