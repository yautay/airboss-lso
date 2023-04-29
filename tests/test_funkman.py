import json
import os
from src.lib.Bcolors import Bcolors as Colors
from root import ROOT_DIR
from src.lib.ParserAirbossData import ParserAirbossData
from src.plotters.funkman_plot.FunkmanPlot import Plot as FunkmanPlot

# fplot = Plot()
#
# for testcase in testfiles_funkman:
#     filename = testcase["filename"]
#     savefile = testcase["savefile"]
#     result = get_result_trap(filename)
#     fplot.PlotTrapSheet(result, savefile)

for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "dumps")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
    plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "funkman"), filename.strip(".json"))

    with open(file_path, "r") as dump_file:
        try:
            dump_data = json.load(dump_file)
        except Exception as e:
            print(f"{Colors.FAIL} e {file_path} {Colors.ENDC}")

        parser_airboss_dump = ParserAirbossData()
        parser_airboss_dump.init_data(dump_data)

        test_data = parser_airboss_dump.oth_data
        test_data["trapsheet"] = parser_airboss_dump.data

        plotter = FunkmanPlot()
        plotter.PlotTrapSheet(result=test_data, filename=plot_path)
