from UnfoldMethod import UnfoldMethod
from utils import DataOutput
from utils import FileUsage
from utils import Utils
import math


class Baron(UnfoldMethod):
    def __init__(self):
        super().__init__()
        self.efficiency_array = None
        self.acceptance_array = None

    def real_init(self, migration_path, data_path):
        self.values = FileUsage.read_file(migration_path, False)
        self.bins = Utils.find_bins(self.values, False)

        super().set_pre_migration_matrix(True)
        super().set_migration_matrix(True)

        self.set_efficiency_and_acceptance(True)

        self.values = FileUsage.read_file(data_path, False)
        super().set_arrays(True)

        baron_algorithm(self.migration_matrix, self.efficiency_array, self.acceptance_array,
                        self.measured_array, self.true_array, self.bins)
        # self.result_array = set_result(self.migration_matrix, self.measured_array, self.bins)

    def set_efficiency_and_acceptance(self, print_result):
        self.efficiency_array = [0] * self.bins
        self.acceptance_array = [0] * self.bins
        for i in range(self.bins):
            self.efficiency_array[i] = self.pre_migration_matrix[i][i] / self.true_array[i]
            self.acceptance_array[i] = self.pre_migration_matrix[i][i] / self.measured_array[i]

        if print_result:
            DataOutput.print_array("Efficiency:", self.efficiency_array, 4)
            DataOutput.print_array("Acceptance:", self.acceptance_array, 4)
            print()

            # DataOutput.show_bar_chart(
            #     acceptance_array, efficiency_array, None,
            #     'Acceptance', 'Efficiency', None,
            #     'Bins', 'Values', bins
            # )


def baron_algorithm(migration_matrix, efficiency_array, acceptance_array, measured_array, true_array, bins):
    distribution = [1 / bins] * bins
    # distribution = true_array.copy()
    result = 1

    # st = 0
    # for t in range(1, bins - 1):
    #     st += pow((distribution[t + 1] - distribution[t]) - (distribution[t] - distribution[t - 1]), 2)
    # forth_factor = pow(math.e, (-0.01) * st)
    # print(f"forth_factor={forth_factor}")

    for i in range(bins):
        sum_j = 0
        for j in range(bins):
            sum_j += migration_matrix[i][j] * distribution[j]
            # print(f"migration_matrix={migration_matrix[i][j]}, dist={distribution[j]}, sum_j={sum_j}")

        first_factor = 1 / efficiency_array[i]
        second_factor = 1 / math.sqrt(2 * math.pi * sum_j)

        power_for_third_factor = acceptance_array[i] * (measured_array[i] / sum(measured_array)) - sum_j
        # power_for_third_factor = acceptance_array[i] * measured_array[i] - sum_j
        third_factor = pow(math.e, (-1) * pow(power_for_third_factor, 2))

        pre_result = first_factor * second_factor * third_factor * 1
        print(f"result_factor={round(pre_result, 4)}, first_factor={round(first_factor, 4)}, "
              f"second_factor={round(second_factor, 4)}, third_factor={round(third_factor, 4)}")

        if pre_result != 0:
            result *= pre_result

    print(result)
    print(f"result={round(result, 10)}")

    # new_result = [0] * bins
    # smf_mnoj = 1
    # for i in range(bins):
    #     for j in range(bins):
    #         if i != j:
    #             smf_mnoj *= (measured_array[i] * 1.99) - (measured_array[i] * 0.01)
    #     new_result[i] = smf_mnoj * result
    #     smf_mnoj = 1
    # DataOutput.print_array("New", new_result)

    # res_array = [0] * bins
    # umnoj_array = [1] * bins
    # for i in range(bins):
    #     for j in range(bins):
    #         if i != j:
    #             umnoj_array[i] *= distribution[j]
    #     res_array[i] = result * umnoj_array[i]
    #
    # DataOutput.print_array("Res:", res_array)