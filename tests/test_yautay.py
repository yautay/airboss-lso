import json
import os
from src.utils.colors import Colors
from root import ROOT_DIR
from src.utils.tests import get_result_trap


for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "dumps")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
    with open(file_path, "r") as dump_file:
        try:
            dump_data = json.load(dump_file)
            results = get_result_trap(dump_data)
            # print(results)
        except OSError as e:
            print(f"{Colors.FAIL}Warning: Error opening {file_path} {Colors.ENDC}")



# for testcase in testfiles_funkman:
#     filename = testcase["filename"]
#     savefile = testcase["savefile"]
#     result = get_result_trap(filename)
#     yplot(result).plot_case(savefile)
