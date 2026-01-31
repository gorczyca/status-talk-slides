import textwrap
from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, get_tex_template, IconDocument
import pandas as pd

import slides.shared.colors as custom_colors

import slides.s10_evaluation1 as ev1

from slides.shared.slide_count import SLIDES, SLIDES_NO
# SLIDE_NO = SLIDES.index('Initial') + 1
SLIDE_NO = 11
# HIGHLIGHT_COLOR = custom_colors.THIRD_COLOR
HIGHLIGHT_COLOR = YELLOW


def make_col_highlight(tbl, col, color=HIGHLIGHT_COLOR, opacity=0.5, first_row=2):
    rows = len(tbl.get_rows())
    cells = [tbl.get_cell((r, col)) for r in range(first_row, rows + 1)]
    rect = SurroundingRectangle(VGroup(*cells), buff=0)\
        .set_fill(color, opacity).set_stroke(width=0).set_z_index(0)
    return rect


def make_plot_highlight(*plots, color=HIGHLIGHT_COLOR, width=3, opacity=0.5, z=100):
    return VGroup(*[
        p.copy().set_stroke(color=color, width=width, opacity=opacity).set_z_index(0)
        for p in plots
    ])

def make_plot_label_highlight(*labels, color=HIGHLIGHT_COLOR, opacity=0.25, z=99):
    return VGroup(*[
        SurroundingRectangle(lbl, buff=0.00)
        .set_fill(color, opacity)
        .set_stroke(width=0)
        .set_z_index(z)
        for lbl in labels
    ])

