class Value:
    def __init__(self, measured_val, true_val):
        self.measuredVal = measured_val
        self.trueVal = true_val


def read_file(file_path):
    values = []
    with open(file_path, encoding="UTF-8") as file:
        for line in file:
            p = line.rstrip("\n").split(", ")
            try:
                values.append(Value(float(p[0]), float(p[1])))
            except ValueError as e:
                print(e)
    return values


def separate_file(file_path, first_path, second_path, lines=10000, bins=20):
    lines_counter = 0
    files_flag = True

    first_file = open(first_path, "w", encoding="UTF-8")
    second_file = open(second_path, "w", encoding="UTF-8")

    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file:
            if lines_counter > lines:
                first_file.close()
                second_file.close()
                file.close()
                return
            else:
                lines_counter += 1

            p = line.rstrip("\n").split(", ")
            try:
                val1 = int(float(p[0]))
                val2 = int(float(p[1]))
            except ValueError as e:
                print(e)
                continue
            if val1 < bins and val2 < bins:
                if files_flag:
                    first_file.write(line)
                    files_flag = False
                else:
                    second_file.write(line)
                    files_flag = True

    first_file.close()
    second_file.close()
    file.close()
