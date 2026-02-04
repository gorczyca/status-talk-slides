from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.common import highlight_box
from slides.shared.graphs import fixed_arrow_graph, curved_arrow

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 7

# Colors for ABA dispute
PROP_COLOR = ["#E8FFE8", "#B5FFB5"]
DEFEAT_COLOR = ["#FFE8E8", "#FFB5B5"]
OPPONENT_COLOR = ["#FFFBE8", "#FFF1B5"]


class SAbaExamples(BaseSlide):
    TITLE = r'Computing Disputes via ASP: Abstract and ABA AFs'

    def create_content(self):
        s = self.slide

        def fixed_arrow_graph_local(n1, n2, tip_h=0.2, tip_w=0.16, stroke=2, color=BLACK):
            c1, c2 = n1.get_center(), n2.get_center()
            v = c2 - c1
            u = normalize(v)
            ang = angle_of_vector(v)
            p1 = n1.point_at_angle(ang)
            p2 = n2.point_at_angle(ang + PI)
            end = p2 - u * tip_h
            shaft = Line(p1, end, color=color, stroke_width=stroke)
            w = rotate_vector(u, PI / 2) * (tip_w / 2)
            base_center = end
            apex = end + u * tip_h
            tip = Polygon(apex, base_center - w, base_center +
                          w).set_fill(color, 1).set_stroke(width=0)
            return VGroup(shaft, tip)

        def highlight(node, color=YELLOW, opacity=0.75):
            h = node.copy().set_fill(color, opacity).set_stroke(width=0).set_z_index(0)
            return h

        # ==================== PART 1: Abstract AF ====================
        # Create the graph nodes
        Y_SHIFT = 0.5
        X_SHIFT = 2
        RADIUS = 0.3
        c_node = Circle(radius=RADIUS, color=BLACK).add(
            MathTexWrapper(r"c").set_z_index(99))
        d_node = Circle(radius=RADIUS, color=BLACK).add(
            MathTexWrapper(r"d").set_z_index(99)).next_to(c_node, RIGHT*X_SHIFT)
        a_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(
            r"a").set_z_index(99)).next_to(d_node, RIGHT*X_SHIFT).shift(DOWN*Y_SHIFT)
        e_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(
            r"e").set_z_index(99)).next_to(c_node, LEFT*X_SHIFT).shift(DOWN*Y_SHIFT)
        b_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(
            r"b").set_z_index(99)).next_to(c_node, LEFT*X_SHIFT).shift(UP*Y_SHIFT)

        edges = [(a_node, e_node), (b_node, c_node), (c_node, d_node),
                 (d_node, a_node), (e_node, b_node), (e_node, c_node)]

        graph_obj = VGroup(a_node, b_node, c_node, d_node, e_node, *
                           [fixed_arrow_graph_local(u, v) for u, v in edges]).scale(0.8)
        graph_obj.move_to(ORIGIN).shift(LEFT*2 + UP*0.5)

        # Static output on the right side
        output_title = TexWrapper(r'Output:', font_size=28)
        output_lines = VGroup(
            TexWrapper(r'\texttt{m(0,p,d).}', font_size=25),
            TexWrapper(r'\texttt{m(1,o,c).}', font_size=25),
            TexWrapper(r'\texttt{m(2,p,e).}', font_size=25),
        )
        output_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        output_group = VGroup(output_title, output_lines).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        output_group.next_to(graph_obj, RIGHT, buff=1.5, aligned_edge=UP)

        # Add static output first
        s.add(output_group)

        # Animate the graph
        # s.play(Write(graph_obj))
        s.add(graph_obj)
        s.wait()
        s.next_slide()

        # Add node highlights to show the final state
        d_node_green = highlight(d_node, color=[GREEN, WHITE])
        a_node_red = highlight(a_node, color=[RED, WHITE])
        c_node_yellow = highlight(c_node, color=[YELLOW, WHITE])
        e_node_green = highlight(e_node, color=[GREEN, WHITE])
        c_node_red = highlight(c_node, color=[RED, WHITE])
        b_node_red = highlight(b_node, color=[RED, WHITE])

        s.play(FadeIn(d_node_green))
        s.play(FadeIn(a_node_red))
        s.play(FadeIn(c_node_yellow))
        s.play(FadeIn(e_node_green))
        s.play(FadeIn(c_node_red), FadeIn(b_node_red), FadeOut(c_node_yellow))

        s.wait()
        s.next_slide()

        # ==================== PART 2: ABA Dispute ====================
        # Fade out the first graph
        af_content = VGroup(graph_obj, output_group, d_node_green,
                            a_node_red, c_node_yellow, e_node_green, c_node_red, b_node_red)
        s.play(FadeOut(af_content))
        s.wait()

        # ABA Framework definition
        FONT_SIZE = 30
        BUFF = 0.05
        assumptions = TexWrapper(
            r'$\frA=\set{a,b,c,d,e,\bar{e},f}$', font_size=FONT_SIZE).to_corner(UL).shift(DOWN+RIGHT)
        rules = TexWrapper(r'$\frR=\{ s \gets d,p,a; \;\; p\gets\bar{c}; \;\; \bar{c} \gets f; $',
                           font_size=FONT_SIZE).next_to(assumptions, DOWN, aligned_edge=LEFT, buff=BUFF*2)
        rules_2 = TexWrapper(r'$\bar{a} \gets b,t; \;\; \bar{d} \gets e;   \;\; t\gets c \;\;\; \}$',
                             font_size=FONT_SIZE).next_to(rules, DOWN, aligned_edge=LEFT, buff=BUFF).shift(RIGHT*.82)

        s.add(assumptions, rules, rules_2)
        s.wait()
        s.next_slide()

        # ABA Output (static)
        FONT_SIZE_OUTPUT = 30
        output_str = TexWrapper(r'Output:', font_size=FONT_SIZE_OUTPUT)
        m_1 = TexWrapper(r'\texttt{m(1,p,pb1,}$s\gets d,p,a$\texttt{).}}',
                         font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_2 = TexWrapper(r'\texttt{m(2,o,ob2,}$\bar{a}\gets b,t$\texttt{).}}',
                         font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_2_1 = TexWrapper(r'\texttt{m(2,o,ob2,}$\bar{d}\gets e$\texttt{).}}',
                           font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_3 = TexWrapper(r'\texttt{m(3,o,ob1,}$t\gets c$\texttt{).}}',
                         font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_4 = TexWrapper(r'\texttt{m(4,p,pf2,$\bar{e}$).}',
                         font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_5 = TexWrapper(r'\texttt{m(5,p,pb1,}$p\gets \bar{c}$\texttt{).}}',
                         font_size=FONT_SIZE_OUTPUT).set_z_index(99)
        m_6 = TexWrapper(r'\texttt{m(6,p,pb1,}$\bar{c}\gets f$\texttt{).}}',
                         font_size=FONT_SIZE_OUTPUT).set_z_index(99)

        aba_output_group = VGroup(output_str, m_1, m_2, m_2_1, m_3, m_4, m_5, m_6).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).to_edge(RIGHT).shift(DOWN*.75+LEFT)

        # Add output statically
        s.add(aba_output_group)
        s.wait()
        s.next_slide()

        # ABA Dispute graph nodes
        ABA_RADIUS = 0.25
        STROKE_WIDTH = 1
        HOR_DIST = 0.5

        s_node = Circle(radius=ABA_RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(
            MathTexWrapper("s")).set_z_index(99).next_to(aba_output_group, LEFT, buff=1.5)

        # s.play(Create(s_node))
        # s.play(Circumscribe(s_node, color=GREEN))
        s.next_slide()

        d = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(
            MathTexWrapper("d")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST).shift(UP)
        p = Circle(radius=ABA_RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(
            MathTexWrapper("p")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST)
        a = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(
            MathTexWrapper("a")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST).shift(DOWN)
        xc = Circle(radius=ABA_RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(
            MathTexWrapper(r"\bar{c}")).set_z_index(99).next_to(p, LEFT, buff=HOR_DIST)
        f = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(
            MathTexWrapper("f")).set_z_index(99).next_to(xc, LEFT, buff=HOR_DIST)
        xd = Circle(radius=ABA_RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(
            MathTexWrapper(r"\bar{d}")).set_z_index(99).next_to(f, LEFT, buff=1.5*HOR_DIST).shift(UP)
        e = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(
            MathTexWrapper("e")).set_z_index(99).next_to(xd, LEFT, buff=HOR_DIST)
        xa = Circle(radius=ABA_RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(
            MathTexWrapper(r"\bar{a}")).set_z_index(99).next_to(f, LEFT, buff=1.5*HOR_DIST).shift(DOWN)
        b = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(
            MathTexWrapper("b")).set_z_index(99).next_to(xa, LEFT, buff=HOR_DIST).shift(.5*UP)
        t = Circle(radius=ABA_RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(
            MathTexWrapper("t")).set_z_index(99).next_to(xa, LEFT, buff=HOR_DIST).shift(.5*DOWN)
        c = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(
            MathTexWrapper("c")).set_z_index(99).next_to(t, LEFT, buff=HOR_DIST)
        xe = Circle(radius=ABA_RADIUS, color=BLACK, stroke_width=STROKE_WIDTH, fill_color=PROP_COLOR, fill_opacity=1).add(
            MathTexWrapper(r"\bar{e}")).set_z_index(99).next_to(e, LEFT, buff=HOR_DIST)

        # m_1: s <- d,p,a
        s.play(FadeIn(VGroup(s_node,
                             d, p, a,
                             fixed_arrow_graph(
                                 d, s_node.get_left()+UP*0.1, color=BLACK),
                             fixed_arrow_graph(
                                 a, s_node.get_left()+DOWN*0.1, color=BLACK),
                             fixed_arrow_graph(p, s_node.get_left(), color=BLACK)),
                      highlight_box(VGroup(s_node, d, p, a), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=True).set_z_index(3)))
        # s.next_slide()

        # m_2, m_2_1: opponent attacks
        e_xd = highlight_box(VGroup(e, xd), fill_opacity=1,
                             fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(0)
        s.play(FadeIn(VGroup(e, xd, fixed_arrow_graph(e, xd.get_left(
        ), color=BLACK), e_xd, fixed_arrow_graph(xd, d.get_left(), color=RED))))
        # s.next_slide()

        t_b_xa = highlight_box(VGroup(t, b, xa), stroke_width=STROKE_WIDTH, fill_opacity=1,
                               fill_color=OPPONENT_COLOR, dashed=True, buff=0.15).set_z_index(1)
        s.play(FadeIn(VGroup(t, b, xa, fixed_arrow_graph(b, xa.get_left()+UP*0.1, color=BLACK), fixed_arrow_graph(t,
               xa.get_left()+DOWN*0.1, color=BLACK), t_b_xa, fixed_arrow_graph(xa, a.get_left(), color=RED))))
        # s.next_slide()

        # m_3: t <- c
        c_t = highlight_box(VGroup(c, t), stroke_width=STROKE_WIDTH, fill_opacity=1,
                            fill_color=OPPONENT_COLOR, dashed=True, buff=0.1).set_z_index(5)
        opp_arg = highlight_box(
            VGroup(c_t, b, xa), buff=0.3, fill_color=OPPONENT_COLOR, dashed=False).set_z_index(0)
        s.play(FadeIn(VGroup(c, fixed_arrow_graph(
            c, t.get_left(), color=BLACK), c_t, opp_arg)))
        # s.next_slide()

        # m_4: proponent plays xe
        s.play(FadeIn(VGroup(xe, fixed_arrow_graph(xe, e.get_left(), color=RED))),
                e_xd[0].animate.set_fill(DEFEAT_COLOR, opacity=1))
        # s.next_slide()

        # # m_5: p <- xc
        xc_p = highlight_box(VGroup(xc, p), fill_opacity=1, fill_color=PROP_COLOR, buff=0.15, dashed=True).set_z_index(4)
        s.play(FadeIn(VGroup(xc, fixed_arrow_graph(xc, p.get_left(), color=BLACK), xc_p)))
        # s.play(FadeIn(xc_p))
        
        # s.next_slide()
        s.play(FadeIn(curved_arrow(xc.get_bottom(), c.get_right() + 0.1*DOWN+0.2*RIGHT, bend=1, color=RED)), 
            c_t[0].animate.set_fill(DEFEAT_COLOR, opacity=1), t_b_xa[0].animate.set_fill(DEFEAT_COLOR, opacity=1), opp_arg[0].animate.set_fill(DEFEAT_COLOR, opacity=1))
        # s.next_slide()

        # # m_6: xc <- f
        f_xc = highlight_box(VGroup(f, xc), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=True).set_z_index(5)
        s_arg = highlight_box(VGroup(f, s_node, d, a), fill_opacity=1, fill_color=PROP_COLOR, buff=0.3, dashed=False).set_z_index(0)
        s.play(FadeIn(VGroup(f, fixed_arrow_graph(f, xc.get_left(), color=BLACK), f_xc, s_arg)))
        s.wait()


class SAbaExamplesScene(Slide):
    def construct(self):
        SAbaExamples(self, show_footer=True,
                     slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
