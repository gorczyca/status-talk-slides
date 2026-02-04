from slides.shared.slide_count import SLIDES, SLIDES_NO
from slides.shared.file_icon import FileIcon
from slides.shared.block_diagram import BlockDiagram
from slides.shared.colors import D_BLUE, LAT_ORANGE
from slides.shared.wrappers import MathTexWrapper, TextWrapper, TexWrapper
from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


SLIDE_NO = 8

WIDTH = 13
BUFF = 1.5

# Node colors
NODE_DEFAULT = WHITE
NODE_GREEN = "#4CAF50"  # Material green
NODE_RED = "#F44336"    # Material red

# Icon scale and spacing
ICON_SCALE = 0.6
V_BUFF = 1.0  # vertical spacing between rows
H_BUFF = 1.0  # horizontal spacing between columns


class SAbaArchitecture(BaseSlide):
    TITLE = r'MS-DIS: System Architecture \& Extensibility'

    def create_content(self):
        s = self.slide

        # Add block diagram on the left
        diagram = BlockDiagram()
        diagram.to_edge(LEFT, buff=1.5).shift(UP*3)
        s.add(diagram)
        self.diagram = diagram

        s.wait()
        s.next_slide()

        control_file = FileIcon(".PY", accent_color=D_BLUE, scale=ICON_SCALE, caption="(20 lines of Python)",
                                title="Control").move_to(diagram.get_center()).shift(LEFT*2+DOWN*0.5)

        s.play(
            Transform(diagram, control_file)
        )

        s.add(control_file)

        # Create three ASP file icons
        abstract_af_enc = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE,
                                   title="Abstract AF Encoding", caption="(14 lines of ASP)")
        aba_af_enc = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE,
                              title="ABA AF Encoding", caption="(77 lines of ASP)")
        aspic_af_enc = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE,
                                title="ASPIC+ AF Encoding", caption="(77 lines of ASP)")

        # Arrange them vertically to the right of control_file
        asp_files = VGroup(abstract_af_enc, aba_af_enc,
                           aspic_af_enc).arrange(DOWN, buff=V_BUFF)
        asp_files.next_to(control_file, RIGHT, buff=H_BUFF)

        # Create arrows from control_file to each ASP file
        arrow1 = Arrow(control_file.get_right(),
                       abstract_af_enc.get_left(), buff=0.1, color=BLACK)
        arrow2 = Arrow(control_file.get_right(),
                       aba_af_enc.get_left(), buff=0.1, color=BLACK)
        arrow3 = Arrow(control_file.get_right(),
                       aspic_af_enc.get_left(), buff=0.1, color=BLACK)

        # Show files one by one
        s.wait()
        s.next_slide()
        s.play(FadeIn(abstract_af_enc), Create(arrow1))
        s.wait()
        s.next_slide()

        s.play(FadeIn(aba_af_enc), Create(arrow2))
        s.wait()
        s.next_slide()

        s.play(FadeIn(aspic_af_enc), Create(arrow3))
        s.wait()
        s.next_slide()

        # Create targets to the right of the ASP files
        aba_stable_sem = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE,
                                  title="Stable Semantics", caption="(3 lines of ASP)")
        aba_stable_sem.next_to(aba_af_enc, RIGHT, buff=H_BUFF)

        # Create dots with invisible padding to match file icon width

        def padded_dots():
            padding = TextWrapper("...", font_size=30, color=WHITE)
            dots = TextWrapper("...", font_size=40)
            return VGroup(padding.copy(), dots, padding.copy()).arrange(RIGHT, buff=0)

        dots1 = padded_dots().next_to(abstract_af_enc, RIGHT, buff=H_BUFF)
        dots3 = padded_dots().next_to(aspic_af_enc, RIGHT, buff=H_BUFF)

        # Create horizontal arrows (dashed for dots)
        arrow_to_dots1 = Arrow(abstract_af_enc.get_right(),
                               dots1.get_left(), buff=0.1, color=BLACK)
        arrow_to_aba_stable_sem = Arrow(aba_af_enc.get_right(
        ), aba_stable_sem.get_left(), buff=0.1, color=BLACK)
        arrow_to_dots3 = Arrow(aspic_af_enc.get_right(),
                               dots3.get_left(), buff=0.1, color=BLACK)

        # Show them one by one
        s.play(FadeIn(dots1), Create(arrow_to_dots1),
               FadeIn(aba_stable_sem), Create(arrow_to_aba_stable_sem),
               FadeIn(dots3), Create(arrow_to_dots3))
        # s.wait()
        # s.next_slide()

        # s.play(FadeIn(aba_stable_sem), Create(arrow_to_aba_stable_sem))
        # s.wait()
        # s.next_slide()

        # s.play(FadeIn(dots3), Create(arrow_to_dots3))
        s.wait()
        s.next_slide()

        # Footnote (single line, no marker object)
        footnote_text = TexWrapper(
            r"\makebox[30cm][l]{\small $^{1}$ Susana Hahn, Orkunt Sabuncu, Torsten Schaub, Tobias Stolzmann. \textit{Clingraph: A System for ASP-based Visualization.} TPLP (2024).}",
            font_size=14
        ).to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.4).shift(UP*.5)
        # s.add(footnote_text)


        # Create three ASP file icons
        abstract_vis = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE,
                                title="Visualisation (Clingraph$^1$)", caption="(16-35 lines of ASP)").next_to(dots1, RIGHT, buff=H_BUFF)
        aba_vis = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE, title="Visualisation (Clingraph$^1$)",
                           caption="(40-84 lines of ASP)").next_to(aba_stable_sem, RIGHT, buff=H_BUFF)
        aspic_vis = FileIcon(".ASP", accent_color=LAT_ORANGE, scale=ICON_SCALE,
                             title="Visualisation (Clingraph$^1$)", caption="(49 lines of ASP)").next_to(dots3, RIGHT, buff=H_BUFF)

        # Add visualization images from ms-dis-vis
        IMG_SCALE = 0.4
        af_img = ImageMobject(
            str(_PROJECT_ROOT / "img/ms-dis-vis/af.png")).scale(IMG_SCALE)
        aba_img = ImageMobject(
            str(_PROJECT_ROOT / "img/ms-dis-vis/aba.png")).scale(IMG_SCALE)
        aspic_img = ImageMobject(
            str(_PROJECT_ROOT / "img/ms-dis-vis/aspic.png")).scale(IMG_SCALE)

        # Position images to the right of the output column
        img_buff = 0.1
        af_img.next_to(abstract_vis, RIGHT, buff=img_buff)
        aba_img.next_to(aba_vis, RIGHT, buff=img_buff)
        aspic_img.next_to(aspic_vis, RIGHT, buff=img_buff*3)

        # Arrows to images
        arrow_to_af_img = Arrow(
            dots1.get_right(), abstract_vis.get_left(), buff=0.1, color=BLACK)
        arrow_to_aba_img = Arrow(aba_stable_sem.get_right(
        ), aba_vis.get_left(), buff=0.1, color=BLACK)
        arrow_to_aspic_img = Arrow(
            dots3.get_right(), aspic_vis.get_left(), buff=0.1, color=BLACK)

        # Show images one by one
        s.play(FadeIn(af_img), FadeIn(abstract_vis), Create(arrow_to_af_img),
               FadeIn(aba_img), FadeIn(aba_vis), Create(arrow_to_aba_img),
               FadeIn(aspic_img), FadeIn(aspic_vis), Create(arrow_to_aspic_img),
                FadeIn(footnote_text)
        )

        s.wait()
        s.next_slide()
        

        # Add Python files above and below the control file
        py_file_above = FileIcon(".PY", accent_color=D_BLUE, scale=ICON_SCALE, caption="(18 lines of ASP)",
                                 title="Approximation").next_to(control_file, UP, buff=V_BUFF*0.5)
        py_file_below = FileIcon(".PY", accent_color=D_BLUE, scale=ICON_SCALE, caption="(50 lines of Python)",
                                 title="Interactive").next_to(control_file, DOWN, buff=V_BUFF*0.5)

        s.play(FadeIn(py_file_above), FadeIn(py_file_below))



class SAbaArchitectureScene(Slide):
    def construct(self):
        SAbaArchitecture(self, show_footer=True,
                         slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
