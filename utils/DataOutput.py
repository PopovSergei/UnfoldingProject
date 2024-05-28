import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show_matrix(matrix, bins):
    plt.close()
    if isinstance(matrix[0][0], int):
        sns.heatmap(data=matrix, annot=True, cmap="Blues", fmt="d")
    else:
        new_matrix = [[0] * bins for _ in range(bins)]
        for i in range(bins):
            for j in range(bins):
                new_matrix[i][j] = round(matrix[i][j], 2)
        sns.heatmap(data=new_matrix, annot=True, cmap="Blues")
    plt.xlabel("Measured bins")
    plt.ylabel("True bins")
    plt.show()


def show_bar_chart(
        first_array, second_array, third_array=None,
        first_name="", second_name="", third_name=None,
        x_label="x_label", y_label="y_label", bins=0
):
    plt.close()
    x = np.arange(bins)
    width = 0.3
    fig, ax = plt.subplots(figsize=(10, 5))
    if third_array is None and third_name is None:
        ax.bar(x - width / 2, first_array, width, label=first_name)
        ax.bar(x + width / 2, second_array, width, label=second_name)
    else:
        ax.bar(x - width, first_array, width, label=first_name)
        ax.bar(x, second_array, width, label=second_name)
        ax.bar(x + width, third_array, width, label=third_name)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(x)
    ax.legend()
    plt.show()


def show_bar_chart_5(
        first_array, second_array, third_array, fourth_array, fifth_array,
        first_name, second_name, third_name, fourth_name, fifth_name,
        bins
):
    plt.close()
    x = np.arange(bins)
    width = 0.18
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(x - 2 * width, first_array, width, label=first_name, color="#324D5E")
    ax.bar(x - width, second_array, width, label=second_name, color="#3FB39E")
    ax.bar(x, third_array, width, label=third_name, color="#EFCA3E")
    ax.bar(x + width, fourth_array, width, label=fourth_name, color="#E57A36")
    ax.bar(x + 2 * width, fifth_array, width, label=fifth_name, color="#E24745")

    ax.set_xlabel('Bins')
    ax.set_ylabel('Events')
    ax.set_xticks(x)
    ax.legend()
    plt.show()


def print_matrix(matrix, bins, flag):
    for i in range(bins):
        for j in range(bins):
            if i == j and flag:
                print(f"|{round(matrix[i][j], 2)}|", end=" ")
            else:
                print(round(matrix[i][j], 2), end=" ")
        print()
    print()


def print_array(name, array, round_val=None):
    print(name, end=" ")
    if round_val is None:
        for i in array:
            print(i, end=" ")
    else:
        for i in array:
            print(round(i, round_val), end=" ")
    print()
