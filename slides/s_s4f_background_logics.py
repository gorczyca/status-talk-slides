from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 10


class SS4fBackgroundLogics(BaseSlide):
    TITLE = r'Background: Component Logics'

    def create_content(self):
        s = self.slide

        # Create Standpoint structure on the left
        standpoint_struct = StandpointStructure(
            scale_factor=1.2,
            show_world_labels=True
        ).shift(LEFT * 3.5)

        # Create S4F structure on the right
        s4f_struct = S4FStructure(
            scale_factor=1.2,
            show_world_labels=True
        ).shift(RIGHT * 3.5)

        # Add captions above each structure
        standpoint_caption = TexWrapper(
            r'\textbf{Standpoint Logic}\\ {[Gómez Álvarez \& Sebastian Rudolph, 2021]}',
            font_size=28,
            color=BLACK
        ).next_to(standpoint_struct, UP, buff=0.5)

        s4f_caption = TexWrapper(
            r'\textbf{Modal Logic S4F}\\ {[Segerberg, 1971]}',
            font_size=28,
            color=BLACK
        ).next_to(s4f_struct, UP, buff=0.5)

        font_size = 24 

        # Semantics for Standpoint Logic (below left structure)
        semantics_slogic_1 = MathTexWrapper(
            r"\sstruct,", r"\pi", r"\modelfor", r"\standbs", r"\varphi", r'\;\;',
            r"\iffdef \sffstruct,\pi'\modelfor\varphi\text{ for all }\pi'\in\stan(s)",
            font_size=font_size
        ).next_to(standpoint_struct, DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT*2)

        semantics_slogic_2 = MathTexWrapper(
            r"\sstruct,", r"\pi", r"\modelfor", r"\spform{s} \sharpens \spform{u}",
            r"\iffdef \stan(\spform{s})\subseteq\stan(\spform{u})",
            font_size=font_size
        ).next_to(semantics_slogic_1, DOWN, aligned_edge=LEFT)

        # Semantics for S4F (below right structure)
        semantics_sff = MathTexWrapper(
            r"\sffstruct,", r"\pi", r"\modelfor", r"\know", r"\varphi",
            r"\iffdef\begin{cases} \sffstruct,\pi'\modelfor\varphi\text{ for all }\pi'\in\wf\cup\ws\text{ if }\pi\in\wf, \\ \sffstruct,\pi'\modelfor\varphi\text{ for all }\pi'\in\ws \text{ otherwise}\end{cases}",
            font_size=font_size
        ).next_to(s4f_struct, DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT*2.5)

        s.add(standpoint_struct, s4f_struct, standpoint_caption, s4f_caption,
              semantics_slogic_1, semantics_slogic_2, semantics_sff)


class SS4fBackgroundLogicsScene(Slide):
    def construct(self):
        SS4fBackgroundLogics(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
