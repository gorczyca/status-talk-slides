from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper
from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 19  # adjust if integrating into main numbering

class PublicationsSummary(BaseSlide):
    TITLE = r"Publications Summary"

    def create_content(self):
        s = self.slide

        fs = 24  # uniform font size for this slide

        def w(text):
            return TexWrapper(rf"\parbox{{15cm}}{{\raggedright {text}}}", font_size=fs)


        # Three vertical sections, left-aligned
        in_scope = VGroup(
            TexWrapper(r"\textbf{Dissertation publications}", font_size=fs),
            w(r"$\bullet$ Piotr Gorczyca, Hannes Straß. \textit{``Non-Monotonic S4F Standpoint Logic.''} (AAAI 2026)"),
            w(r"$\bullet$ Martin Diller, Piotr Gorczyca. \textit{``ABA Disputes in ASP: Advancing Argument Games through Multi-Shot Solving.''} PRIMA (2025)."),
            w(r"$\bullet$ Piotr Gorczyca, Hannes Straß. \textit{``Adding Standpoint Modalities to Non-Monotonic S4F: Preliminary Results.''} (NMR 2024)"),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        out_scope = VGroup(
            TexWrapper(r"Publications (outside the dissertation scope)", font_size=fs),
            w(r"$\bullet$ Piotr Gorczyca, Dörthe Arndt, Martin Diller, Jochen Hampe, Georg Heidenreich, Pascal Kettmann, Markus Krötzsch, Stephan Mennicke, Sebastian Rudolph, Hannes Straß. \textit{``Supporting Risk Management for Medical Devices via the Riskman Ontology and Shapes.''} SEMANTiCS (2025).")
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        sections = VGroup(in_scope, out_scope).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_edge(UL).shift(DOWN + RIGHT)

        s.add(sections)
        s.wait()


class PublicationsSummaryScene(Slide):
    def construct(self):
        PublicationsSummary(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
