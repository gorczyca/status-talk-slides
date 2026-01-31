from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, bullet_line, enum_line
from slides.shared.colors import D_BLUE, LAT_ORANGE

from slides.shared.slide_count import SLIDES, SLIDES_NO

from slides.shared.common import FONT_SIZE_TEXT


SLIDE_NO = 3




class S03Advancing(BaseSlide):
    TITLE = r'Advancing Argument Games through Multi-Shot Solving'
    TITLE_FONT_SIZE = 45
    def create_content(self):
        s = self.slide

        items = [
            r'\textbf{ASP} widely used for implementing argumentation, but repeated grounding from scratch is costly in iterative scenarios',
            r'\textbf{Multi-shot ASP} allows updating and re-solving $\rightarrow$ avoids unnecessary \mbox{grounding} overhead',
            r'We present the \textbf{first use of multi-shot ASP} for argumentation games',
            r"Focus on \textbf{ABA dispute derivations} and \textbf{Dung's AFs}",
            r'\textbf{Rule-based flexible ABA disputes} from [Diller, Gaggl, Gorczyca 2021], \mbox{elaboration} on [Toni 2013], [Craven, Toni 2016]',
            r'\textbf{Multi-shot environment} provided by \texttt{clingo}~[Gebser et al. 2019]',
            # r"Offers a \textbf{declarative} and more streamlined implementation of argument games",
            # r"Provides a \textbf{general framework} for implementing and comparing argument games",
        ]

        # bullets_1 = VGroup(*[bullet_line(t) for t in items[0:6]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(RIGHT*.25)
        # bullets_2 = VGroup(*[bullet_line(t) for t in items[6:]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(RIGHT*.25+UP)
        # bullets = VGroup(*[bullet_line(t) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(RIGHT*.25+UP)
        bullets = VGroup(*[bullet_line(t) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(RIGHT*.25)

        for b in bullets:
            s.wait()
            s.next_slide()
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            s.add(b)
        
        s.wait()
        s.next_slide()
        # s.play(FadeOut(bullets))
        for b in bullets:
            s.remove(b)
        

        s.remove(bullets)

        # for b in bullets_1:
        #     s.play(FadeIn(b, shift=0.2*RIGHT))
        #     s.next_slide()
        
        # s.play(FadeOut(bullets_1))
        # s.remove(bullets_1)

        # for b in bullets_2:
        #     s.play(FadeIn(b, shift=0.2*RIGHT))
        #     s.next_slide()

        # next = TexWrapper(r'\textbf{Next}:', font_size=FONT_SIZE_TEXT).to_edge(LEFT).shift(DOWN*.5+RIGHT*.25)
        next = TexWrapper(r'\textbf{Next}:', font_size=FONT_SIZE_TEXT).to_edge(LEFT).shift(UP+RIGHT*.25)
        next_items = [
            r"Multi-shot ASP for Dung's AFs",
            r"Extension to ABA disputes",
            r"Empirical evaluation",
        ]

        lines_with_count = VGroup(*[enum_line(i, t) for i, t in enumerate(next_items, start=1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(next, DOWN, aligned_edge=LEFT)

        
        s.add(next)
        # s.play(FadeIn(next))
        # s.next_slide()

        for b in lines_with_count:
            s.wait()
            s.next_slide()
            s.add(b)
            # s.play(FadeIn(b, shift=0.2*RIGHT))
            




class S03AdvancingScene(Slide):
    def construct(self):
        S03Advancing(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
