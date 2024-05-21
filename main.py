import DAgostini
import Baron
import utils
from UI import Window

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
    # Запуск UI
    window = Window()
    window.run()

    # Метод, позволяющий разделять файлы
    # utils.separate_file(filePath2, first_path2, second_path2)

    # Запуск алгоритма Д'Агостини
    # dagostini = DAgostini.DAgostini()
    # dagostini.real_init(first_path2, second_path2)

    # Запуск алгоритма Барона
    # baron = Baron.Baron()
    # baron.real_init(first_path2, second_path2)
