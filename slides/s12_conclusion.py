from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, bullet_line
from slides.shared.colors import D_BLUE, LAT_ORANGE

from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 12


class S12Conclusion(BaseSlide):
    TITLE = r'Conclusion'

    def create_content(self):
        s = self.slide

        items = [
            r'\textbf{first multi-shot ASP implementation} of argument games (ABA \& AFs)',
            r'modular and declarative design separating \textbf{formal definitions} (in ASP) from \textbf{procedural control} (in Python)',
            r'easily extensible -- \textbf{interactivity}, \textbf{visualization} (via \texttt{clingraph} [Hahn et al. 2024]), \textbf{additional semantics} (e.g. stable) can be added by providing only a few extra ASP rules',
            r'\textbf{outperforms} existing dispute-based ABA systems (e.g. flexABle)',
            r'suggests multi-shot ASP as a \textbf{general, adaptable framework} for implementing and comparing argument games across formalisms'
        ]

        items_group = VGroup(*[bullet_line(t) for t in items]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(RIGHT*.25)

        for b in items_group:
            s.wait()
            s.next_slide()
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            s.add(b)

        # s.wait()


class S12ConclusionScene(Slide):
    def construct(self):
        S12Conclusion(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
