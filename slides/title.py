from pathlib import Path
from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper
import slides.shared.colors as custom_colors

from slides.shared.graphs import make_dispute_diagram


from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 0

# Project root for resolving asset paths
_PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Title(BaseSlide):
    TITLE = ''
    def create_content(self):


        s = self.slide

        bg = SVGMobject(str(_PROJECT_ROOT / 'img/logo/tud-logo.svg'))
        bg.set_color(custom_colors.PRIMARY_COLOR)
        bg.move_to(ORIGIN, aligned_edge=ORIGIN).scale(15).shift(RIGHT*1.25+UP*7)



        s.add(bg)

        title = TexWrapper(
            r'\raggedright  \textbf{Status Talk}\\' ,
            r'Integration of Multi-Perspective \\ ' \
            r'and Non-Monotonic Reasoning',
            font_size=42, 
            color=WHITE,
        ).to_edge(LEFT).shift(DOWN * 1.75)      



        authors = TexWrapper(r'\raggedright  Piotr Gorczyca \\ Computational Logic Group, TU Dresden', color=WHITE, font_size=32).next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
        venue_and_date = TexWrapper(r'\raggedright Dresden, February 5th, 2026', color=WHITE, font_size=32).next_to(authors, DOWN, aligned_edge=LEFT, buff=0)

        # images
        buff = 1
        tud = ImageMobject(str(_PROJECT_ROOT / "img/logo/TUD_Logos_final_RGB_TUD_Logo_horizontal_weiß_de.png")).scale_to_fit_width(3).to_corner(UL).shift(UP*0.5+LEFT*0.2)
        # iccl = ImageMobject(str(_PROJECT_ROOT / "img/logo/iccl_logo.png")).scale_to_fit_width(3.5).to_corner(DR).shift(RIGHT*0.25) 
        iccl = ImageMobject(str(_PROJECT_ROOT / "img/logo/iccl_logo.png")).scale_to_fit_width(3.5).next_to(tud, RIGHT, buff=buff) 
        cl = ImageMobject(str(_PROJECT_ROOT / "img/logo/CLGroup-line-brillantblau.png")).scale_to_fit_width(3).next_to(iccl, RIGHT, buff=buff) 
            

        # supervision = TexWrapper(r'\raggedleft \textbf{Supervision:}\\Dr. habil. Hannes Strass\\Prof. Dr. Sebastian Rudolph\\\textbf{Fachrefent:} \\Prof. Dr. Markus Krötzsch', color=custom_colors.D_BLUE, font_size=32).to_corner(DR).shift(UP*0.2 + RIGHT *.25)
        supervision = TexWrapper(r'\raggedleft \textbf{Supervisor:}\\Dr. habil. Hannes Strass\\\textbf{Fachrefent:} \\Prof. Dr. Markus Krötzsch').to_corner(DR).shift(UP*0.2 + RIGHT *.25)
        
        # \\Prof. Dr. Sebastian Rudolph\\\textbf{Fachrefent:} \\Prof. Dr. Markus Krötzsch', color=custom_colors.D_BLUE, font_size=32).to_corner(DR).shift(UP*0.2 + RIGHT *.25)




        self.slide.add(tud, title, authors, venue_and_date, iccl, cl, supervision)

        # diagram = make_dispute_diagram().scale(0.8).move_to(ORIGIN).shift(RIGHT*2.5+UP)
        # s.add(diagram)
        
        
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