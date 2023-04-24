import json
import os
from src.utils.colors import Colors
from root import ROOT_DIR
from src.utils.tests import get_result_trap
from src.precise_plot.modules.Plotter import Plotter


for filename in os.listdir(os.path.join(ROOT_DIR, "tests", "dumps")):
    file_path = os.path.join(os.path.join(ROOT_DIR, "tests", "dumps"), filename)
    plot_path = os.path.join(os.path.join(ROOT_DIR, "tests", "results", "yautay"), filename.strip(".json"))

    with open(file_path, "r") as dump_file:
        try:
            dump_data = json.load(dump_file)
            results = get_result_trap(dump_data)
        except Exception as e:
            print(f"{Colors.FAIL} e {file_path} {Colors.ENDC}")
        plotter = Plotter()
        plotter.init_data(results)
        plotter.plot_case(plot_path)
