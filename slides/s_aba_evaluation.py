import textwrap
from pathlib import Path
from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, get_tex_template, IconDocument
import pandas as pd

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
# SLIDE_NO = SLIDES.index('Initial') + 1
SLIDE_NO = 9

# 
ASPFORABA_COLOR = '#2ca02c'
MSDIS_COLOR = '#d41159'
FLEXABLE_COLOR = '#1f77b4'


ASP_FOR_ABA = 'aspforaba'
FLEXABLE = 'flexABle'
MS_DIS = 'MS-DIS'
FLEXABLE_A_05 = 'flexABle a=.05'
FLEXABLE_A_25 = 'flexABle a=.25'
FLEXABLE_A_5 = 'flexABle a=.5'
MS_DIS_A_5 = 'MS-DIS a=5'
MS_DIS_A_10 = 'MS-DIS a=10'
MS_DIS_A_25 = 'MS-DIS a=25'

RESULT_PATHS = {
    ASP_FOR_ABA: _PROJECT_ROOT / 'results/aspforaba-adm_iccma_ver.csv',
    FLEXABLE: _PROJECT_ROOT / 'results/flexable-adm_iccma_ver.csv',
    MS_DIS: _PROJECT_ROOT / 'results/msdis-adm_iccma_ver.csv',
    FLEXABLE_A_05: _PROJECT_ROOT / 'results/flexable-adm-app-0.05_iccma_ver.csv',
    FLEXABLE_A_25: _PROJECT_ROOT / 'results/flexable-adm-app-0.25_iccma_ver.csv',
    FLEXABLE_A_5: _PROJECT_ROOT / 'results/flexable-adm-app-0.5_iccma_ver.csv',
    MS_DIS_A_5: _PROJECT_ROOT / 'results/msdis-adm-app-5_iccma_ver.csv',
    MS_DIS_A_10: _PROJECT_ROOT / 'results/msdis-adm-app-10_iccma_ver.csv',
    MS_DIS_A_25: _PROJECT_ROOT / 'results/msdis-adm-app-25_iccma_ver.csv',
}


def load_and_sort(path):
    df = pd.read_csv(path)
    df = df[df['verdict'] != 'TIMEOUT'].sort_values(
        'duration').reset_index(drop=True)
    df['X'] = df.index + 1
    return df


def compute_pos(ax, x, y, x_at):
    x = np.array(x); y = np.array(y)
    y_at = float(np.interp(x_at, x, y))
    p = ax.c2p(x_at, y_at)
    return p


def create_plot(df, ax, color, border_style, border_color, bg_color, fg_color, x_at, name, font_size=18):
    x, y = df["duration"], df["X"]
    plot = ax.plot_line_graph(
        x, y,
        stroke_width=1, line_color=color, add_vertex_dots=True,
        vertex_dot_radius=0.03,
        vertex_dot_style={"fill_color": color, "stroke_color": color, "stroke_width": 0.5},
    )

    # x_at = 510
    label = curve_label(ax, x, y, x_at=x_at, text=name, border_style=border_style, border_color=border_color, bg=bg_color, fg=fg_color, offset=UR*0, font_size=font_size)

    return plot, label


def curve_label(ax, x, y, x_at, text, bg=BLUE_E, fg=WHITE, font="Cousine", offset=UR*0.0,
                border_color=WHITE, border_width=2, border_style="solid", font_size=18):
    p = compute_pos(ax, x, y, x_at)
    lbl = Text(text, font_size=font_size, color=fg, font=font, fill_opacity=1).set_z_index(999)
    w, h = lbl.width + 0.3, lbl.height + 0.2

    fill_box = RoundedRectangle(corner_radius=0.05, width=w, height=h,
                                fill_color=bg, fill_opacity=1, stroke_width=0)
    outline = RoundedRectangle(corner_radius=0.05, width=w, height=h,
                               stroke_color=border_color, stroke_width=border_width)
    if border_style == "dotted":
        outline = DashedVMobject(outline, num_dashes=80, dashed_ratio=0.12)
    elif border_style == "dashed":
        outline = DashedVMobject(outline, num_dashes=30, dashed_ratio=0.5)

    g = VGroup(fill_box, outline, lbl).move_to(p).shift(offset).set_z_index(50)
    return g



