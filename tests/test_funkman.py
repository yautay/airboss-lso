from root import ROOT_DIR
from src.plotters.funkman_plot.FunkmanPlot import Plot
from src.utils.tests import get_result_trap
import os

fplot = Plot()

testfiles_funkman = [
    {"filename": os.path.join(ROOT_DIR, "tests", "csv", "Trapsheet-AV8B_Tarawa-001.csv"),
     "savefile": os.path.join(ROOT_DIR, "tests", "results", "funkman", "Trapsheet-AV8B_Tarawa-001.png")},
    {"filename": os.path.join(ROOT_DIR, "tests", "csv", "SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.csv"),
     "savefile": os.path.join(ROOT_DIR, "tests", "results", "funkman", "SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.png")},
    {"filename": os.path.join(ROOT_DIR, "tests", "csv", "Trapsheet-FA-18C_hornet-001.csv"),
     "savefile": os.path.join(ROOT_DIR, "tests", "results", "funkman", "Trapsheet-FA-18C_hornet-001.png")},
    {"filename": os.path.join(ROOT_DIR, "tests", "csv", "Trapsheet-FA-18C_hornet-002.csv"),
     "savefile": os.path.join(ROOT_DIR, "tests", "results", "funkman", "Trapsheet-FA-18C_hornet-002.png")},

]

for testcase in testfiles_funkman:
    filename = testcase["filename"]
    savefile = testcase["savefile"]
    result = get_result_trap(filename, csv=True)
    fplot.PlotTrapSheet(result, savefile)
