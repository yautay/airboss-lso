from src.lib.ParserAirbossData import ParserAirbossData


class Plotter(ParserAirbossData):
    def __init__(self, dump_rcvd_data: bool = False):
        super().__init__(dump_rcvd_data=dump_rcvd_data)

