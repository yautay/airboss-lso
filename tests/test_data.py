import json
import os
from src.lib.ParserAirbossData import ParserAirbossData
from src.lib.Bcolors import Bcolors as Colors
from root import ROOT_DIR
from src.plotters.raw_data_plot.RawDataPlotter import RawDataPlotter


for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "dumps")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
    plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "raw_plots", filename.strip(".json")))
    plot_json = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "json", filename))

    with open(file_path, "r") as dump_file:
        results = dict
        try:
            dump_data = json.load(dump_file)
        except Exception as e:
            print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")
        try:
            plotter = RawDataPlotter(rcvd_data=dump_data, dump_parsed_data=plot_json)
            plotter.plot_case(plot_path)
        except Exception as e:
            print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")

