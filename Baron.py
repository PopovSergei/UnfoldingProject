from utils import DataOutput
from utils import FileUsage
from utils import Utils
import math


def baron(first_path, second_path):
    values = []
    true_values = []
    measured_values = []
    FileUsage.read_first_file(first_path, values, False)

    bins = Utils.find_bins(values, True)

    migration_matrix = [[0] * bins for _ in range(bins)]
    efficiency_array = [0] * bins
    acceptance_array = [0] * bins
    set_arrays(values, migration_matrix, efficiency_array, acceptance_array, bins, True)

    FileUsage.read_second_file(second_path, true_values, measured_values)
    baron_algorithm(migration_matrix, efficiency_array, acceptance_array, measured_values, true_values, bins)


def set_arrays(values, migration_matrix, efficiency_array, acceptance_array, bins, print_result):
    true_array = [0] * bins
    meas_array = [0] * bins
    for value in values:
        true_array[value.trueVal] = true_array[value.trueVal] + 1
        meas_array[value.measuredVal] = meas_array[value.measuredVal] + 1
        migration_matrix[value.trueVal][value.measuredVal] = migration_matrix[value.trueVal][value.measuredVal] + 1

    middle_array = [0] * bins
    for i in range(bins):
        middle_array[i] = migration_matrix[i][i]

    if print_result:
        print()
        DataOutput.print_array("True:", true_array)
        DataOutput.print_array("Meas:", meas_array)
        print()
        DataOutput.print_array("Middle:", middle_array)
        print()

    for i in range(bins):
        efficiency_array[i] = middle_array[i] / true_array[i]
        acceptance_array[i] = middle_array[i] / meas_array[i]

    if print_result:
        DataOutput.print_array("Efficiency:", efficiency_array, 4)
        DataOutput.print_array("Acceptance:", acceptance_array, 4)
        print()

        # DataOutput.show_bar_chart(
        #     acceptance_array, efficiency_array, None,
        #     'Acceptance', 'Efficiency', None,
        #     'Bins', 'Values', bins
        # )

        # DataOutput.show_matrix_v2(migration_matrix, bins)
        DataOutput.print_matrix(migration_matrix, bins, False)

    for i in range(bins):
        for j in range(bins):
            if efficiency_array[i] > 0 and migration_matrix[i][j] > 0:
                migration_matrix[i][j] = migration_matrix[i][j] / meas_array[i]  # DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD

    if print_result:
        # DataOutput.show_matrix(migration_matrix, bins)
        DataOutput.print_matrix(migration_matrix, bins, True)


def baron_algorithm(migration_matrix, efficiency_array, acceptance_array, measured_values, true_values, bins):
    measured_array = [0] * bins
    true_array = [0] * bins
    for value in measured_values:
        measured_array[value] = measured_array[value] + 1
    for value in true_values:
        true_array[value] = true_array[value] + 1

    if True:
        DataOutput.print_array("True:", true_array)
        DataOutput.print_array("Meas:", measured_array)
        print()

    distribution = [1 / bins] * bins
    result = 1

    st = 0
    for t in range(1, bins - 1):
        st += pow((distribution[t + 1] - distribution[t]) - (distribution[t] - distribution[t - 1]), 2)
    forth_factor = pow(math.e, (-0.01) * st)
    print(f"forth_factor={forth_factor}")

    for i in range(bins):
        if efficiency_array[i] != 0:
            first_factor = 1 / efficiency_array[i]
        else:
            first_factor = 0

        sum_j = 0
        for j in range(bins):
            sum_j += migration_matrix[i][j] * distribution[j]
            # print(f"migration_matrix={migration_matrix[i][j]}, dist={distribution[j]}, sum_j={sum_j}")

        second_factor = 1 / math.sqrt(2 * math.pi * sum_j)

        power_for_third_factor = acceptance_array[i] * (measured_array[i] / sum(measured_array)) - sum_j
        third_factor = pow(math.e, (-1) * pow(power_for_third_factor, 2))

        pre_result = first_factor * second_factor * third_factor * forth_factor
        print(f"result_factor={round(pre_result, 4)}, first_factor={round(first_factor, 4)}, "
              f"second_factor={round(second_factor, 4)}, third_factor={round(third_factor, 4)}")

        if pre_result != 0:
            result *= pre_result

    print(f"result={round(result, 4)}")

    res_array = [0] * bins
    for i in range(bins):
        for j in range(bins):
            if i != j:
                res_array[i] = result * distribution[j]

    DataOutput.print_array("Res:", res_array)
