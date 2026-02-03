from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.asp_lexer import set_asp_lexer

from slides.shared.slide_count import SLIDES, SLIDES_NO

set_asp_lexer()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 4


class SAbaIntro(BaseSlide):
    TITLE = r'Argument Games: Implementations'

    def create_content(self):
        s = self.slide

        # Add image on the right side
        img = ImageMobject(str(_PROJECT_ROOT / "img/math-definitions.png"))
        img.scale_to_fit_height(5)
        img.to_edge(RIGHT, buff=0.5)

        bullet_texts = [
            r"\textbf{Argument games}: structured dialogue between proponent and opponent; provide dialectical justification and interaction; useful for XAI",
            r"\textbf{Argumentation as a process}: the reasoning mechanism itself, not just its outcome",
            r"\textbf{State of the art}: formalised in Diller, Gaggl, Gorczyca (2021); Scala implementation \texttt{flexABle} with $\sim$5.5k LOC",
            r"\textbf{Problem}: imperative implementations hard to maintain and grow in complexity with each added feature",
            r"\textbf{Idea}: declarative ASP implementation; using multi-shot grounding to avoid full re-grounding; first use of multi-shot ASP for argument games",
        ]


        def make_bullet(text: str) -> VGroup:
            dot = Dot(radius=0.06, color=self.FONT_COLOR)
            dot.shift(DOWN * 0.08)  # nudge marker slightly lower than text top
            body = TexWrapper(
                rf"\parbox[t]{{9cm}}{{\raggedright {text}}}",
                font_size=28,
                color=self.FONT_COLOR,
            )
            body.next_to(dot, RIGHT, buff=0.25, aligned_edge=UP).shift(UP*0.075)
            return VGroup(dot, body)

        bullets = VGroup(*[make_bullet(t) for t in bullet_texts])
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        bullets.to_edge(LEFT, buff=0.5)
        bullets.align_to(img, UP)

        # Reveal bullets one by one
        s.add(bullets[0])
        for i, bullet in enumerate(bullets[1:], 1):
            if i == 4:
                s.wait()
                s.next_slide()
                s.add(img)

            s.wait()
            s.next_slide()

            s.add(bullet)



class SAbaIntroScene(Slide):
    def construct(self):
        SAbaIntro(self, show_footer=True,
                     slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
