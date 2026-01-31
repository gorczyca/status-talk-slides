from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper, bullet_line
from slides.shared.colors import D_BLUE, LAT_ORANGE
from slides.shared.asp_lexer import set_asp_lexer, get_asp_code

from slides.shared.slide_count import SLIDES, SLIDES_NO
from slides.shared.common import FONT_SIZE_TEXT


SLIDE_NO = 5
CODE_W = 5.5


set_asp_lexer()

def example_box(mobj):
    box = SurroundingRectangle(mobj, color=GREEN, stroke_width=1.5, buff=0.1).set_fill(color=[GREEN,WHITE], opacity=0.15)
    return VGroup(box, mobj)


class S05ABAFramework(BaseSlide):
    TITLE = r'Extension to ABA Disputes: Framework'

    def create_content(self):
        s = self.slide

        FONT_SIZE = FONT_SIZE_TEXT
        BUFF=0.1
        VERTICAL_BUFF = .8
        FONT_SIZE_CODE = 18
        X = 0

        SHIFT_RIGHT = 0.35*RIGHT

        framework_text = MathTexWrapper(r'\frF=\frTup', font_size=FONT_SIZE).to_edge(LEFT).shift(UP*2+RIGHT*.25)

        language_l = bullet_line(r'Language $\frL$').next_to(framework_text, DOWN, aligned_edge=LEFT)
        # language_l = TexWrapper(r'Language $\frL$', font_size=FONT_SIZE).next_to(framework_text, DOWN, aligned_edge=LEFT).shift(.5*RIGHT)
        example_language_l = example_box(MathTexWrapper(r'\set{ a,b,c,d,e,f,g\ldots }', font_size=FONT_SIZE)).next_to(language_l, DOWN, aligned_edge=LEFT, buff=BUFF).shift(SHIFT_RIGHT)
        language_code = get_asp_code('./code/aba-framework/language.lp', font_size=FONT_SIZE_CODE).move_to([X, language_l.get_top()[1], 0], aligned_edge=UL)

        assumptions_a = bullet_line(r'Assumptions $\frA\subseteq\frL$').next_to(language_l, DOWN, aligned_edge=LEFT, buff=VERTICAL_BUFF)
        example_assumptions_a = example_box(MathTexWrapper(r'\set{ b,d,\ldots }', font_size=FONT_SIZE)).next_to(assumptions_a, DOWN, aligned_edge=LEFT,  buff=BUFF).shift(SHIFT_RIGHT)
        assumptions_code = get_asp_code('./code/aba-framework/assumptions.lp', font_size=FONT_SIZE_CODE).move_to([X, assumptions_a.get_top()[1], 0], aligned_edge=UL)
        
        contraries = bullet_line(r'Contrary function $\frCtr:\frA\mapsto\frL$').next_to(assumptions_a, DOWN, aligned_edge=LEFT, buff=VERTICAL_BUFF)
        example_contraries = example_box(MathTexWrapper(r'\bar{b}=c,\bar{d}=a,\ldots', font_size=FONT_SIZE)).next_to(contraries, DOWN, aligned_edge=LEFT,  buff=BUFF).shift(SHIFT_RIGHT)
        contraries_code = get_asp_code('./code/aba-framework/contraries.lp', font_size=FONT_SIZE_CODE).move_to([X, contraries.get_top()[1], 0], aligned_edge=UL)
        
        rules = bullet_line(r'Rules $h\leftarrow B$ with $h\in\frL\setminus\frA$, $B\subseteq \frL$').next_to(contraries, DOWN, aligned_edge=LEFT, buff=VERTICAL_BUFF)
        example_rules = example_box(MathTexWrapper(r'\set{d \leftarrow c,e,\ldots }', font_size=FONT_SIZE)).next_to(rules, DOWN, aligned_edge=LEFT,  buff=BUFF).shift(SHIFT_RIGHT)
        rules_code = get_asp_code('./code/aba-framework/rules.lp', font_size=FONT_SIZE_CODE).move_to([X, rules.get_top()[1], 0], aligned_edge=UL)

        s.add(framework_text)
        
        s.wait()
        s.next_slide()

        # s.play(FadeIn(language_l, shift=0.2*RIGHT), FadeIn(example_language_l, shift=0.2*RIGHT))
        s.add(language_l)
        # s.wait()
        # s.next_slide()
        s.add(example_language_l)
        s.wait()
        s.next_slide()
        s.add(language_code)
        s.wait()
        s.next_slide()


        # s.play(FadeIn(assumptions_a, shift=0.2*RIGHT), FadeIn(example_assumptions_a, shift=0.2*RIGHT))
        s.add(assumptions_a)
        # s.wait()
        # s.next_slide()
        s.add(example_assumptions_a)        
        s.wait()
        s.next_slide()        
        s.add(assumptions_code)
        s.wait()
        s.next_slide()

        s.add(contraries)
        # s.wait()
        # s.next_slide()
        s.add(example_contraries)
        s.wait()
        s.next_slide()
        s.add(contraries_code)
        s.wait()
        s.next_slide()

        # s.play(FadeIn(rules, shift=0.2*RIGHT), FadeIn(example_rules, shift=0.2*RIGHT))
        s.add(rules) 
        # s.wait()
        # s.next_slide()
        s.add(example_rules)
        s.wait()
        s.next_slide()
        # s.play(FadeIn(rules_code))
        s.add(rules_code)
        # s.wait()
        # s.next_slide()


class S05AbaFrameworkScene(Slide):
    def construct(self):
        S05ABAFramework(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
