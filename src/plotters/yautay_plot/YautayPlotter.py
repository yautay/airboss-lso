import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from src.lib.Keys import KeysTrapsheet as K, KeysGRV as GRV, KeysGS as GS, KeysAoA as AoA
from src.lib.Keys import KeysTrapfile as KO
from src.lib.Keys import KeysAirframes as AIRFRAME
from src.lib.Utils import Utils
from src.plotters.yautay_plot.assets import assets
from src.lib.ParserAirbossData import ParserAirbossData, DownwindStripper


class YautayPlotter(object):
    def __init__(self,  data_object: ParserAirbossData):
        self.__data = data_object.data
        self.__oth_data = data_object.oth_data
        self.__airframe_index = data_object.airframe_index
        self.__limits_aoa = data_object.limits_aoa
        self.__limits_lu = data_object.limits_lu
        self.__limits_lue = data_object.limits_lue
        self.__limits_gs = data_object.limits_gs
        self.__limits_gse = data_object.limits_gse

    def plot_case(self, save_file_name: str = "yautay_plot" or None, fillins: bool = False):
        def data_interpolate(smooth: int = 500, **kwargs):
            ax = kwargs["ax"]
            x = kwargs["x"]
            y = kwargs["y"]

            downwind_pool = -len(x) + DownwindStripper.downwind_stripper(x)

            x = x[downwind_pool:]
            y = y[downwind_pool:]

            X_smooth = np.linspace(x[:1], x[-1:], smooth)

            _f = interp1d(x, y, kind='quadratic')
            _dfs = _f(X_smooth)
            ax.plot(X_smooth, _dfs, linewidth=track_line_width, label="Track",
                    color=track_line_colour)

        dta = self.__data

        # X-axis setup [cbls]
        x_axis_limit_left = 15
        x_axis_limit_right = 0
        limits_x_axis = np.linspace(x_axis_limit_right, x_axis_limit_left, x_axis_limit_left)

        # AoA Limits
        aoa_slo_hi_limit = self.__limits_aoa[AoA.SLO_HI]
        aoa_slo_med_limit = self.__limits_aoa[AoA.SLO_MED]
        aoa_slo_lo_limit = self.__limits_aoa[AoA.SLO_LO]
        aoa_fst_lo_limit = self.__limits_aoa[AoA.FAST_LO]
        aoa_fst_med_limit = self.__limits_aoa[AoA.FAST_MED]
        aoa_fst_hi_limit = self.__limits_aoa[AoA.FAST_HI]

        # LU Limits
        lu___lul___limit = self.__limits_lu[GRV.___LUL___]
        lu__lul__limit = self.__limits_lu[GRV.__LUL__]
        lu_lul_limit = self.__limits_lu[GRV.LUL]
        lu_lur_limit = self.__limits_lu[GRV.LUR]
        lu__lur__limit = self.__limits_lu[GRV.__LUR__]
        lu___lur___limit = self.__limits_lu[GRV.___LUR___]

        # GS Limits
        gs___hi___limit = self.__limits_gs[GS.___HI___]
        gs__hi__limit = self.__limits_gs[GS.__HI__]
        gs_hi_limit = self.__limits_gs[GS.HI]
        gs_lo_limit = self.__limits_gs[GS.LO]
        gs__lo__limit = self.__limits_gs[GS.__LO__]
        gs___lo___limit = self.__limits_gs[GS.___LO___]

        # GSE Limits
        gse___hi___limit = self.__limits_gse[GS.___HI___]
        gse__hi__limit = self.__limits_gse[GS.__HI__]
        gse_hi_limit = self.__limits_gse[GS.HI]
        gse_lo_limit = self.__limits_gse[GS.LO]
        gse__lo__limit = self.__limits_gse[GS.__LO__]
        gse___lo___limit = self.__limits_gse[GS.___LO___]

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

                lue_plot_limits(lu___lul___limit, 'red', '__LUL__')
                lue_plot_limits(lu__lul__limit, 'orange', 'LUL')
                lue_plot_limits(lu_lul_limit, 'green', '(LUL)')
                lue_plot_limits(lu_lur_limit, 'green', '(LUR)')
                lue_plot_limits(lu__lur__limit, 'orange', 'LUR')
                lue_plot_limits(lu___lur___limit, 'red', '__LUL__')

                if fillins:
                    lue_fill_limits(lu___lul___limit, lu__lul__limit, 'red')
                    lue_fill_limits(lu__lul__limit, lu_lul_limit, 'orange')
                    lue_fill_limits(lu_lul_limit, lu_lur_limit, 'green')
                    lue_fill_limits(lu_lur_limit, lu__lur__limit, 'orange')
                    lue_fill_limits(lu__lur__limit, lu___lur___limit, 'red')
                data_interpolate(ax=axins_grv, x=Utils.mtrs_to_cbls(dta[K.X]), y=dta[K.LUE], X=Utils.mtrs_to_cbls(dta[K.X]),
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

            grv_plot_limits(lu___lul___limit, 'red', '__LUL__')
            grv_plot_limits(lu__lul__limit, 'orange', 'LUL')
            grv_plot_limits(lu_lul_limit, 'green', '(LUL)')
            grv_plot_limits(lu_lur_limit, 'green', '(LUR)')
            grv_plot_limits(lu__lur__limit, 'orange', 'LUR')
            grv_plot_limits(lu___lur___limit, 'red', '__LUR__')

            if fillins:
                grv_fill_limits(lu_lul_limit, lu_lur_limit, 'green')
                grv_fill_limits(lu_lul_limit, lu__lul__limit, 'orange')
                grv_fill_limits(lu_lur_limit, lu__lur__limit, 'orange')
                grv_fill_limits(lu__lul__limit, lu___lul___limit, 'red')
                grv_fill_limits(lu__lur__limit, lu___lur___limit, 'red')

            data_interpolate(ax=ax_grv, x=Utils.mtrs_to_cbls(dta[K.X]), y=Utils.mtrs_to_cbls(dta[K.Z]), C="groove")

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

                data_interpolate(ax=axins_gs, x=Utils.mtrs_to_cbls(dta[K.X]), y=dta[K.GSE], C="ins_gs")

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
            gs_plot_limits(gs_lo_limit, 'green', '(LO)')
            gs_plot_limits(gs__lo__limit, 'orange', 'LO')
            gs_plot_limits(gs___lo___limit, 'red', '__LO__')

            if fillins:
                gs_fill_limits(gs_lo_limit, gs_hi_limit, 'green')
                gs_fill_limits(gs_lo_limit, gs__lo__limit, 'orange')
                gs_fill_limits(gs_hi_limit, gs__hi__limit, 'orange')
                gs_fill_limits(gs__lo__limit, gs___lo___limit, 'red')
                gs_fill_limits(gs__hi__limit, gs___hi___limit, 'red')

            data_interpolate(ax=ax_gs, x=Utils.mtrs_to_cbls(dta[K.X]), y=Utils.mtrs_to_feet(dta[K.ALT]), C="gs")

            plot_distance_marks(ax_gs)
            ax_gs.invert_xaxis()
            ax_gs.grid(False)
            plotter_gse()

        def plotter_aoa():
            # AoA
            aoa_y_axis_limit_low = self.__limits_aoa[AoA.FAST_HI] - .5
            aoa_y_axis_limit_hi = self.__limits_aoa[AoA.SLO_HI] + .5
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
            aoa_plot_limits(aoa_fst_lo_limit, 'green', "(F)")
            aoa_plot_limits(aoa_fst_med_limit, 'orange', "F")
            aoa_plot_limits(aoa_fst_hi_limit, 'red', "__F__")

            if fillins:
                aoa_fill_limits(aoa_slo_hi_limit, aoa_slo_med_limit, 'red')
                aoa_fill_limits(aoa_slo_med_limit, aoa_slo_lo_limit, 'orange')
                aoa_fill_limits(aoa_slo_lo_limit, aoa_fst_lo_limit, 'green')
                aoa_fill_limits(aoa_fst_lo_limit, aoa_fst_med_limit, 'orange')
                aoa_fill_limits(aoa_fst_med_limit, aoa_fst_hi_limit, 'red')

            data_interpolate(ax=ax_aoa, x=Utils.mtrs_to_cbls(dta[K.X]), y=dta[K.AOA], C="aoa")

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
            data_interpolate(ax=axins_vy, x=Utils.mtrs_to_cbls(dta[K.X]), y=dta[K.VY]*196.85, C="ins_vy")
            data_interpolate(ax=axins_roll, x=Utils.mtrs_to_cbls(dta[K.X]), y=dta[K.ROLL], C="ins_roll")

        plotter_groove()
        plotter_glideslope()
        plotter_aoa()
        plotter_utils()

        plt.xlim(x_axis_limit_left, x_axis_limit_right)

        # plt.show()

        # print(self.__oth_data)

        title = str(f'Trapsheet of {self.__oth_data[KO.NAME]} [{self.__oth_data[KO.AIRFRAME]}]')
        title += str(f'\n{self.__oth_data[KO.GRADE]} {self.__oth_data[KO.POINTS]}PT - {self.__oth_data[KO.DETAILS]}')

        fig.suptitle(title, fontsize=12, color='black')
        # fig.figure.figimage(plt.imread(assets.png_bckg_cag), 0, 0, alpha=1, zorder=-1, clip_on=True)
        fig.figure.figimage(plt.imread(assets.png_bckg_clean), 0, 0, alpha=1, zorder=-1, clip_on=True)

        def overlay_squadron(taw: bool = False):
            if taw:
            # Squadron
                if self.__oth_data[KO.AIRFRAME] in [AIRFRAME.HORNET.value[0]]:
                    fig.figure.figimage(plt.imread(assets.png_stamp_212), 0, 0, alpha=1, zorder=1,
                                        clip_on=True)
                elif self.__oth_data[KO.AIRFRAME] in [AIRFRAME.F14B.value[0], AIRFRAME.F14A.value[0]]:
                    fig.figure.figimage(plt.imread(assets.png_stamp_103), 0, 0, alpha=1, zorder=1,
                                        clip_on=True)
            else:
                if self.__oth_data[KO.AIRFRAME] in [AIRFRAME.HORNET.value[0]]:
                    fig.figure.figimage(plt.imread(assets.png_logo_hornet), 100, 1580, alpha=1, zorder=1,
                                        clip_on=True)
                elif self.__oth_data[KO.AIRFRAME] in [AIRFRAME.F14B.value[0], AIRFRAME.F14A.value[0]]:
                    fig.figure.figimage(plt.imread(assets.png_logo_tomcat), 100, 1600, alpha=1, zorder=1,
                                        clip_on=True)
                elif self.__oth_data[KO.AIRFRAME] in [AIRFRAME.AV8B.value[0]]:
                    fig.figure.figimage(plt.imread(assets.png_logo_harrier), 100, 1580, alpha=1, zorder=1,
                                        clip_on=True)

        def overlay_points():
            # Points
            if self.__oth_data[KO.POINTS] == 0:
                fig.figure.figimage(plt.imread(assets.png_0pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data[KO.POINTS] == 1:
                fig.figure.figimage(plt.imread(assets.png_1pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data[KO.POINTS] == 2:
                fig.figure.figimage(plt.imread(assets.png_2pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data[KO.POINTS] == 2.5:
                fig.figure.figimage(plt.imread(assets.png_25pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data[KO.POINTS] == 3:
                fig.figure.figimage(plt.imread(assets.png_3pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data[KO.POINTS] == 4:
                fig.figure.figimage(plt.imread(assets.png_4pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)
            elif self.__oth_data[KO.POINTS] == 5:
                fig.figure.figimage(plt.imread(assets.png_5pts), 0, 0, alpha=1, zorder=2,
                                    clip_on=True)

        def overlay_stamps_and_comments():
            #Stamps
            if self.__oth_data[KO.CASE] == 3:
                fig.figure.figimage(plt.imread(assets.png_stamp_nightpass), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            if self.__oth_data[KO.GRADE] == "OK":
                fig.figure.figimage(plt.imread(assets.png_stamp_perfect), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_unicorn), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data[KO.GRADE] == "CUT":
                fig.figure.figimage(plt.imread(assets.png_stamp_cut_pass), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_cut_pass), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data[KO.GRADE] == "WO":
                fig.figure.figimage(plt.imread(assets.png_stamp_wave_off), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_wave_off), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data[KO.GRADE] == "NG":
                fig.figure.figimage(plt.imread(assets.png_stamp_no_grade), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_no_grade), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data[KO.GRADE] == "BLT":
                fig.figure.figimage(plt.imread(assets.png_stamp_bolter), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_bolter), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
            elif self.__oth_data[KO.GRADE] == "FAIR":
                fig.figure.figimage(plt.imread(assets.png_stamp_fair), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)
                fig.figure.figimage(plt.imread(assets.png_comment_fair), 0, 0, alpha=1, zorder=4,
                                    clip_on=True)

        overlay_squadron()
        # overlay_points()
        # overlay_stamps_and_comments()

        # fig.figure.figimage(plt.imread("/home/yautay/repo/dcs-bot/assets/testpic.png"), 0, 0, alpha=0.2, zorder=-1,
        #                     clip_on=True)
        # plt.annotate("TEST anotacja", xy=(.51, .51), xycoords='figure fraction', alpha=1, color="red",
        #
        #              horizontalalignment='left', verticalalignment="bottom")
        if save_file_name:
            # fig.savefig(file_name)
            fig.savefig(save_file_name + "-alpha", transparent=True)

        return fig

