import math
import numpy as np
from matplotlib import pyplot as plt
from src.lib.ParserAirbossData import DownwindStripper
from src.lib.Keys import KeysTrapsheet as K, KeysGRV as GRV, KeysGS as GS, KeysAoA as AoA
from src.lib.Keys import KeysTrapfile as KO
from src.lib.Utils import Utils
from src.plotters.Plotter import Plotter
from src.plotters.yautay_plot.assets import assets


class RawDataPlotter(Plotter):
    def __init__(self, rcvd_data: dict, dump_rcvd_data: bool = False, dump_parsed_data: str or None = None):
        super().__init__(rcvd_data, dump_rcvd_data, dump_parsed_data)

    def plot_case(self, file_name: str or None = None, fillins: bool = False):
        def data_interpolate(smooth: int = 500, **kwargs):
            if self.groove_telemetry:
                ax = kwargs["ax"]
                x_raw = kwargs["x"]
                y_raw = kwargs["y"]

                downwind_pool = -len(x_raw) + DownwindStripper.downwind_stripper(x_raw)

                x = x_raw[downwind_pool:]
                y = y_raw[downwind_pool:]

                ax.plot(x_raw, y_raw, linewidth=track_line_width, label="Track",
                        color=track_line_colour)

                ax.plot(x, y, linewidth=2, label="Stripped",
                        color="red")

        # X-axis setup [cbls]
        x_axis_limit_left = 15
        x_axis_limit_right = 0
        limits_x_axis = np.linspace(x_axis_limit_right, x_axis_limit_left, x_axis_limit_left)

        line_alpha = .3
        fill_alpha = .05
        track_line_width = .75
        track_line_colour = 'black'

        fig, (ax_grv, ax_gs, ax_aoa, utils) = plt.subplots(4)
        fig.set_size_inches(12, 18)

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

                lue_plot_limits(self.lu___lul___limit, 'red', '__LUL__')
                lue_plot_limits(self.lu__lul__limit, 'orange', 'LUL')
                lue_plot_limits(self.lu_lul_limit, 'green', '(LUL)')
                lue_plot_limits(self.lu_lur_limit, 'green', '(LUR)')
                lue_plot_limits(self.lu__lur__limit, 'orange', 'LUR')
                lue_plot_limits(self.lu___lur___limit, 'red', '__LUL__')

                if fillins:
                    lue_fill_limits(self.lu___lul___limit, self.lu__lul__limit, 'red')
                    lue_fill_limits(self.lu__lul__limit, self.lu_lul_limit, 'orange')
                    lue_fill_limits(self.lu_lul_limit, self.lu_lur_limit, 'green')
                    lue_fill_limits(self.lu_lur_limit, self.lu__lur__limit, 'orange')
                    lue_fill_limits(self.lu__lur__limit, self.lu___lur___limit, 'red')
                data_interpolate(ax=axins_grv, x=Utils.mtrs_to_cbls(self.data[K.X]), y=self.data[K.LUE],
                                 X=Utils.mtrs_to_cbls(self.data[K.X]),
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

            grv_plot_limits(self.lu___lul___limit, 'red', '__LUL__')
            grv_plot_limits(self.lu__lul__limit, 'orange', 'LUL')
            grv_plot_limits(self.lu_lul_limit, 'green', '(LUL)')
            grv_plot_limits(self.lu_lur_limit, 'green', '(LUR)')
            grv_plot_limits(self.lu__lur__limit, 'orange', 'LUR')
            grv_plot_limits(self.lu___lur___limit, 'red', '__LUR__')

            if fillins:
                grv_fill_limits(self.lu_lul_limit, self.lu_lur_limit, 'green')
                grv_fill_limits(self.lu_lul_limit, self.lu__lul__limit, 'orange')
                grv_fill_limits(self.lu_lur_limit, self.lu__lur__limit, 'orange')
                grv_fill_limits(self.lu__lul__limit, self.lu___lul___limit, 'red')
                grv_fill_limits(self.lu__lur__limit, self.lu___lur___limit, 'red')
            data_interpolate(ax=ax_grv, x=Utils.mtrs_to_cbls(self.data[K.X]), y=Utils.mtrs_to_cbls(self.data[K.Z]), C="groove")

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
                x1, x2, y1, y2 = 6, 0, self.gse___lo___limit - .5, self.gse___hi___limit + .5
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

                gse_plot_limits(self.gse___hi___limit, 'red', '__HI__')
                gse_plot_limits(self.gse__hi__limit, 'orange', 'H')
                gse_plot_limits(self.gse_hi_limit, 'green', '(H)')
                gse_plot_limits(self.gse_lo_limit, 'green', '(L)')
                gse_plot_limits(self.gse__lo__limit, 'orange', 'L')
                gse_plot_limits(self.gse___lo___limit, 'red', '__L__')

                if fillins:
                    gse_fill_limits(self.gse___hi___limit, self.gse__hi__limit, 'red')
                    gse_fill_limits(self.gse__hi__limit, self.gse_hi_limit, 'orange')
                    gse_fill_limits(self.gse_hi_limit, self.gse_lo_limit, 'green')
                    gse_fill_limits(self.gse_lo_limit, self.gse__lo__limit, 'orange')
                    gse_fill_limits(self.gse__lo__limit, self.gse___lo___limit, 'red')
                data_interpolate(ax=axins_gs, x=Utils.mtrs_to_cbls(self.data[K.X]), y=self.data[K.GSE], C="ins_gs")

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

            gs_plot_limits(self.gs___hi___limit, 'red', '__HI__')
            gs_plot_limits(self.gs__hi__limit, 'orange', 'H')
            gs_plot_limits(self.gs_hi_limit, 'green', '(H)')
            gs_plot_limits(self.gs_lo_limit, 'green', '(LO)')
            gs_plot_limits(self.gs__lo__limit, 'orange', 'LO')
            gs_plot_limits(self.gs___lo___limit, 'red', '__LO__')

            if fillins:
                gs_fill_limits(self.gs_lo_limit, self.gs_hi_limit, 'green')
                gs_fill_limits(self.gs_lo_limit, self.gs__lo__limit, 'orange')
                gs_fill_limits(self.gs_hi_limit, self.gs__hi__limit, 'orange')
                gs_fill_limits(self.gs__lo__limit, self.gs___lo___limit, 'red')
                gs_fill_limits(self.gs__hi__limit, self.gs___hi___limit, 'red')
            data_interpolate(ax=ax_gs, x=Utils.mtrs_to_cbls(self.data[K.X]), y=Utils.mtrs_to_feet(self.data[K.ALT]), C="gs")

            plot_distance_marks(ax_gs)
            ax_gs.invert_xaxis()
            ax_gs.grid(False)
            plotter_gse()

        def plotter_aoa():
            # AoA
            aoa_y_axis_limit_low = self.limits_aoa[AoA.FAST_HI] - .5
            aoa_y_axis_limit_hi = self.limits_aoa[AoA.SLO_HI] + .5
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

            aoa_plot_limits(self.aoa_slo_hi_limit, 'red', "__SLO__")
            aoa_plot_limits(self.aoa_slo_med_limit, 'orange', "SLO")
            aoa_plot_limits(self.aoa_slo_lo_limit, 'green', "(SLO)")
            aoa_plot_limits(self.aoa_fst_lo_limit, 'green', "(F)")
            aoa_plot_limits(self.aoa_fst_med_limit, 'orange', "F")
            aoa_plot_limits(self.aoa_fst_hi_limit, 'red', "__F__")

            if fillins:
                aoa_fill_limits(self.aoa_slo_hi_limit, self.aoa_slo_med_limit, 'red')
                aoa_fill_limits(self.aoa_slo_med_limit, self.aoa_slo_lo_limit, 'orange')
                aoa_fill_limits(self.aoa_slo_lo_limit, self.aoa_fst_lo_limit, 'green')
                aoa_fill_limits(self.aoa_fst_lo_limit, self.aoa_fst_med_limit, 'orange')
                aoa_fill_limits(self.aoa_fst_med_limit, self.aoa_fst_hi_limit, 'red')
            data_interpolate(ax=ax_aoa, x=Utils.mtrs_to_cbls(self.data[K.X]), y=self.data[K.AOA], C="aoa")

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
            data_interpolate(ax=axins_vy, x=Utils.mtrs_to_cbls(self.data[K.X]), y=self.data[K.VY] * 196.85, C="ins_vy")
            data_interpolate(ax=axins_roll, x=Utils.mtrs_to_cbls(self.data[K.X]), y=self.data[K.ROLL], C="ins_roll")

        plotter_groove()
        plotter_glideslope()
        plotter_aoa()
        plotter_utils()

        plt.xlim(x_axis_limit_left, x_axis_limit_right)

        title = str(f'Trapsheet of {self.oth_data[KO.NAME]} [{self.oth_data[KO.AIRFRAME]}]')
        title += str(f'\n{self.oth_data[KO.GRADE]} {self.oth_data[KO.POINTS]}PT - {self.oth_data[KO.DETAILS]}')

        fig.suptitle(title, fontsize=12, color='black')
        fig.figure.figimage(plt.imread(assets.png_bckg_clean), 0, 0, alpha=1, zorder=-1, clip_on=True)

        if file_name:
            fig.savefig(file_name + "-alpha", transparent=True)

        return fig
