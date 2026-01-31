from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, bullet_line
from slides.shared.colors import D_BLUE, LAT_ORANGE

from slides.shared.common import FONT_SIZE_TEXT

from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 9


class S09EvaluationSetup(BaseSlide):
    TITLE = r'Evaluation Setup'

    def create_content(self):
        s = self.slide

        # WIDTH = 13
        BUFF=3


        solvers_text = TexWrapper(r'Solvers:', font_size=FONT_SIZE_TEXT).to_edge(LEFT).shift(UP*2+RIGHT*.25)
        solvers_items = [
            r'\textbf{MS-DIS} -- lightweight Multi-Shot ASP \textbf{dispute-based} solver',
            r'\textbf{flexABle} [Diller, Gaggl, Gorczyca 2022] -- state-of-the-art ABA \textbf{dispute-based} solver, written in Scala',
            r'\textbf{aspforaba} [Lehtonen, Wallner, Järvisalo 2023] -- \textbf{reduction-based} one-shot \mbox{ASP solver} -- upper bound on performance',
        ]

        bullets = VGroup(*[bullet_line(t) for t in solvers_items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(solvers_text, DOWN, aligned_edge=LEFT)

        s.add(solvers_text)
        for b in bullets:
            s.wait()
            s.next_slide()
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            s.add(b)

        setup = TexWrapper(r'Setup:', font_size=FONT_SIZE_TEXT).next_to(solvers_text, DOWN, buff=BUFF, aligned_edge=LEFT)
        setup_items = [
            r"ICCMA'23 ABA track instances (containing 25-5000 atoms)",
            r'600s timeout'
        ]


        r_bullets = VGroup(*[bullet_line(t) for t in setup_items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(setup, DOWN, aligned_edge=LEFT)

        s.wait()
        s.next_slide()
        # s.play(FadeIn(setup))
        s.add(setup)

        for b in r_bullets:
            s.wait()
            s.next_slide()
            s.add(b)

class S09EvaluationSetupScene(Slide):
    def construct(self):
        S09EvaluationSetup(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