# ---------- Your slide ----------
class SAbaEvaluation(BaseSlide):
    TITLE = 'Evaluation'

    def create_content(self):
        s = self.slide

        Y_LENGTH = 5
        X_LENGTH = 10

        aspforaba_df = load_and_sort(RESULT_PATHS[ASP_FOR_ABA])

        flexable_df = load_and_sort(RESULT_PATHS[FLEXABLE])
        msdis_df = load_and_sort(RESULT_PATHS[MS_DIS])

        #
        flexable_a_05_df = load_and_sort(RESULT_PATHS[FLEXABLE_A_05])
        flexable_a_25_df = load_and_sort(RESULT_PATHS[FLEXABLE_A_25])
        flexable_a_5_df = load_and_sort(RESULT_PATHS[FLEXABLE_A_5])

        #
        msdis_a_05_df = load_and_sort(RESULT_PATHS[MS_DIS_A_5])
        msdis_a_10_df = load_and_sort(RESULT_PATHS[MS_DIS_A_10])
        msdis_a_25_df = load_and_sort(RESULT_PATHS[MS_DIS_A_25])

        # 1st set of plots
        # create axes
        ax = Axes(
            x_range=[0, 610, 100],
            y_range=[0, 210, 100],
            x_length=X_LENGTH,
            y_length=Y_LENGTH,
            tips=True,
            axis_config={"include_numbers": True,
                         "font_size": 28, "color": BLACK},
        )
        coords = ax.add_coordinates()
        coords.set_color(BLACK)

        x_lbl = TexWrapper(r'\textit{t[s]}', color=GREY).scale(0.8).next_to(ax.x_axis, RIGHT, buff=0.1).shift(DOWN*0.1)
        y_lbl = TexWrapper(r'\textit{n[\#]}', color=GREY).scale(0.8).next_to(ax.y_axis, UP, buff=0.1).shift(LEFT*0.1)
        # ax.add(x_lbl, y_lbl)

        # add grid
        grid = NumberPlane(
            x_range=ax.x_range,
            y_range=ax.y_range,
            x_length=ax.x_axis.get_length(),
            y_length=ax.y_axis.get_length(),
            background_line_style={"stroke_color": GRAY, "stroke_width": 1, "stroke_opacity": 0.5},
            axis_config={"stroke_opacity": 0},
        )

        grid.shift(ax.c2p(0, 0) - grid.c2p(0, 0))  # pin origins together

        # s.play(Create(grid), Create(ax), Create(x_lbl), Create(y_lbl))
        s.add(grid, ax, x_lbl, y_lbl)
        s.wait()
        s.next_slide()

        flex_g_x_at = 510
        flex_plot, flex_label = create_plot(flexable_df, ax, color=FLEXABLE_COLOR, border_style='solid', border_color=FLEXABLE_COLOR, bg_color=FLEXABLE_COLOR, fg_color=WHITE, x_at=flex_g_x_at, name=FLEXABLE)

        s.play(Create(flex_plot['line_graph'], lag_ratio=1), Create(flex_plot['vertex_dots']), Create(flex_label))
        s.wait()
        s.next_slide()

        ms_dis_g_x_at = 540
        msdis_plot, msdis_label = create_plot(msdis_df, ax, color=MSDIS_COLOR, border_style='solid', border_color=MSDIS_COLOR, bg_color=MSDIS_COLOR, fg_color=WHITE, x_at=ms_dis_g_x_at, name=MS_DIS)
        s.play(Create(msdis_plot['line_graph'], lag_ratio=1), Create(msdis_plot['vertex_dots']), Create(msdis_label))
        s.wait()
        s.next_slide()

        # draw msdis

        new_ax = Axes(
            y_range=[0, 410, 100],
            x_range=[0, 610, 100],
            x_length=X_LENGTH,
            y_length=Y_LENGTH,
            tips=True,
            axis_config={"include_numbers": True,
                         "font_size": 28, "color": BLACK},
        ).move_to(ax)
        new_coords = new_ax.add_coordinates()
        new_coords.set_color(BLACK)

        new_grid = NumberPlane(
            x_range=new_ax.x_range,
            y_range=new_ax.y_range,
            x_length=new_ax.x_axis.get_length(),
            y_length=new_ax.y_axis.get_length(),
            background_line_style={"stroke_color": GRAY, "stroke_width": 1, "stroke_opacity": 0.5},
            axis_config={"stroke_opacity": 0},
        )
        new_grid.shift(new_ax.c2p(0, 0) - new_grid.c2p(0, 0))  # pin origins together        

        # move existing plots
        new_flex_plot, _ = create_plot(flexable_df, new_ax, color=FLEXABLE_COLOR, border_style='solid', border_color=FLEXABLE_COLOR, bg_color=FLEXABLE_COLOR, fg_color=WHITE, x_at=flex_g_x_at, name=FLEXABLE)
        new_flex_label_position = compute_pos(new_ax, flexable_df['duration'], flexable_df['X'], flex_g_x_at)

        new_msdis_plot, _ = create_plot(msdis_df, new_ax, color=MSDIS_COLOR, border_style='solid', border_color=MSDIS_COLOR, bg_color=MSDIS_COLOR, fg_color=WHITE, x_at=ms_dis_g_x_at, name=MS_DIS)
        new_msdis_label_position = compute_pos(new_ax, msdis_df['duration'], msdis_df['X'], ms_dis_g_x_at)


        # create aspforaba
        aspforaba_g_x_at = 400
        aspforaba_plot, aspforaba_label = create_plot(aspforaba_df, new_ax, color=ASPFORABA_COLOR, border_style='solid', border_color=ASPFORABA_COLOR, bg_color=ASPFORABA_COLOR, fg_color=WHITE, x_at=aspforaba_g_x_at, name=ASP_FOR_ABA)


        # transform everything to new scale
        s.play(
            Transform(ax, new_ax), 
            FadeOut(grid), Create(new_grid), 
            flex_label.animate.move_to(new_flex_label_position), Transform(flex_plot, new_flex_plot), 
            msdis_label.animate.move_to(new_msdis_label_position), Transform(msdis_plot, new_msdis_plot), 
            Create(aspforaba_plot['vertex_dots']), Create(aspforaba_plot['line_graph']), Create(aspforaba_label))
            

        s.wait()
        s.next_slide()

        # create approximate things
        flexable_a_05_x_at = 120
        flexable_a_05_plot, flexable_a_05_label = create_plot(flexable_a_05_df, new_ax, color=FLEXABLE_COLOR, border_style='dashed', border_color=FLEXABLE_COLOR, bg_color=WHITE, fg_color=FLEXABLE_COLOR, x_at=flexable_a_05_x_at, name=FLEXABLE_A_05)

        flexable_a_25_x_at = 100
        flexable_a_25_plot, flexable_a_25_label = create_plot(flexable_a_25_df, new_ax, color=FLEXABLE_COLOR, border_style='dashed', border_color=FLEXABLE_COLOR, bg_color=WHITE, fg_color=FLEXABLE_COLOR, x_at=flexable_a_25_x_at, name=FLEXABLE_A_25)

        ms_dis_a_10_g_x_at = 550
        ms_dis_a_10_plot, ms_dis_a_10_label = create_plot(msdis_a_10_df, new_ax, color=MSDIS_COLOR, border_style='dashed', border_color=MSDIS_COLOR, bg_color=WHITE, fg_color=MSDIS_COLOR, x_at=ms_dis_a_10_g_x_at, name=MS_DIS_A_10)

        ms_dis_a_5_g_x_at = 265
        ms_dis_a_5_plot, ms_dis_a_5_label = create_plot(msdis_a_05_df, new_ax, color=MSDIS_COLOR, border_style='dashed', border_color=MSDIS_COLOR, bg_color=WHITE, fg_color=MSDIS_COLOR, x_at=ms_dis_a_5_g_x_at, name=MS_DIS_A_5)

        RUN_TIME = 0.1

        s.play(
            Create(flexable_a_25_plot['line_graph'], lag_ratio=1), Create(flexable_a_25_plot['vertex_dots']), 
            Create(flexable_a_25_label[0], run_time=RUN_TIME), Create(flexable_a_25_label[1], run_time=RUN_TIME), Write(flexable_a_25_label[2]), 
            Create(ms_dis_a_10_plot['line_graph'], lag_ratio=1), Create(ms_dis_a_10_plot['vertex_dots']), 
            Create(ms_dis_a_10_label[0], run_time=RUN_TIME), Create(ms_dis_a_10_label[1], run_time=RUN_TIME), Write(ms_dis_a_10_label[2])
        )
        s.wait()
        s.next_slide()

        s.play(
            Create(flexable_a_05_plot['line_graph'], lag_ratio=1), Create(flexable_a_05_plot['vertex_dots']), 
            Create(flexable_a_05_label[0], run_time=RUN_TIME), Create(flexable_a_05_label[1], run_time=RUN_TIME), Write(flexable_a_05_label[2]),
            Create(ms_dis_a_5_plot['line_graph'], lag_ratio=1), Create(ms_dis_a_5_plot['vertex_dots']), 
            Create(ms_dis_a_5_label[0], run_time=RUN_TIME), Create(ms_dis_a_5_label[1], run_time=RUN_TIME), Write(ms_dis_a_5_label[2]),  
            # Create(ms_dis_a_5_label)  
        )
        # s.wait()


class SAbaEvaluationScene(Slide):
    def construct(self):
        SAbaEvaluation(self, show_footer=True,
                slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()


if __name__ == '__main__':
    SAbaEvaluationScene().construct()
