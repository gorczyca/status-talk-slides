from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 1


class SNewSlide(BaseSlide):
    TITLE = r'New Slide'

    def create_content(self):
        s = self.slide



class SNewSlideScene(Slide):
    def construct(self):
        SNewSlide(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
