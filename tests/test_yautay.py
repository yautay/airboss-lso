import json
import os
from src.lib.Bcolors import Bcolors as Colors
from root import ROOT_DIR
from src.plotters.yautay_plot.YautayPlotter import YautayPlotter
from src.lib.ParserAirbossData import ParserAirbossData


for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "dumps")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
    plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "yautay"), filename.strip(".json"))

    with open(file_path, "r") as dump_file:
        try:
            dump_data = json.load(dump_file)
        except Exception as e:
            print(f"{Colors.FAIL} e {file_path} {Colors.ENDC}")
        plotter = YautayPlotter(rcvd_data=dump_data)
        plotter.plot_case(plot_path)
