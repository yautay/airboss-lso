import numpy as np
from src.lib.ParserAirbossData import ParserAirbossData
from src.lib.Keys import KeysGRV as GRV, KeysGS as GS, KeysAoA as AoA
from src.lib.ParserCSVAirbossData import ParserCSVAirbossData


class Plotter(ParserAirbossData, ParserCSVAirbossData):
    def __init__(self, rcvd_data: dict or str, dump_rcvd_data: bool = False, dump_parsed_data: str or None = None):
        if isinstance(rcvd_data, dict):
            super(ParserAirbossData).__init__(dump_rcvd_data=dump_rcvd_data)
            self.init_data(result=rcvd_data, filename=dump_parsed_data)
        elif isinstance(rcvd_data, ParserCSVAirbossData):
            super(ParserCSVAirbossData).__init__()
            self.init_data(result=rcvd_data)
        self.groove_telemetry: bool = self.__assert_groove_telemetry()

        # AoA Limits
        self.aoa_slo_hi_limit = self.limits_aoa[AoA.SLO_HI]
        self.aoa_slo_med_limit = self.limits_aoa[AoA.SLO_MED]
        self.aoa_slo_lo_limit = self.limits_aoa[AoA.SLO_LO]
        self.aoa_fst_lo_limit = self.limits_aoa[AoA.FAST_LO]
        self.aoa_fst_med_limit = self.limits_aoa[AoA.FAST_MED]
        self.aoa_fst_hi_limit = self.limits_aoa[AoA.FAST_HI]

        # LU Limits
        self.lu___lul___limit = self.limits_lu[GRV.___LUL___]
        self.lu__lul__limit = self.limits_lu[GRV.__LUL__]
        self.lu_lul_limit = self.limits_lu[GRV.LUL]
        self.lu_lur_limit = self.limits_lu[GRV.LUR]
        self.lu__lur__limit = self.limits_lu[GRV.__LUR__]
        self.lu___lur___limit = self.limits_lu[GRV.___LUR___]

        # GS Limits
        self.gs___hi___limit = self.limits_gs[GS.___HI___]
        self.gs__hi__limit = self.limits_gs[GS.__HI__]
        self.gs_hi_limit = self.limits_gs[GS.HI]
        self.gs_lo_limit = self.limits_gs[GS.LO]
        self.gs__lo__limit = self.limits_gs[GS.__LO__]
        self.gs___lo___limit = self.limits_gs[GS.___LO___]

        # GSE Limits
        self.gse___hi___limit = self.limits_gse[GS.___HI___]
        self.gse__hi__limit = self.limits_gse[GS.__HI__]
        self.gse_hi_limit = self.limits_gse[GS.HI]
        self.gse_lo_limit = self.limits_gse[GS.LO]
        self.gse__lo__limit = self.limits_gse[GS.__LO__]
        self.gse___lo___limit = self.limits_gse[GS.___LO___]

    def __assert_groove_telemetry(self):
        grv_data = self.data
        for k, v in grv_data.items():
            if not np.any(v):
                return False
        return True
