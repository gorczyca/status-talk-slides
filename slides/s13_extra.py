from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper
from slides.shared.colors import D_BLUE, LAT_ORANGE

from slides.shared.slide_count import SLIDES, SLIDES_NO
from slides.shared.asp_lexer import get_asp_code, set_asp_lexer, create_code_block

set_asp_lexer()

FONT_SIZE_CODE = 17


class S13Extra(BaseSlide):
    TITLE = r'Extension: Stable Semantics'

    def create_content(self):
        s = self.slide
        stable_code = get_asp_code('./code/stable-extension.lp', font_size=FONT_SIZE_CODE, add_line_numbers=True)
        s.add(stable_code)
        # s.wait()


class S13ExtraScene(Slide):
    def construct(self):
        S13Extra(self, show_footer=False)
        self.wait()
