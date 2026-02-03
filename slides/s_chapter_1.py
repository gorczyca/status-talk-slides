from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper

from slides.shared.slide_count import SLIDES, SLIDES_NO

SLIDE_NO = 1


class SChapter1(BaseSlide):
    TITLE = None  # No title bar for chapter slides

    def create_content(self):
        s = self.slide

        text = TexWrapper(
            r'\textbf{Part I: Argumentation Games in Multi-Shot ASP}',
            font_size=36,
            color=BLACK
        ).move_to(ORIGIN)

        s.add(text)


class SChapter1Scene(Slide):
    def construct(self):
        SChapter1(self, show_footer=False, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
