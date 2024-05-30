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
    plt.xlabel("Measured bins")
    plt.ylabel("True bins")
    plt.show()


def show_bar_charts(arrays, names, x_label="x_label", y_label="y_label", color_scheme=0, bins=0):
    plt.close()
    x = np.arange(bins)
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
        ax.bar(x - width / 2, first_array, width, label=first_name, color="#6FAC9C")
        ax.bar(x + width / 2, second_array, width, label=second_name, color="#9FD4C0")
    else:
        ax.bar(x - width, first_array, width, label=first_name, color="#6FAC9C")
        ax.bar(x, second_array, width, label=second_name, color="#9FD4C0")
        ax.bar(x + width, third_array, width, label=third_name, color="#D0E8B4")

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
