import DAgostini
import Baron
import utils
from view import Window

filePath = "resources/text.txt"
filePath2 = "resources/sim_p_2.txt"
filePath3 = "resources/text1.txt"
filePath4 = "resources/text1bin.txt"

first_path = "resources/first_part.txt"
second_path = "resources/second_part.txt"

first_path1 = "resources/first_part1.txt"
second_path1 = "resources/second_part1.txt"

first_path2 = "resources/first_part2.txt"
second_path2 = "resources/second_part2.txt"

if __name__ == '__main__':
    window = Window(700, 500, "Обратная свёртка")
    window.run()
    # utils.separate_file(filePath2, first_path2, second_path2)
    # DAgostini.d_agostini(first_path2, second_path2)
    # Baron.baron(first_path2, second_path2)
