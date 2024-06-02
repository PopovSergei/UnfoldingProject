import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show_matrix(matrix, bins, int_vals):
    plt.close()
    if int_vals:
        sns.heatmap(data=matrix, annot=True, cmap="Blues", fmt="d")
    else:
        new_matrix = [[0] * bins for _ in range(bins)]
        for i in range(bins):
            for j in range(bins):
                new_matrix[i][j] = round(matrix[i][j], 2)
        sns.heatmap(data=new_matrix, annot=True, cmap="Blues")
    plt.xlabel("Бины измеренных событий")
    plt.ylabel("Бины истинных событий")
    plt.show()


def show_bar_charts(arrays, names, x_label, y_label, color_scheme=1):
    plt.close()
    x = np.arange(len(arrays[0]))
    fig, ax = plt.subplots(figsize=(10, 5))

    if color_scheme == 0:
        color1 = "#324D5E"
        color2 = "#3FB39E"
        color3 = "#EFCA3E"
        color4 = "#E57A36"
        color5 = "#E24745"
    elif color_scheme == 1:
        color1 = "#85C86E"
        color2 = "#024669"
        color3 = "#035D8F"
        color4 = "#2787B7"
        color5 = "#67B3DA"
        color6 = "#AED3E5"
        color7 = "#DBEAF1"
    else:
        color1 = "#6FAC9C"
        color2 = "#9FD4C0"
        color3 = "#D0E8B4"
        color4 = "#2787B7"
        color5 = "#67B3DA"

    length = len(arrays)

    if length == 1:
        width = 0.7
        ax.bar(x, arrays[0], width, label=names[0], color=color1)
    elif length == 2:
        width = 0.3
        ax.bar(x - width / 2, arrays[0], width, label=names[0], color=color1)
        ax.bar(x + width / 2, arrays[1], width, label=names[1], color=color4)
    elif length == 3:
        width = 0.3
        ax.bar(x - width, arrays[0], width, label=names[0], color=color1)
        ax.bar(x, arrays[1], width, label=names[1], color=color4)
        ax.bar(x + width, arrays[2], width, label=names[2], color=color5)
    elif length == 4:
        width = 0.22
        ax.bar(x - 1.5 * width, arrays[0], width, label=names[0], color=color1)
        ax.bar(x - width / 2, arrays[1], width, label=names[1], color=color3)
        ax.bar(x + width / 2, arrays[2], width, label=names[2], color=color4)
        ax.bar(x + 1.5 * width, arrays[3], width, label=names[3], color=color5)
    else:
        width = 0.18
        ax.bar(x - 2 * width, arrays[-5], width, label=names[-5], color=color1)
        ax.bar(x - width, arrays[-4], width, label=names[-4], color=color2)
        ax.bar(x, arrays[-3], width, label=names[-3], color=color3)
        ax.bar(x + width, arrays[-2], width, label=names[-2], color=color4)
        ax.bar(x + 2 * width, arrays[-1], width, label=names[-1], color=color5)

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


def matrix_to_string(matrix, bins, flag):
    string = ""
    for i in range(bins):
        for j in range(bins):
            if i == j and flag:
                string += f"|{round(matrix[i][j], 2)}| "
            else:
                string += f"{round(matrix[i][j], 2)} "
        string += "\n"
    string += "\n"
    return string


def print_array(name, array, round_val=None):
    print(name, end=" ")
    if round_val is None:
        for value in array:
            print(value, end=" ")
    else:
        for value in array:
            print(round(value, round_val), end=" ")
    print()


def array_to_string(name, array, round_val=None):
    string = f"{name} "
    if round_val is None:
        for value in array:
            string += f"{value} "
    else:
        for value in array:
            string += f"{round(value, round_val)} "
    string += "\n"
    return string
