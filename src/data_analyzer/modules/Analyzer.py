import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

from src.precise_plot.modules.Keys import KeysCSV as K, KeysGRV as GRV, KeysGS as GS, KeysAoA as AoA
from src.precise_plot.modules.Utils import Utils
from src.precise_plot.assets import assets
from src.utils.colors import Colors


class Analyzer(object):
    def __init__(self,  dump_data: bool = False):
        self.dump_data = dump_data

    def init_data(self, result: dict):

        self.__data = {
            K.x(): -np.array(result["trapsheet"][K.x()]),
            K.z(): np.array(result["trapsheet"][K.z()]),
            K.aoa(): np.array(result["trapsheet"][K.aoa()]),
            K.alt(): np.array(result["trapsheet"][K.alt()]),
            K.vy(): np.array(result["trapsheet"][K.vy()]),
            K.roll(): np.array(result["trapsheet"][K.roll()]),
            K.lue(): -np.array(result["trapsheet"][K.lue()]),
            K.gse(): np.array(result["trapsheet"][K.gse()]),
        }

        def get_val(table, key, nil="", precision=None):
            """
            Get table value.
            """
            if key in table:
                value = table[key]
                if value == "false":
                    return False
                elif value == "true":
                    return True
                else:
                    if precision != None:
                        return str(round(value, precision))
                    else:
                        return value
            else:
                return nil

        self.__oth_data = {
            "actype": get_val(result, "airframe", "Unkown"),
            "Tgroove": get_val(result, "Tgroove", "?", 1),

            "player": get_val(result, "name", "Ghostrider"),
            "grade": get_val(result, "grade", "?"),
            "points": get_val(result, "points", "?"),
            "details": get_val(result, "details"),
            "case": get_val(result, "case", "?"),
            "wire": get_val(result, "wire", "?"),

            "carriertype": get_val(result, "carriertype", "?"),
            "carriername": get_val(result, "carriername", "?"),
            "landingdist": get_val(result, "landingdist", "?"),
            "windondeck": get_val(result, "wind", "?", 1),
            "missiontime": get_val(result, "mitime", "?"),
            "missiondate": get_val(result, "midate", "?"),
            "theatre": get_val(result, "theatre", "Unknown Map")
        }

        self.__airframe = self.__airframe_context()
        self.__limits_aoa = self.__data_limits_aoa()
        self.__limits_grv = self.__data_limits_grv()
        self.__limits_gs = self.__data_limits_gs()

    def __airframe_context(self, text: bool = False):
        """
        1: FA-18C
        2: F-14
        3: AV-8
        """
        if "FA-18C" in self.__oth_data["actype"]:
            if text:
                return "F/A-18C"
            return 1
        elif "F-14" in self.__oth_data["actype"]:
            if text:
                return "F-14"
            return 2
        elif "AV-8" in self.__oth_data["actype"]:
            if text:
                return "AV-8B"
            return 9

    def __data_limits_aoa(self):
        if self.__airframe == 1:
            # F18
            return {
                AoA.slo_hi(): 9.8,
                AoA.slo_med(): 9.3,
                AoA.slo_lo(): 8.8,
                AoA.ok(): 8.1,
                AoA.fast_lo(): 7.4,
                AoA.fast_med(): 6.9,
                AoA.fast_hi(): 6.3,
            }

    def __data_limits_gs(self):
        if self.__airframe == 9:
            return {
                GS.___hi___(): 5.4,
                GS.__hi__(): 4.9,
                GS.hi(): 4.2,
                GS.gs(): 3.5,
                GS.lo(): 3,
                GS.__lo__(): 2.3,
                GS.___lo___(): 2.0,
            }
        else:
            return {
                GS.___hi___(): 5.0,
                GS.__hi__(): 4.3,
                GS.hi(): 3.9,
                GS.gs(): 3.5,
                GS.lo(): 3.2,
                GS.__lo__(): 2.9,
                GS.___lo___(): 2.6,
            }

    def __data_limits_gse(self):
        if self.__airframe == 9:
            return {
                GS.___hi___(): 1.9,
                GS.__hi__(): 1.4,
                GS.hi(): 0.7,
                GS.gs(): 0,
                GS.lo(): -0.5,
                GS.__lo__(): -1.2,
                GS.___lo___(): -1.5,
            }
        else:
            return {
                GS.___hi___(): 1.5,
                GS.__hi__(): 0.8,
                GS.hi(): 0.4,
                GS.gs(): 0,
                GS.lo(): -0.3,
                GS.__lo__(): -0.6,
                GS.___lo___(): -0.9,
            }

    @staticmethod
    def __data_limits_grv():
        return {
            GRV.___lul___(): -3,
            GRV.__lul__(): -1,
            GRV.lul(): -.5,
            GRV.ok(): 0,
            GRV.lur(): .5,
            GRV.__lur__(): 1,
            GRV.___lur___(): 3,
        }

    def plot_case(self, file_name: str = "plot" or None, fillins: bool = False):
        def data_interpolate(smooth: int = 500, **kwargs):
            ax = kwargs["ax"]
            x = kwargs["x"]
            y = kwargs["y"]
            context = kwargs["C"]

            def downwind_stripper() -> int:
                x_max = x.max()
                # print(Bcolors.OKCYAN + "x max: " + str(x_max) + Bcolors.ENDC)
                downwind = False
                last_x = 9999
                downwind_index = 0

                for i in range(len(x)):
                    # jeśli jest za rufą
                    if x[i] > 0:
                        # jeśli maleje
                        if x[i] < last_x:
                            # print("fall ", x[i])
                            last_x = x[i]
                        else:
                            # print("raise", x[i])
                            downwind_index = i
                return downwind_index

            # downwind_pool = -len(x) + downwind_stripper()
            # x = x[downwind_pool:]
            # y = y[downwind_pool:]

            # X_smooth = np.linspace(x[:1], x[-1:], smooth)

            # _f = interp1d(x, y, kind='quadratic')
            # _dfs = _f(X_smooth)
            ax.plot(x, y, linewidth=track_line_width, label="Track",
                    color=track_line_colour)
            # print(Bcolors.OKBLUE + context + Bcolors.ENDC)

        dta = self.__data

        # X-axis setup [cbls]
        x_axis_limit_left = 15
        x_axis_limit_right = 0
        limits_x_axis = np.linspace(x_axis_limit_right, x_axis_limit_left, x_axis_limit_left)

        # AoA Limits
        aoa_limits_data = self.__data_limits_aoa()
        aoa_slo_hi_limit = aoa_limits_data[AoA.slo_hi()]
        aoa_slo_med_limit = aoa_limits_data[AoA.slo_med()]
        aoa_slo_lo_limit = aoa_limits_data[AoA.slo_lo()]
        aoa_ok_limit = aoa_limits_data[AoA.ok()]
        aoa_fst_lo_limit = aoa_limits_data[AoA.fast_lo()]
        aoa_fst_med_limit = aoa_limits_data[AoA.fast_med()]
        aoa_fst_hi_limit = aoa_limits_data[AoA.fast_hi()]

        # GRV Limits
        grv_limits_data = self.__data_limits_grv()
        grv___lul___limit = grv_limits_data[GRV.___lul___()]
        grv__lul__limit = grv_limits_data[GRV.__lul__()]
        grv_lul_limit = grv_limits_data[GRV.lul()]
        grv_ok_limit = grv_limits_data[GRV.ok()]
        grv_lur_limit = grv_limits_data[GRV.lur()]
        grv__lur__limit = grv_limits_data[GRV.__lur__()]
        grv___lur___limit = grv_limits_data[GRV.___lur___()]

        # GS Limits
        gs_limits_data = self.__data_limits_gs()
        gs___hi___limit = gs_limits_data[GS.___hi___()]
        gs__hi__limit = gs_limits_data[GS.__hi__()]
        gs_hi_limit = gs_limits_data[GS.hi()]
        gs_ok_limit = gs_limits_data[GS.gs()]
        gs_lo_limit = gs_limits_data[GS.lo()]
        gs__lo__limit = gs_limits_data[GS.__lo__()]
        gs___lo___limit = gs_limits_data[GS.___lo___()]

        # GSE Limits
        gse_limits_data = self.__data_limits_gse()
        gse___hi___limit = gse_limits_data[GS.___hi___()]
        gse__hi__limit = gse_limits_data[GS.__hi__()]
        gse_hi_limit = gse_limits_data[GS.hi()]
        gse_ok_limit = gse_limits_data[GS.gs()]
        gse_lo_limit = gse_limits_data[GS.lo()]
        gse__lo__limit = gse_limits_data[GS.__lo__()]
        gse___lo___limit = gse_limits_data[GS.___lo___()]

        line_alpha = .3
        fill_alpha = .05
        track_line_width = .75
        track_line_colour = 'black'

        fig, (ax_grv, ax_gs, ax_aoa, utils) = plt.subplots(4)
        fig.set_size_inches(12, 18)
        # fig.text(0.5, 0.05, self.__filename, horizontalalignment='center', verticalalignment='center',
        #          color='red')

        def plot_distance_marks(axe):
            axe.axvline(x=Utils.mile_quarts(1, mtrs=False, cbls=True), color='black', alpha=.15, linestyle='--',
                        linewidth=1, label="1/4 Nm")
            axe.axvline(x=Utils.mile_quarts(2, mtrs=False, cbls=True), color='black', alpha=.15, linestyle='--',
                        linewidth=1, label="1/2 Nm'")
            axe.axvline(x=Utils.mile_quarts(3, mtrs=False, cbls=True), color='red', alpha=.75, linestyle='--',
                        linewidth=1, label="3/4 Nm'")
            axe.axvline(x=Utils.mile_quarts(4, mtrs=False, cbls=True), color='black', alpha=.15, linestyle='--',
                        linewidth=1, label="1 Nm'")

        def plotter_groove():
            grv_y_axis_limit_low = 2.5
            grv_y_axis_limit_hi = -.2
            grv_longitudinal_correction_in_ft = 290
            grv_lateral_correction_in_ft = 0

            def plotter_lue():
                axins_grv = ax_grv.inset_axes([.6, 0, .4, .4], transform=None, alpha=0.5, clip_path=None)
                x1, x2, y1, y2 = 6, 0, -4, 4
                axins_grv.set_xlim(x1, x2)
                axins_grv.set_ylim(y1, y2)
                axins_grv.text(.5, .9, "LUE [deg/cbls]", horizontalalignment='center',
                               transform=axins_grv.transAxes)
                def lue_plot_limits(limit, colour, label):
                    axins_grv.plot(
                        np.linspace(limit, limit),
                        color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

                def lue_fill_limits(limit_1, limit_2, colour):
                    axins_grv.fill_between(
                        np.linspace(x1, x2, x1),
                        np.linspace(limit_1, limit_1, x1),
                        np.linspace(limit_2, limit_2, x1),
                        color=colour, alpha=fill_alpha)

                lue_plot_limits(grv___lul___limit, 'red', '__LUL__')
                lue_plot_limits(grv__lul__limit, 'orange', 'LUL')
                lue_plot_limits(grv_lul_limit, 'green', '(LUL)')
                lue_plot_limits(grv_lur_limit, 'green', '(LUR)')
                lue_plot_limits(grv__lur__limit, 'orange', 'LUR')
                lue_plot_limits(grv___lur___limit, 'red', '__LUL__')

                if fillins:
                    lue_fill_limits(grv___lul___limit, grv__lul__limit, 'red')
                    lue_fill_limits(grv__lul__limit, grv_lul_limit, 'orange')
                    lue_fill_limits(grv_lul_limit, grv_lur_limit, 'green')
                    lue_fill_limits(grv_lur_limit, grv__lur__limit, 'orange')
                    lue_fill_limits(grv__lur__limit, grv___lur___limit, 'red')
                data_interpolate(ax=axins_grv, x=Utils.mtrs_to_cbls(dta[K.x()]), y=dta[K.lue()], X=Utils.mtrs_to_cbls(dta[K.x()]),
                                 C="ins_groove")
                axins_grv.yaxis.tick_right()
                axins_grv.xaxis.tick_top()
                axins_grv.invert_yaxis()
                axins_grv.patch.set_alpha(0)
                axins_grv.grid(False)

            def grove_dev_component(grv_limit: float, x: float, fb_correction: float = 9,
                                    lateral_correction: float = grv_lateral_correction_in_ft) -> float:
                rads = math.radians(grv_limit + fb_correction)
                return math.tan(rads) * x + Utils.feet_to_cbl(lateral_correction)

            def grv_plot_limits(limit, colour, label):
                ax_grv.plot(
                    limits_x_axis + Utils.feet_to_cbl(grv_longitudinal_correction_in_ft),
                    grove_dev_component(limit, limits_x_axis),
                    color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def grv_fill_limits(limit_1, limit_2, colour):
                ax_grv.fill_between(
                    limits_x_axis + Utils.feet_to_cbl(grv_longitudinal_correction_in_ft),
                    grove_dev_component(limit_1, limits_x_axis),
                    grove_dev_component(limit_2, limits_x_axis),
                    color=colour, alpha=fill_alpha)

            ax_grv.set_ylim(grv_y_axis_limit_low, grv_y_axis_limit_hi)
            ax_grv.set_ylabel('lateral offset [Cbls]')
            ax_grv.set_xlabel("distance [Cbls]")
            ax_grv.set_xlim(x_axis_limit_right, x_axis_limit_left)
            ax_grv.patch.set_alpha(0)

            grv_plot_limits(grv___lul___limit, 'red', '__LUL__')
            grv_plot_limits(grv__lul__limit, 'orange', 'LUL')
            grv_plot_limits(grv_lul_limit, 'green', '(LUL)')
            # grv_plot_limits(grv_ok_limit, 'black', '__OK__')
            grv_plot_limits(grv_lur_limit, 'green', '(LUR)')
            grv_plot_limits(grv__lur__limit, 'orange', 'LUR')
            grv_plot_limits(grv___lur___limit, 'red', '__LUR__')

            if fillins:
                grv_fill_limits(grv_lul_limit, grv_lur_limit, 'green')
                grv_fill_limits(grv_lul_limit, grv__lul__limit, 'orange')
                grv_fill_limits(grv_lur_limit, grv__lur__limit, 'orange')
                grv_fill_limits(grv__lul__limit, grv___lul___limit, 'red')
                grv_fill_limits(grv__lur__limit, grv___lur___limit, 'red')

            data_interpolate(ax=ax_grv, x=Utils.mtrs_to_cbls(dta[K.x()]), y=Utils.mtrs_to_cbls(dta[K.z()]), C="groove")

            plot_distance_marks(ax_grv)
            ax_grv.invert_xaxis()
            ax_grv.grid(False)
            plotter_lue()

        def plotter_glideslope():
            gs_y_axis_limit_low = 0
            gs_y_axis_limit_hi = 850
            gs_longitudinal_correction_in_ft = 290
            gs_vertical_correction_in_ft = 0

            def plotter_gse():
                axins_gs = ax_gs.inset_axes([.6, .6, .4, .4], transform=None, alpha=0.5, clip_path=None)
                x1, x2, y1, y2 = 6, 0, gse___lo___limit - .5, gse___hi___limit + .5
                axins_gs.set_xlim(x1, x2)
                axins_gs.set_ylim(y1, y2)
                axins_gs.text(.5, .9, "GSE [deg/cbls]", horizontalalignment='center',
                              transform=axins_gs.transAxes)

                def gse_plot_limits(limit, colour, label):
                    axins_gs.plot(
                        np.linspace(limit, limit),
                        color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

                def gse_fill_limits(limit_1, limit_2, colour):
                    axins_gs.fill_between(
                        np.linspace(x1, x2, x1),
                        np.linspace(limit_1, limit_1, x1),
                        np.linspace(limit_2, limit_2, x1),
                        color=colour, alpha=fill_alpha)

                gse_plot_limits(gse___hi___limit, 'red', '__HI__')
                gse_plot_limits(gse__hi__limit, 'orange', 'H')
                gse_plot_limits(gse_hi_limit, 'green', '(H)')
                gse_plot_limits(gse_lo_limit, 'green', '(L)')
                gse_plot_limits(gse__lo__limit, 'orange', 'L')
                gse_plot_limits(gse___lo___limit, 'red', '__L__')

                if fillins:
                    gse_fill_limits(gse___hi___limit, gse__hi__limit, 'red')
                    gse_fill_limits(gse__hi__limit, gse_hi_limit, 'orange')
                    gse_fill_limits(gse_hi_limit, gse_lo_limit, 'green')
                    gse_fill_limits(gse_lo_limit, gse__lo__limit, 'orange')
                    gse_fill_limits(gse__lo__limit, gse___lo___limit, 'red')

                data_interpolate(ax=axins_gs, x=Utils.mtrs_to_cbls(dta[K.x()]), y=dta[K.gse()], C="ins_gs")

                axins_gs.patch.set_alpha(0)
                axins_gs.yaxis.tick_right()
                axins_gs.grid(False)

            def glideslope_alt_component(gs_limit: float, x: float) -> float:
                rads = math.radians(gs_limit)
                return math.tan(rads) * x + gs_vertical_correction_in_ft

            def gs_plot_limits(limit, colour, label):
                ax_gs.plot(
                    limits_x_axis + Utils.feet_to_cbl(gs_longitudinal_correction_in_ft),
                    glideslope_alt_component(limit, Utils.cbl_to_feet(limits_x_axis))
                    , color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def gs_fill_limits(limit_1, limit_2, colour):
                ax_gs.fill_between(
                    limits_x_axis + Utils.feet_to_cbl(gs_longitudinal_correction_in_ft),
                    glideslope_alt_component(limit_1, Utils.cbl_to_feet(limits_x_axis)),
                    glideslope_alt_component(limit_2, Utils.cbl_to_feet(limits_x_axis)),
                    color=colour, alpha=fill_alpha)

            ax_gs.set_ylim(gs_y_axis_limit_low, gs_y_axis_limit_hi)
            ax_gs.set_xlim(x_axis_limit_right, x_axis_limit_left)
            ax_gs.set_ylabel('height [feet]')
            ax_gs.set_xlabel("distance [Cbls]")
            ax_gs.patch.set_alpha(0)

            gs_plot_limits(gs___hi___limit, 'red', '__HI__')
            gs_plot_limits(gs__hi__limit, 'orange', 'H')
            gs_plot_limits(gs_hi_limit, 'green', '(H)')
            # gs_plot_limits(gs_ok_limit, 'black', '__OK__')
            gs_plot_limits(gs_lo_limit, 'green', '(LO)')
            gs_plot_limits(gs__lo__limit, 'orange', 'LO')
            gs_plot_limits(gs___lo___limit, 'red', '__LO__')

            if fillins:
                gs_fill_limits(gs_lo_limit, gs_hi_limit, 'green')
                gs_fill_limits(gs_lo_limit, gs__lo__limit, 'orange')
                gs_fill_limits(gs_hi_limit, gs__hi__limit, 'orange')
                gs_fill_limits(gs__lo__limit, gs___lo___limit, 'red')
                gs_fill_limits(gs__hi__limit, gs___hi___limit, 'red')

            data_interpolate(ax=ax_gs, x=Utils.mtrs_to_cbls(dta[K.x()]), y=Utils.mtrs_to_feet(dta[K.alt()]), C="gs")

            plot_distance_marks(ax_gs)
            ax_gs.invert_xaxis()
            ax_gs.grid(False)
            plotter_gse()

        def plotter_aoa():
            # AoA
            aoa_y_axis_limit_low = aoa_limits_data[AoA.fast_hi()] - .5
            aoa_y_axis_limit_hi = aoa_limits_data[AoA.slo_hi()] + .5
            ax_aoa.set_ylim(aoa_y_axis_limit_low, aoa_y_axis_limit_hi)
            ax_aoa.set_xlim(x_axis_limit_right, x_axis_limit_left)
            ax_aoa.set_ylabel('AoA [deg]')
            ax_aoa.set_xlabel("distance [Cbls]")
            ax_aoa.patch.set_alpha(0)

            def aoa_plot_limits(limit, colour, label):
                ax_aoa.plot(
                    np.linspace(limit, limit, x_axis_limit_left),
                    color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def aoa_fill_limits(limit_1, limit_2, colour):
                ax_aoa.fill_between(
                    limits_x_axis,
                    np.linspace(limit_1, limit_1, x_axis_limit_left),
                    np.linspace(limit_2, limit_2, x_axis_limit_left),
                    color=colour, alpha=.03)

            aoa_plot_limits(aoa_slo_hi_limit, 'red', "__SLO__")
            aoa_plot_limits(aoa_slo_med_limit, 'orange', "SLO")
            aoa_plot_limits(aoa_slo_lo_limit, 'green', "(SLO)")
            # aoa_plot_limits(aoa_ok_limit, 'black', "__OK__")
            aoa_plot_limits(aoa_fst_lo_limit, 'green', "(F)")
            aoa_plot_limits(aoa_fst_med_limit, 'orange', "F")
            aoa_plot_limits(aoa_fst_hi_limit, 'red', "__F__")

            if fillins:
                aoa_fill_limits(aoa_slo_hi_limit, aoa_slo_med_limit, 'red')
                aoa_fill_limits(aoa_slo_med_limit, aoa_slo_lo_limit, 'orange')
                aoa_fill_limits(aoa_slo_lo_limit, aoa_fst_lo_limit, 'green')
                aoa_fill_limits(aoa_fst_lo_limit, aoa_fst_med_limit, 'orange')
                aoa_fill_limits(aoa_fst_med_limit, aoa_fst_hi_limit, 'red')

            data_interpolate(ax=ax_aoa, x=Utils.mtrs_to_cbls(dta[K.x()]), y=dta[K.aoa()], C="aoa")

            plot_distance_marks(ax_aoa)
            ax_aoa.invert_xaxis()
            ax_aoa.grid(False)

        def plotter_utils():
            # UTILS
            utils.set_xticks([], [])
            utils.set_yticks([], [])
            utils_y_axis_limit_lo = 0
            utils_y_axis_limit_hi = 1
            utils.set_ylim(utils_y_axis_limit_lo, utils_y_axis_limit_hi)
            utils.patch.set_alpha(0)

            axins_vy = utils.inset_axes([0, 0, .5, 1], transform=None, alpha=0.5, clip_path=None)
            axins_roll = utils.inset_axes([.5, 0, .5, 1], transform=None, alpha=0.5, clip_path=None)
            vyx1, vyx2, vyy1, vyy2 = 6, 0, -400, -1500
            rx1, rx2, ry1, ry2 = 6, 0, 50, -50
            axins_vy.set_xlim(vyx1, vyx2)
            axins_vy.set_ylim(vyy1, vyy2)
            axins_roll.set_xlim(rx1, rx2)
            axins_roll.set_ylim(ry1, ry2)
            axins_roll.yaxis.tick_right()
            axins_vy.grid(False)
            axins_roll.grid(False)
            axins_roll.patch.set_alpha(0)
            axins_vy.patch.set_alpha(0)
            axins_vy.set_xticks([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6])
            axins_roll.set_xticks([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5])
            axins_vy.set_ylabel('Vertical spd [ft/min]')
            axins_vy.set_xlabel("distance [Cbls]")
            axins_roll.set_ylabel('Bank Angle [deg]')
            axins_roll.yaxis.set_label_position("right")
            axins_roll.set_xlabel("distance [Cbls]")

            def plot_lin_limits(limit, colour, label, axin):
                axin.plot(
                    np.linspace(limit, limit),
                    color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def fill_lin_limits(limit_1, limit_2, colour, axin):
                axin.fill_between(
                    np.linspace(vyx1, vyx2, vyx1),
                    np.linspace(limit_1, limit_1, vyx1),
                    np.linspace(limit_2, limit_2, vyx1),
                    color=colour, alpha=fill_alpha)

            plot_lin_limits(-900, 'red', 'Vy limit', axins_vy)
            fill_lin_limits(-900, vyy2, 'red', axins_vy)
            axins_vy.text(.5, .75, "EXTENDED LANDING GEAR INSPECTION", horizontalalignment='center',
                          transform=axins_vy.transAxes)

            plot_lin_limits(-2.5, 'green', 'roll limit', axins_roll)
            plot_lin_limits(2.5, 'green', 'roll limit', axins_roll)
            data_interpolate(ax=axins_vy, x=Utils.mtrs_to_cbls(dta[K.x()]), y=dta[K.vy()]*196.85, C="ins_vy")
            data_interpolate(ax=axins_roll, x=Utils.mtrs_to_cbls(dta[K.x()]), y=dta[K.roll()], C="ins_roll")

        plotter_groove()
        plotter_glideslope()
        plotter_aoa()
        plotter_utils()

        plt.xlim(x_axis_limit_left, x_axis_limit_right)

        # plt.show()

        # print(self.__oth_data)

        title = str(f'Trapsheet of {self.__oth_data["player"]} [{self.__oth_data["actype"]}]')
        title += str(f'\n{self.__oth_data["grade"]} {self.__oth_data["points"]}PT - {self.__oth_data["details"]}')

        fig.suptitle(title, fontsize=12, color='black')
        fig.figure.figimage(plt.imread(assets.png_bckg_cag), 0, 0, alpha=1, zorder=-1, clip_on=True)

        def overlay_squadron():
            # Squadron
            if "FA-18C" in self.__oth_data["actype"]:
                fig.figure.figimage(plt.imread(assets.png_stamp_212), 0, 0, alpha=1, zorder=1,
                                    clip_on=True)
            elif "F-14" in self.__oth_data["actype"]:
                fig.figure.figimage(plt.imread(assets.png_stamp_103), 0, 0, alpha=1, zorder=1,
                                    clip_on=True)

        def overlay_points():
            # Points
            if self.__oth_data["points"] == 0:
                fig.figure.figimage(plt.imread(assets.png_0pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data["points"] == 1:
                fig.figure.figimage(plt.imread(assets.png_1pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data["points"] == 2:
                fig.figure.figimage(plt.imread(assets.png_2pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data["points"] == 2.5:
                fig.figure.figimage(plt.imread(assets.png_25pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data["points"] == 3:
                fig.figure.figimage(plt.imread(assets.png_3pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data["points"] == 4:
                fig.figure.figimage(plt.imread(assets.png_4pts), 0, 0, alpha=1, zorder=2,
                                clip_on=True)
            elif self.__oth_data["points"] == 5:
                fig.figure.figimage(plt.imread(assets.png_5pts), 0, 0, alpha=1, zorder=2,
                                clip_on=True)

        def overlay_stamps_and_comments():
            #Stamps
            if self.__oth_data["case"] == 3:
                fig.figure.figimage(plt.imread(assets.png_stamp_nightpass), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            if self.__oth_data["grade"] == "OK":
                fig.figure.figimage(plt.imread(assets.png_stamp_perfect), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_unicorn), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data["grade"] == "CUT":
                fig.figure.figimage(plt.imread(assets.png_stamp_cut_pass), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_cut_pass), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data["grade"] == "WO":
                fig.figure.figimage(plt.imread(assets.png_stamp_wave_off), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_wave_off), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data["grade"] == "NG":
                fig.figure.figimage(plt.imread(assets.png_stamp_no_grade), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_no_grade), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data["grade"] == "BLT":
                fig.figure.figimage(plt.imread(assets.png_stamp_bolter), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_bolter), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data["grade"] == "FAIR":
                fig.figure.figimage(plt.imread(assets.png_stamp_fair), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_fair), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            else:
                fig.figure.figimage(plt.imread(assets.png_stamp_error), 0, 0, alpha=.3, zorder=4,
                                    clip_on=True)

        overlay_squadron()
        overlay_points()
        # overlay_stamps_and_comments()

        # fig.figure.figimage(plt.imread("/home/yautay/repo/dcs-bot/assets/testpic.png"), 0, 0, alpha=0.2, zorder=-1,
        #                     clip_on=True)
        # plt.annotate("TEST anotacja", xy=(.51, .51), xycoords='figure fraction', alpha=1, color="red",
        #
        #              horizontalalignment='left', verticalalignment="bottom")
        if file_name:
            fig.savefig(file_name)
            fig.savefig(file_name + "-alpha", transparent=True)

        return fig

