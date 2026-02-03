from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper

from slides.shared.slide_count import SLIDES, SLIDES_NO

SLIDE_NO = 2


class SOutline(BaseSlide):
    TITLE = r'Outline'


    def create_content(self):
        s = self.slide

        font_size = 30

        part1 = TexWrapper(
            r'\textbf{Part I: Argumentation Games in Multi-Shot ASP}',
            font_size=font_size,
            color=BLACK
        )

        part2 = TexWrapper(
            r'\textbf{Part II: Generalisations of S4F and Standpoint Logic}',
            font_size=font_size,
            color=BLACK
        )

        sub2a = TexWrapper(
            r'-- Product of Standpoint and S4F Logic: Standpoint S4F Logic',
            font_size=font_size,
            color=BLACK
        )

        sub2b = TexWrapper(
            r'-- Fusion of S4F and Standpoint Logic: S4F Standpoint Logic',
            font_size=font_size,
            color=BLACK
        )

        # Arrange vertically
        outline = VGroup(part1, part2, sub2a, sub2b).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # Indent the sub-items
        sub2a.shift(RIGHT * 0.25)
        sub2b.shift(RIGHT * 0.25)

        outline.to_edge(LEFT).shift(RIGHT*.25 + UP*0)

        s.add(outline)


class SOutlineScene(Slide):
    def construct(self):
        SOutline(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
