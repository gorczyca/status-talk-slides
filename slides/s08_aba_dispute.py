from manim import *
from manim_slides import Slide

from slides.s11_evaluation2 import HIGHLIGHT_COLOR
from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper
from slides.shared.colors import D_BLUE, LAT_ORANGE
from slides.shared.common import highlight_box
from slides.shared.graphs import fixed_arrow_graph, curved_arrow

from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 8




class S08ABADispute(BaseSlide):
    TITLE = r'Extension to ABA Disputes: Dispute'

    def create_content(self):
        s = self.slide

        # framework        
        FONT_SIZE = 30
        BUFF=0.05
        assumptions = TexWrapper(r'$\frA=\set{a,b,c,d,e,\bar{e},f}$, $\frCtr(x)=\bar{x}$ for $x\in\frA$', font_size=FONT_SIZE).to_corner(UR).shift(DOWN)
        rules = TexWrapper(r'$\frR=\{ s \gets d,p,a; \;\; p\gets\bar{c}; \;\; \bar{c} \gets f; $', font_size=FONT_SIZE).next_to(assumptions, DOWN, aligned_edge=LEFT, buff=BUFF*2)
        rules_2 = TexWrapper(r'$\bar{a} \gets b,t; \;\;\;\;\;\; \bar{d} \gets e;   \;\; t\gets c \;\;\; \}$', font_size=FONT_SIZE).next_to(rules, DOWN, aligned_edge=LEFT, buff=BUFF).shift(RIGHT*.85)

        s.add(assumptions, rules, rules_2)
        s.wait()
        s.next_slide()



        FONT_SIZE_OUTPUT = 30
        output_str = TexWrapper(r'Output:', font_size=FONT_SIZE_OUTPUT)
        m_1 = TexWrapper(r'\texttt{m(1,p,pb1,}$s\gets d,p,a$\texttt{).}}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_2 = TexWrapper(r'\texttt{m(2,o,ob2,}$\bar{a}\gets b,t$\texttt{).}}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_2_1 = TexWrapper(r'\texttt{m(2,o,ob2,}$\bar{d}\gets e$\texttt{).}}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_3 = TexWrapper(r'\texttt{m(3,o,ob1,}$t\gets c$\texttt{).}}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_4 = TexWrapper(r'\texttt{m(4,p,pf2,$\bar{e}$).}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_5 = TexWrapper(r'\texttt{m(5,p,pb1,}$p\gets \bar{c}$\texttt{).}}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_6 = TexWrapper(r'\texttt{m(6,p,pb1,}$\bar{c}\gets f$\texttt{).}}', font_size=FONT_SIZE_OUTPUT).set_z_index(99)

        output_group = VGroup(output_str, m_1, m_2, m_2_1, m_3, m_4, m_5, m_6).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(assumptions, DOWN, buff=1.5)
                
        s.play(Write(output_group))
        s.next_slide()


        # highlight first move
        HIGHLIGHT_FILL_OPACITY=0.2
        HIGHLIGHT_BUFF=0.05


        PROP_COLOR = [ "#E8FFE8", "#B5FFB5" ]
        DEFEAT_COLOR=["#FFE8E8", "#FFB5B5"]
        OPPONENT_COLOR=["#FFFBE8", "#FFF1B5"]

        ATTACK_COLOR = RED
        # draw the dispute
        RADIUS = 0.25
        STROKE_WIDTH=1
        CIRCLE_BUFF = 0.2

        HOR_DIST = 0.5

        s_node = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("s")).set_z_index(99).next_to(output_group, LEFT, buff=1.75)

        s.play(Create(s_node)); s.play(Circumscribe(s_node, color=GREEN))
        s.next_slide()

        d = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("d")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST).shift(UP)
        p = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("p")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST)
        a = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("a")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST).shift(DOWN)
        xc = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\bar{c}")).set_z_index(99).next_to(p, LEFT, buff=HOR_DIST)
        f = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("f")).set_z_index(99).next_to(xc, LEFT, buff=HOR_DIST)
        xd = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\bar{d}")).set_z_index(99).next_to(f, LEFT, buff=1.5*HOR_DIST).shift(UP)
        e = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("e")).set_z_index(99).next_to(xd, LEFT, buff=HOR_DIST)
        xa = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\bar{a}")).set_z_index(99).next_to(f, LEFT, buff=1.5*HOR_DIST).shift(DOWN)
        b = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("b")).set_z_index(99).next_to(xa, LEFT, buff=HOR_DIST).shift(.5*UP)
        t = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("t")).set_z_index(99).next_to(xa, LEFT, buff=HOR_DIST).shift(.5*DOWN)
        c = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("c")).set_z_index(99).next_to(t, LEFT, buff=HOR_DIST)
        xe = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH,     fill_color=PROP_COLOR, fill_opacity=1).add(MathTexWrapper(r"\bar{e}")).set_z_index(99).next_to(e, LEFT, buff=HOR_DIST)

        
        s.next_slide()
        highlight_code_line = highlight_box(output_group[1], fill_color=HIGHLIGHT_COLOR, fill_opacity=HIGHLIGHT_FILL_OPACITY, buff=HIGHLIGHT_BUFF)
        s.add(highlight_code_line)
        s.play(FadeIn(highlight_code_line))

        s.next_slide()
        s.play(Create(VGroup(
            d, p, a,
            fixed_arrow_graph(d, s_node.get_left()+UP*0.1, color=BLACK),
            fixed_arrow_graph(a, s_node.get_left()+DOWN*0.1, color=BLACK),
            fixed_arrow_graph(p, s_node.get_left(), color=BLACK))))
        s.play(DrawBorderThenFill(
            highlight_box(VGroup(s_node, d, p, a), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=True).set_z_index(3)))
        
        
        s.next_slide()
        s.play(Transform(highlight_code_line, highlight_box(VGroup(output_group[2], output_group[3]), fill_color=HIGHLIGHT_COLOR, fill_opacity=HIGHLIGHT_FILL_OPACITY, buff=HIGHLIGHT_BUFF)))
        s.next_slide()

        e_xd = highlight_box(VGroup(e, xd), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(0)
        s.play(Create(VGroup(e,xd, fixed_arrow_graph(e, xd.get_left(), color=BLACK))))
        s.play(DrawBorderThenFill(e_xd))
        s.play(Create(fixed_arrow_graph(xd, d.get_left(), color=RED))),
        s.next_slide()
        # 

        t_b_xa = highlight_box(VGroup(t, b, xa), stroke_width=STROKE_WIDTH, fill_opacity=1, fill_color=OPPONENT_COLOR, dashed=True, buff=0.15).set_z_index(0)
        s.play(Create(VGroup(t,b,xa, fixed_arrow_graph(b, xa.get_left()+UP*0.1, color=BLACK),fixed_arrow_graph(t, xa.get_left()+DOWN*0.1, color=BLACK))))
        s.play(DrawBorderThenFill(t_b_xa))
        s.play(Create(fixed_arrow_graph(xa,a.get_left(), color=RED)))
        s.next_slide()

        s.play(Transform(highlight_code_line, highlight_box(output_group[4], fill_color=HIGHLIGHT_COLOR, fill_opacity=HIGHLIGHT_FILL_OPACITY, buff=HIGHLIGHT_BUFF)))
        s.next_slide()
        s.play(Create(VGroup(c, fixed_arrow_graph(c, t.get_left(), color=BLACK))))
        c_t = highlight_box(VGroup(c, t), stroke_width=STROKE_WIDTH, fill_opacity=1, fill_color=OPPONENT_COLOR, dashed=True, buff=0.1).set_z_index(5)
        s.play(DrawBorderThenFill(c_t))
        opp_arg = highlight_box(VGroup(c_t, b, xa), buff=0.3, fill_color=OPPONENT_COLOR, dashed=False)
        s.play(DrawBorderThenFill(opp_arg))
        s.next_slide()

        s.play(Transform(highlight_code_line, highlight_box(output_group[5], fill_color=HIGHLIGHT_COLOR, fill_opacity=HIGHLIGHT_FILL_OPACITY, buff=HIGHLIGHT_BUFF)))
        s.next_slide()
        s.play(Create(xe))
        s.play(Create(fixed_arrow_graph(xe, e.get_left(), color=RED)))
        s.play(e_xd[0].animate.set_fill(DEFEAT_COLOR, opacity=1))
        s.next_slide()

        s.play(Transform(highlight_code_line, highlight_box(output_group[6], fill_color=HIGHLIGHT_COLOR, fill_opacity=HIGHLIGHT_FILL_OPACITY, buff=HIGHLIGHT_BUFF)))
        s.next_slide()
        s.play(Create(VGroup(xc, fixed_arrow_graph(xc, p.get_left(), color=BLACK))))
        xc_p = highlight_box(VGroup(xc, p), fill_opacity=1, fill_color=PROP_COLOR, buff=0.15, dashed=True).set_z_index(4)
        s.play(DrawBorderThenFill(xc_p))
        s.next_slide()
        s.play(Create(curved_arrow(xc.get_bottom(), c.get_right()+0.1*DOWN+0.2*RIGHT, bend=1, color=RED)))
        s.play(c_t[0].animate.set_fill(DEFEAT_COLOR, opacity=1), t_b_xa[0].animate.set_fill(DEFEAT_COLOR, opacity=1), opp_arg[0].animate.set_fill(DEFEAT_COLOR, opacity=1))
        s.next_slide()

        s.play(Transform(highlight_code_line, highlight_box(output_group[7], fill_color=HIGHLIGHT_COLOR, fill_opacity=HIGHLIGHT_FILL_OPACITY, buff=HIGHLIGHT_BUFF)))
        s.next_slide()
        s.play(Create(VGroup(f, fixed_arrow_graph(f, xc.get_left(), color=BLACK))))
        f_xc = highlight_box(VGroup(f, xc), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=True).set_z_index(5)
        s.play(DrawBorderThenFill(f_xc))
        s_arg = highlight_box(VGroup(f, s_node, d, a), fill_opacity=1, fill_color=PROP_COLOR, buff=0.3, dashed=False).set_z_index(0)
        s.play(DrawBorderThenFill(s_arg))
     


class S08AbaDisputeScene(Slide):
    def construct(self):
        S08ABADispute(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
