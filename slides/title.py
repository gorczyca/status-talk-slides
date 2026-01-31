from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper
import slides.shared.colors as custom_colors

from slides.shared.graphs import make_dispute_diagram


from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 0

class Title(BaseSlide):
    TITLE = ''
    def create_content(self):


        s = self.slide

        bg = SVGMobject('img/logo/tud-logo.svg')
        bg.set_color(custom_colors.PRIMARY_COLOR)
        bg.move_to(ORIGIN, aligned_edge=ORIGIN).scale(15).shift(RIGHT*1.25+UP*7)



        s.add(bg)

        title = TexWrapper(
            r'\raggedright  \setstretch{0.5}\textbf{ABA Disputes in ASP}:\\' ,
            r'Advancing Argument Games \\ ' \
            r'through Multi-Shot Solving',
            font_size=45, 
            color=WHITE,
        ).to_edge(LEFT).shift(DOWN * 2)      



        authors = TexWrapper(r'\raggedright \textbf{Martin Diller}, Piotr Gorczyca', color=WHITE, font_size=32).next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
        venue_and_date = TexWrapper(r'\raggedright NMR @ KR2025 -- 11th November 2025', color=WHITE, font_size=32).next_to(authors, DOWN, aligned_edge=LEFT, buff=0)

        # images
        tud = ImageMobject("./img/logo/TUD_Logos_final_RGB_TUD_Logo_horizontal_weiß_de.png").scale_to_fit_width(3.5).to_corner(UL).shift(UP*0.5+LEFT*0.5)
        iccl = ImageMobject("img/logo/iccl_logo.png").scale_to_fit_width(3.5).to_corner(DR).shift(RIGHT*0.25) 
            



        self.slide.add(tud, title, authors, venue_and_date, iccl)

        diagram = make_dispute_diagram().scale(0.8).move_to(ORIGIN).shift(RIGHT*2.5+UP)
        s.add(diagram)
        
        
        # s.wait(1)
        # s.play(DrawBorderThenFill(diagram, run_time=5, lag_ratio=0.5))
        # s.play(Create(diagram, run_time=15, lag_ratio=0.5))

        # run the looped animation (will draw, reset, draw, ...)
        # animator.loop(s, loops=4, step_time=0.6)

        # when the loop is done, we proceed to the next slide
        s.next_slide()


class TitleScene(Slide):  
    def construct(self):
        Title(self, show_footer=False, slide_no=SLIDE_NO, slide_total=SLIDES_NO, show_logo=False)
        self.wait()