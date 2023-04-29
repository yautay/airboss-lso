import json
import os
from src.lib.ParserAirbossData import ParserAirbossData
from src.lib.Bcolors import Bcolors as Colors
from root import ROOT_DIR
from src.plotters.raw_data_plot.RawDataPlotter import RawDataPlotter

filename = "2023_04_29_06_14_trap_file.json"

file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "raw_plots", filename.strip(".json")))

print(Colors.OKGREEN + file_path + Colors.ENDC)

with open(file_path, "r") as dump_file:
    try:
        dump_data = json.load(dump_file)
    except Exception as e:
        print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")
    try:
        parser_airboss_dump = ParserAirbossData()
    except Exception as e:
        print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")
    try:
        parser_airboss_dump.init_data(dump_data)
    except Exception as e:
        print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")
    try:
        plotter = RawDataPlotter(parser_airboss_dump)
    except Exception as e:
        print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")
    try:
        plotter.plot_case(plot_path)
    except Exception as e:
        print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")
