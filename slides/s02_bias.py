from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, bullet_line
from slides.shared.colors import D_BLUE, LAT_ORANGE

from slides.shared.slide_count import SLIDES, SLIDES_NO

from slides.shared.common import FONT_SIZE_TEXT


SLIDE_NO = 2




class S02Bias(BaseSlide):
    TITLE = r'Bias Toward Inference-Based Approaches'

    def create_content(self):
        s = self.slide


        items = [
            r'Research on implementation methods arguably biased toward \textbf{abstract} and \mbox{\textbf{inference}-focused} models',
            r'\textbf{ICCMA} focuses on decision problems and only added a structured (ABA) track in 2023'
        ]

        bullets = VGroup(*[bullet_line(t) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(UP+RIGHT*.25)

        for b in bullets:
            s.wait()
            s.next_slide()
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            s.add(b)
            # s.next_slide()

        reasons_text = TexWrapper(r'Some likely reasons:', font_size=FONT_SIZE_TEXT).to_edge(LEFT).shift(DOWN+RIGHT*.25)
        reasons_items = [
            r"Simplicity and popularity of Dung's AFs",
            r'Reduction-based methods (\textbf{SAT/ASP} work especially well for inference)'
        ]


        r_bullets = VGroup(*[bullet_line(t) for t in reasons_items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(reasons_text, DOWN, aligned_edge=LEFT)

        s.wait()
        s.next_slide()
        s.add(reasons_text)
        

        for b in r_bullets:
            s.wait()     
            s.next_slide()     
            s.add(b)



class S02BiasScene(Slide):
    def construct(self):
        S02Bias(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