# ---------- Your slide ----------
class S11Evaluation2(BaseSlide):
    TITLE = 'Evaluation (2)'

    def create_content(self):
        s = self.slide

        Y_LENGTH, X_LENGTH = 5, 5

        aspforaba_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.ASP_FOR_ABA])
        flexable_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.FLEXABLE])
        msdis_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.MS_DIS])
        flex_a05_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.FLEXABLE_A_05])
        flex_a25_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.FLEXABLE_A_25])
        ms_a05_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.MS_DIS_A_5])
        ms_a10_df = ev1.load_and_sort(ev1.RESULT_PATHS[ev1.MS_DIS_A_10])

        ax = Axes(
            y_range=[0, 430, 100], x_range=[0, 700, 100],
            x_length=X_LENGTH, y_length=Y_LENGTH, tips=True,
            axis_config={"include_numbers": True,
                         "font_size": 28, "color": BLACK},
        ).to_edge(RIGHT).shift(LEFT*.5)
        ax.add_coordinates().set_color(BLACK)

        # labels = ax.get_axis_labels(x_label=TexWrapper(r'\textit{t[s]}', color=GREY).scale(0.8).shift(DOWN*10), y_label=TexWrapper(r"\textit{n[\#]}", color=GREY).scale(0.8).shift(DOWN+LEFT))
        # ax.add(labels)
        x_lbl = TexWrapper(r'\textit{t[s]}', color=GREY).scale(0.8).next_to(
            ax.x_axis, RIGHT, buff=0.1).shift(DOWN*0.1+LEFT*0.1)
        y_lbl = TexWrapper(r'\textit{n[\#]}', color=GREY).scale(
            0.8).next_to(ax.y_axis, UP, buff=0.1).shift(LEFT*0.1+DOWN*0.1)
        ax.add(x_lbl, y_lbl)
        grid = NumberPlane(
            x_range=ax.x_range, y_range=ax.y_range,
            x_length=ax.x_axis.get_length(), y_length=ax.y_axis.get_length(),
            background_line_style={"stroke_color": GRAY,
                                   "stroke_width": 1, "stroke_opacity": 0.25},
            axis_config={"stroke_opacity": 0},
        )
        grid.shift(ax.c2p(0, 0) - grid.c2p(0, 0))
        FONT_SIZE = 14

        flex_plot, flex_lbl = ev1.create_plot(flexable_df, ax, ev1.FLEXABLE_COLOR, 'solid',
                                              ev1.FLEXABLE_COLOR, ev1.FLEXABLE_COLOR, WHITE, 510, ev1.FLEXABLE, font_size=FONT_SIZE)
        ms_plot, ms_lbl = ev1.create_plot(msdis_df, ax, ev1.MSDIS_COLOR, 'solid',
                                          ev1.MSDIS_COLOR, ev1.MSDIS_COLOR, WHITE, 540, ev1.MS_DIS, font_size=FONT_SIZE)
        asp_plot, asp_lbl = ev1.create_plot(aspforaba_df, ax, ev1.ASPFORABA_COLOR, 'solid',
                                            ev1.ASPFORABA_COLOR, ev1.ASPFORABA_COLOR, WHITE, 450, ev1.ASP_FOR_ABA, font_size=FONT_SIZE)
        fa25_plot, fa25_lbl = ev1.create_plot(flex_a25_df, ax, ev1.FLEXABLE_COLOR, 'dashed',
                                              ev1.FLEXABLE_COLOR, WHITE, ev1.FLEXABLE_COLOR, 200, ev1.FLEXABLE_A_25, font_size=FONT_SIZE)
        ma10_plot, ma10_lbl = ev1.create_plot(ms_a10_df, ax, ev1.MSDIS_COLOR, 'dashed',
                                              ev1.MSDIS_COLOR, WHITE, ev1.MSDIS_COLOR, 550, ev1.MS_DIS_A_10, font_size=FONT_SIZE)
        fa05_plot, fa05_lbl = ev1.create_plot(flex_a05_df, ax, ev1.FLEXABLE_COLOR, 'dashed',
                                              ev1.FLEXABLE_COLOR, WHITE, ev1.FLEXABLE_COLOR, 220, ev1.FLEXABLE_A_05, font_size=FONT_SIZE)
        ma05_plot, ma05_lbl = ev1.create_plot(ms_a05_df, ax, ev1.MSDIS_COLOR, 'dashed',
                                              ev1.MSDIS_COLOR, WHITE, ev1.MSDIS_COLOR, 265, ev1.MS_DIS_A_5, font_size=FONT_SIZE)

        s.add(
            grid, ax,
            flex_plot, flex_lbl,
            ms_plot, ms_lbl,
            asp_plot, asp_lbl,
            fa25_plot, fa25_lbl,
            ma05_plot, ma05_lbl,
            ma10_plot, ma10_lbl,
            fa05_plot, fa05_lbl,
        )

        # HERE the table
        # lets fucking goooooooooooo
        # SCALE_FACTOR = 0.6
        FONT_SIZE = 18
        FONT_SIZE_INFO = 25
        table = Table(
            [
                ['xxxxx', 'xxx', 'xxx', 'xxx', 'xxx', 'xxx', 'xxx', 'xxx'],
                [' ', ' ', ' ', 'a=10', 'a=5', ' ', 'a=.25', 'a=.05'],
                [' ', '3', '214', '81', '0', '250', '146', '43'],
                [' ', '0', '0', '30', '153', '0', '69', '114'],
                [' ', '1', '38', '19', '2', '43', '25', '8'],
                [' ', '99', '44', '71', '60', '34', '44', '59'],
            ],
            row_labels=[
                TextWrapper(' ', font_size=FONT_SIZE).set_z_index(
                    8),  # .scale(SCALE_FACTOR),
                TextWrapper(' ', font_size=FONT_SIZE).set_z_index(
                    8),  # .scale(SCALE_FACTOR),
                # .scale(SCALE_FACTOR),
                TexWrapper(r'\sffamily \#t-out.', font_size=FONT_SIZE_INFO).align_to(LEFT).set_z_index(8),
                TexWrapper(r'\sffamily \#inc.', font_size=FONT_SIZE_INFO).align_to(LEFT).set_z_index(
                    8),  # .scale(SCALE_FACTOR),
                TexWrapper(r'\sffamily time[h]', font_size=FONT_SIZE_INFO).align_to(LEFT).set_z_index(
                    8),  # .scale(SCALE_FACTOR),
                # TextWrapper(r'% acc.', font_size=FONT_SIZE).set_z_index(8),#.scale(SCALE_FACTOR),
                TexWrapper(r'\sffamily \%acc. t', font_size=FONT_SIZE_INFO).align_to(LEFT).set_z_index(
                    8),  # .scale(SCALE_FACTOR)
            ],
            element_to_mobject=lambda s: TextWrapper(s, font_size=FONT_SIZE).set_z_index(
                8),  # .scale(SCALE_FACTOR).set_color(BLACK),
            h_buff=0.15,
            v_buff=0.12,
        ).to_edge(LEFT)

        h = table.get_horizontal_lines()
        v = table.get_vertical_lines()

        for line in [*h, *v]:
            line.set_z_index(0)

        lines = [v[0], v[2], v[5], h[1]]
        for line in lines:
            line.set_stroke(color=BLACK, width=1).set_z_index(9)

        s.add(table)

        # hide original header cells
        for c in range(1, 9):
            table.get_entries((1, c)).set_opacity(0)

        # spanning header blocks (row 1; 1-based indexing)
        r1 = SurroundingRectangle(VGroup(*[table.get_cell((1, c)) for c in range(
            2, 4)]), buff=0).set_fill(ev1.ASPFORABA_COLOR, 1).set_stroke(width=0).set_z_index(8)
        r2 = SurroundingRectangle(VGroup(*[table.get_cell((1, c)) for c in range(
            4, 7)]), buff=0).set_fill(ev1.MSDIS_COLOR, 1).set_stroke(width=0).set_z_index(8)
        r3 = SurroundingRectangle(VGroup(*[table.get_cell((1, c)) for c in range(
            7, 10)]), buff=0).set_fill(ev1.FLEXABLE_COLOR, 1).set_stroke(width=0).set_z_index(8)

        # FONT = 'Cousine'
        FONT = 'Consolas'
        FONT_SIZE_DELTA = 3
        t1 = TextWrapper("aspforaba", font=FONT, font_size=FONT_SIZE -
                         FONT_SIZE_DELTA, color=WHITE).move_to(r1).set_z_index(9)
        t2 = TextWrapper("MD-DIS", font=FONT, font_size=FONT_SIZE -
                         FONT_SIZE_DELTA, color=WHITE).move_to(r2).set_z_index(9)
        t3 = TextWrapper("flexABble", font=FONT, font_size=FONT_SIZE -
                         FONT_SIZE_DELTA, color=WHITE).move_to(r3).set_z_index(9)

        # lines = VGroup(v[0], v[1], v[4], h[0]).set_color(BLACK)
        # s.add(table, lines)

        # table_placeholder = TexWrapper(r'Here will be the table', font_size=30).to_edge(LEFT)
        s.add(r1, r2, r3, t1, t2, t3)

        s.wait()
        s.next_slide()

        exact_solvers_cols = VGroup(make_col_highlight(table, 4),
                                    make_col_highlight(table, 7))

        exact_solvers_plots = make_plot_highlight(flex_plot, ms_plot)
        # exact_solvers_plots_lbls = make_plot_label_highlight(flex_lbl, ms_lbl)


        # s.play(FadeIn(exact_solvers_cols), FadeIn(exact_solvers_plots), FadeIn(exact_solvers_plots_lbls))
        s.play(FadeIn(exact_solvers_cols), FadeIn(exact_solvers_plots))
        s.next_slide()
        # s.play(FadeOut(exact_solvers_cols), FadeOut(exact_solvers_plots), FadeOut(exact_solvers_plots_lbls))
        s.play(FadeOut(exact_solvers_cols), FadeOut(exact_solvers_plots))
        s.next_slide()

        ##
        approx_1_solvers_cols = VGroup(make_col_highlight(table, 5),
                                       make_col_highlight(table, 8))

        approx_1_solvers_plots = make_plot_highlight(fa25_plot, ma10_plot)
        approx_1_solvers_plots_lbls = make_plot_label_highlight(fa25_lbl, ma10_lbl)

        s.play(FadeIn(approx_1_solvers_cols), FadeIn(approx_1_solvers_plots), FadeIn(approx_1_solvers_plots_lbls))
        s.next_slide()
        s.play(FadeOut(approx_1_solvers_cols), FadeOut(approx_1_solvers_plots), FadeOut(approx_1_solvers_plots_lbls))
        s.next_slide()

        ##
        approx_2_solvers_cols = VGroup(make_col_highlight(table, 6),
                                       make_col_highlight(table, 9))

        approx_2_solvers_plots = make_plot_highlight(fa05_plot, ma05_plot)
        approx_2_solvers_plots_lbls = make_plot_label_highlight(fa05_lbl, ma05_lbl)

        s.play(FadeIn(approx_2_solvers_cols), FadeIn(approx_2_solvers_plots), FadeIn(approx_2_solvers_plots_lbls))
        s.next_slide()
        s.play(FadeOut(approx_2_solvers_cols), FadeOut(approx_2_solvers_plots), FadeOut(approx_2_solvers_plots_lbls))


class S11Evaluation2Scene(Slide):
    def construct(self):
        S11Evaluation2(self, show_footer=True,
                    slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()


if __name__ == '__main__':
    S11Evaluation2Scene().construct()
