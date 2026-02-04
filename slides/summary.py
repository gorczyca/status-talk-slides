from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper
from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 18  # adjust if integrating into main numbering

class Summary(BaseSlide):
    TITLE = r"Summary"

    def create_content(self):
        s = self.slide

        fs = 24  # uniform font size for this slide

        def w(text):
            return TexWrapper(rf"\parbox{{18cm}}{{\raggedright {text}}}", font_size=fs)

        # Intro (no slide title element; rely on footer/title bar)
        intro = w("Two approaches to multi-perspective, non-monotonic reasoning:").to_corner(UL, buff=0.6).shift(DOWN)

        # Three vertical sections, left-aligned
        proc_section = VGroup(
            TexWrapper(r"\textbf{Procedural (ASP / argumentation)}", font_size=fs),
            w(r"$\bullet$ First multi-shot ASP implementation of argument games."),
            w(r"$\bullet$ Modular and declarative design, separating formal definitions (ASP) from procedural control (Python)."),
            w(r"$\bullet$ Extensible: interactivity, visualisation, additional semantics."),
            w(r"$\bullet$ Outperforms existing dispute-based ABA systems (e.g. \texttt{flexABle})."),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        decl_section = VGroup(
            TexWrapper(r"\textbf{Declarative (Generalising S4F and Standpoint Logic)}", font_size=fs),
            w(r"$\bullet$ Explored multiple approaches to integrating standpoint modalities into S4F."),
            w(r"$\bullet$ Adding standpoint modalities does not increase complexity (in monotonic or non-monotonic case)."),
            w(r"$\bullet$ Yields standpoint-enhanced variants of non-monotonic reasoning formalisms (default logic, argumentation, logic programs\ldots)"),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        sections = VGroup(proc_section, decl_section).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        sections.next_to(intro, DOWN, buff=0.5, aligned_edge=LEFT)

        # Reveal intro, then procedural block, then declarative block
        s.add(intro)
        s.wait()
        s.next_slide()

        s.add(proc_section)
        s.wait()
        s.next_slide()

        s.add(decl_section)
        s.wait()


class SummaryScene(Slide):
    def construct(self):
        Summary(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
