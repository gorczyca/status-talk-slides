from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper

from slides.shared.slide_count import SLIDES, SLIDES_NO

SLIDE_NO = 1


class SChapter2b(BaseSlide):
    TITLE = None  # No title bar for chapter slides

    def create_content(self):
        s = self.slide

        text = TexWrapper(
            r'\textbf{Fusion of S4F and Standpoint Logic: S4F Standpoint Logic}',
            font_size=36,
            color=BLACK
        ).move_to(ORIGIN)

        s.add(text)


class SChapter2bScene(Slide):
    def construct(self):
        SChapter2b(self, show_footer=False, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
