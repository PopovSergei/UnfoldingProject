from utils import DataOutput


def find_bins(values, print_result):
    max_measured = 0
    max_true = 0
    for value in values:
        max_measured = max(max_measured, value.measuredVal)
        max_true = max(max_true, value.trueVal)
    bins = max(max_measured, max_true) + 1
    if print_result:
        print(f"maxMeasured={max_measured}, maxTrue={max_true}, bins={bins}")
        print()
    return bins


# Не используется
def get_old_unfolding_matrix(unfolding_matrix, migration_matrix, true_array, bins, all_events, print_result):
    for i in range(bins):
        for j in range(bins):

            if true_array[i] > 0 and migration_matrix[i][j] > 0:
                summ = 0
                for k in range(len(true_array)):
                    summ += migration_matrix[k][j] * (true_array[k] / all_events)

                if summ != 0:
                    value = (migration_matrix[i][j] * (true_array[i] / all_events)) / summ
                    unfolding_matrix[j][i] = value
    if print_result:
        DataOutput.print_matrix(unfolding_matrix, bins, True)


# Не используется
def old_eff_and_acc(efficiency_array, acceptance_array, bins, print_result):
    eff_sum = sum(efficiency_array)
    acc_sum = sum(acceptance_array)
    for i in range(bins):
        efficiency_array[i] = efficiency_array[i] / eff_sum
        acceptance_array[i] = acceptance_array[i] / acc_sum

    if print_result:
        print("Efficiency: ", end="")
        for i in efficiency_array:
            print(round(i, 2), end=" ")
        print()

        print("Acceptance: ", end="")
        for i in acceptance_array:
            print(round(i, 2), end=" ")
        print()
        print()
