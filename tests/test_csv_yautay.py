import json
import os
from src.lib.ParserAirbossData import ParserAirbossData
from src.lib.Bcolors import Bcolors as Colors
from root import ROOT_DIR
from src.plotters.raw_data_plot.RawDataPlotter import RawDataPlotter
from src.plotters.yautay_plot.YautayPlotter import YautayPlotter

for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "csv")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "csv"), filename)
    plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "raw_plots", "CSV_" + filename.strip(".json")))
    plot_json = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "json", "CSV_" + filename))

    try:
        plotter = YautayPlotter(rcvd_data=file_path, dump_parsed_data=plot_json)
        plotter.plot_case(plot_path)
    except Exception as e:
        print(f"{Colors.FAIL} {str(e)} {file_path} {Colors.ENDC}")

