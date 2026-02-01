from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, bullet_line, tex_paragraph
from slides.shared.colors import D_BLUE, LAT_ORANGE

from slides.shared.slide_count import SLIDES, SLIDES_NO
from slides.shared.common import FONT_SIZE_TEXT

SLIDE_NO = 1

WIDTH = 13
BUFF=1.5





class S01TwoPerspectives(BaseSlide):
    TITLE = r'Formal Argumentation: Two Perspectives'

    def create_content(self):
        s = self.slide


        m_types_text = TexWrapper(r'Model types:', font_size=FONT_SIZE_TEXT).to_edge(LEFT).shift(UP*2+RIGHT*.25)

        items = [
            r'\textbf{Abstract} (e.g. \textbf{Dung AFs}) -- focus on relations between arguments',
            r'\textbf{Structured} (e.g. \textbf{ABA}) -- include premises, rules and inference steps',
        ]

        bullets = VGroup(*[bullet_line(t) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(m_types_text, DOWN, aligned_edge=LEFT)

    
        s.add(m_types_text)
        for b in bullets:
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            s.wait()
            s.next_slide()
            s.add(b)
            # s.play(FadeIn(b, shift=0.2*RIGHT))

        reasoning_views_text = TexWrapper(r'Reasoning views:', font_size=FONT_SIZE_TEXT).next_to(m_types_text, DOWN, buff=BUFF, aligned_edge=LEFT)
        reasoning_views_text_items = [
            r'\textbf{Argumentation as inference} -- decide acceptable arguments or claims',
            r'\textbf{Argumentation as process} -- argumentation as the reasoning mechanism itself'
        ]


        r_bullets = VGroup(*[bullet_line(t) for t in reasoning_views_text_items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(reasoning_views_text, DOWN, aligned_edge=LEFT)

        s.wait()
        s.next_slide()
        # s.play(FadeIn(reasoning_views_text))
        s.add(reasoning_views_text)
        # s.wait()
        # s.next_slide()

        for b in r_bullets:
            s.wait()
            s.next_slide()
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            s.add(b)

        arg_text = tex_paragraph(r'\textbf{Argument games:} discussion between proponent and opponent; provide \mbox{dialectical} justifications, support interaction, connected to dialogical models $\rightarrow$ useful for XAI').next_to(reasoning_views_text, DOWN, buff=BUFF*1.15, aligned_edge=LEFT)

        # s.play(FadeIn(arg_text))
        s.wait()
        s.next_slide()
        s.add(arg_text)

        



class S01TwoPerspectivesScene(Slide):
    def construct(self):
        S01TwoPerspectives(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
