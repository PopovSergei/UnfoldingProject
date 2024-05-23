import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show_matrix(matrix, bins):
    new_matrix = [[0] * bins for _ in range(bins)]
    for i in range(bins):
        for j in range(bins):
            new_matrix[i][j] = round(matrix[i][j], 2)

    sns.heatmap(data=new_matrix, annot=True, cmap="Blues")
    plt.xlabel('Measured bins')
    plt.ylabel('True bins')
    plt.show()


def show_matrix_v2(matrix, bins):
    fig, ax = plt.subplots()
    ax.matshow(matrix, cmap="Blues")
    for i in range(bins):
        for j in range(bins):
            ax.text(i, j, str(matrix[j][i]), va='center', ha='center')
    plt.xlabel('Measured bins')
    plt.ylabel('True bins')
    plt.show()


def show_bar_chart(
        first_array, second_array, third_array=None,
        first_name="", second_name="", third_name=None,
        x_label="x_label", y_label="y_label", bins=0
):
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
