import os
from random import randrange
from root import ROOT_DIR
from src.lib.ParserCSVAirbossData import ParserCSVAirbossData
from src.plotters.yautay_plot.YautayPlotter import YautayPlotter

test_csv_files = []


for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "csv")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "csv"), filename)
    plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "raw_plots", "CSV_" + filename.strip(".json")))
    plot_json = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "data", "json", "CSV_" + filename))
    test_csv_files.append(file_path)


x = randrange(len(test_csv_files))
parser_csv = ParserCSVAirbossData()
parser_csv.read_csv_trap(test_csv_files[x])
plotter = YautayPlotter(parser_csv)
plotter.plot_case()

