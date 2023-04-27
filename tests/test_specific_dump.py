import json
import os
from src.lib.ParserAirbossData import ParserAirbossData
from src.lib.Bcolors import Bcolors as Colors
from root import ROOT_DIR
from tests.lib import get_result_trap
from src.plotters.raw_data_plot.RawDataPlotter import RawDataPlotter

filename = "2023_04_26_09_31_trap_file.json"

file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "raw_plots", filename.strip(".json")))

with open(file_path, "r") as dump_file:
    try:
        dump_data = json.load(dump_file)
        results = get_result_trap(dump_data)
    except Exception as e:
        print(f"{Colors.FAIL} e {file_path} {Colors.ENDC}")
    parser_airboss_dump = ParserAirbossData()
    parser_airboss_dump.init_data(results)
    plotter = RawDataPlotter(parser_airboss_dump)
    plotter.plot_case(plot_path)
