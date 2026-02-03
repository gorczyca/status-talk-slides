from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.asp_lexer import set_asp_lexer

from slides.shared.slide_count import SLIDES, SLIDES_NO

set_asp_lexer()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 1


class SAbaEncoding(BaseSlide):
    TITLE = r'Declarative ASP Implementation'

    def create_content(self):
        s = self.slide

        # Add image on the right side
        img = ImageMobject(str(_PROJECT_ROOT / "img/math-definitions.png"))
        img.scale_to_fit_height(5)
        img.to_edge(RIGHT, buff=0.5)
        s.add(img)

        # Shadow for definition box
        def_shadow = Rectangle(
            width=5, height=1,
            color=GREY_D,
            stroke_width=0,
            fill_color=GREY_D,
            fill_opacity=0.5
        )
        def_shadow.set_z_index(9)

        # Definition box with white background (centered, on top)
        def_box = Rectangle(
            width=5, height=1,
            color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1
        )
        def_box.set_z_index(10)

        # Position shadow slightly offset from the box
        def_shadow.move_to(def_box.get_center() + DOWN * 0.08 + RIGHT * 0.08)

        # Placeholder for definition text
        def_text = TexWrapper(
            r"Complete Proponent's Statements:\[ \mathbb{P}^* \eqdef (\mathbb{P}\cap \mathcal{A}) \cup \set{h \guard h \leftarrow B \in (\mathbb{P}\cap \mathcal{R}) \text{ and } B \subseteq \mathbb{P}^*}  \]", font_size=20)
        def_text.move_to(def_box)
        def_text.set_z_index(11)

        def_group = VGroup(def_shadow, def_box,
                           def_text).move_to(img.get_center())


        # ASP code snippets on the left side (light background)
        CODE_BG = {"fill_color": "#F5F5F5", "stroke_color": "#CCCCCC", "stroke_width": 1}

        asp_code_1 = Code(
            tab_width=2,
            code_string='''
% Framework encoding
head(1,p).
body(1,a). body(1,b). body(1,x).
assumption(x).
''',
            language='asp',
            formatter_style='default',
            add_line_numbers=False,
            background_config=CODE_BG,
        ).scale(0.6)

        # Math formula next to first listing (left aligned)
        math_1 = MathTexWrapper(r"\begin{aligned}[t] &\frR = \set{ p \leftarrow a,b,x }\\ &\frA = \set{x} \end{aligned}", font_size=24).to_edge(LEFT).shift(UP*1.75)
        s.add(math_1)

        asp_code_1.next_to(math_1, RIGHT, buff=0.5)
        s.wait()
        s.next_slide()

        s.add(asp_code_1)

        s.wait()
        s.next_slide()
        s.add(def_group)

        s.wait()
        s.next_slide()

        # math_1.next_to(asp_code_1, RIGHT, buff=0.3, aligned_edge=UP)

        asp_code_2 = Code(
            tab_width=2,
            code_string='''
% Complete Proponent's Statements
comPropSt(T,S) :- step(T), propSt(T-1,S), assumption(S).
comPropSt(T,H) :- step(T), propRule(T-1,RuleID), head(RuleID,H), 
                    comPropSt(T-1,B) : body(RuleID, B).
''',
            language='asp',
            formatter_style='default',
            add_line_numbers=False,
            background_config=CODE_BG,
        ).scale(0.6).next_to(def_box, LEFT, buff=0.2, aligned_edge=UP).shift(UP*0.15)

        s.add(asp_code_2)


        asp_code_3 = Code(
            tab_width=2,
            code_string='''
% Initialise the step counter
#const max_step = 99.
step(1..max_step).
''',
            language='asp',
            formatter_style='default',
            add_line_numbers=False,
            background_config=CODE_BG,
        ).scale(0.6).next_to(asp_code_2, DOWN, aligned_edge=LEFT, buff=.5)

        s.wait()
        s.next_slide()

        s.add(asp_code_3)

        # Arrange snippets vertically on the left
        # asp_snippets = VGroup(code_1_group, asp_code_2, asp_code_3)
        # asp_snippets.arrange(DOWN, buff=0.5)
        # asp_snippets.to_edge(LEFT, buff=0.5)
        # s.add(asp_snippets)


class SAbaEncodingScene(Slide):
    def construct(self):
        SAbaEncoding(self, show_footer=True,
                     slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
