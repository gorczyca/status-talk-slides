from pathlib import Path
from manim_slides import Slide
from manim import *

from .wrappers import TexWrapper

# Project root (two levels up: shared -> slides -> project)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class BaseSlide:
    
    # Talk meta
    # TALK_TITLE = r'Supporting Risk Management for Medical Devices via the \textsc{Riskman} Ontology \& Shapes'
    SHORT_TITLE = r'Integration of Multi-Perspective and Non-Monotonic Reasoning'
    # SHORT_TITLE = r'Advancing Argument Games through Multi-Shot Solving'
    
    # TALK_AUTHORS = 'M. Diller, P. Gorczyca, Dörthe Arndt, Martin Diller, Jochen Hampe, Georg Heidenreich, Pascal Kettmann, Markus Krötzsch, Stephan Mennicke, Sebastian Rudolph, Hannes Straß'
    SHORT_AUTHORS = r'Piotr Gorczyca, February 5th, 2026'
    
    FOOTER_FONT_SIZE = 18
    BACKGROUND_COLOR = WHITE
    FONT_COLOR = BLACK
    
    
    # Slide specific
    TITLE = None  # Subclasses override
    
    TITLE_FONT_SIZE = 48
    
    def __init__(self, slide: Slide, show_footer=True, slide_no=9, slide_total=99, show_logo=True):
        
        self.slide = slide
        slide.camera.background_color = self.BACKGROUND_COLOR  # White bg for all slides
        
        if self.TITLE:
            _title = TexWrapper(self.TITLE, color=self.FONT_COLOR, font_size=self.TITLE_FONT_SIZE).to_corner(UL)
            slide.add(_title)

        if show_logo:
            _tud_logo = ImageMobject(str(_PROJECT_ROOT / "img/logo/TUD_Logos_final_RGB_TUD_Bildmarke_blau.png")).scale_to_fit_width(1).to_corner(UR).shift(.25*UP+.25*RIGHT)
            slide.add(_tud_logo)

        if show_footer:
            _slide_count = TexWrapper(f'{slide_no}/{slide_total}', font_size=self.FOOTER_FONT_SIZE, color=self.FONT_COLOR).to_corner(DR).shift(0.25*DOWN)
            _footer_title = TexWrapper(self.SHORT_TITLE, font_size=self.FOOTER_FONT_SIZE, color=self.FONT_COLOR).to_edge(DOWN).shift(0.25*DOWN)
            # _authors = TexWrapper(self.SHORT_AUTHORS, font_size=self.FOOTER_FONT_SIZE, color=self.FONT_COLOR).to_edge(DOWN).shift(0.25*DOWN).shift(4*RIGHT)
            _authors = TexWrapper(self.SHORT_AUTHORS, font_size=self.FOOTER_FONT_SIZE, color=self.FONT_COLOR).to_corner(DL).shift(0.25*DOWN)
            slide.add(_slide_count, _authors, _footer_title)
        
        self.create_content()


    def create_content(self):
        pass  # Override per slide
    
    def show_grid(self):
        grid = NumberPlane(
            axis_config={"include_numbers": True, "color": BLACK})
        for num in grid.x_axis.numbers:
            num.set_color(BLACK)
        for num in grid.y_axis.numbers:
            num.set_color(BLACK)
        self.slide.add(grid)

    
    def pause(self):
        self.slide.wait()
        self.slide.next_slide()
        self.slide.clear()

