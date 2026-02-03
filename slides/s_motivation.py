from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper, TextWrapper, TableWrapper
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot
from slides.shared.graphs import fixed_arrow_graph
from slides.shared.common import highlight_box

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 1


class SMotivation(BaseSlide):
    # TITLE = r'Non-Monotonic \& Multi-Perspective Reasoning'
    TITLE = r'Motivation: Procedural and Declarative Approaches'

    def create_content(self):
        s = self.slide

        quote_lines = VGroup(
            TexWrapper(r"\underline{According to the NIH:}", font_size=24, color=BLACK),
            TexWrapper(r"\textit{[PCOS is diagnosed in the presence of] \textbf{Oligo ovulation}}", font_size=22, color=BLACK),
            TexWrapper(r"\textit{and clinical and/or biological signs of \textbf{hyperandrogenism},}", font_size=22, color=BLACK),
            TexWrapper(r"\textit{and [assuming the] \textbf{exclusion of other aetiologies}.}", font_size=22, color=BLACK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        quote_lines.to_edge(LEFT, buff=1).shift(UP*1)
        s.add(quote_lines)

        s.wait()
        s.next_slide()

        # Create the two initial conditions
        oligo = TexWrapper('Oligovulation', font_size=24, color=BLACK)
        hyper = TexWrapper('Hyperandrogenism', font_size=24, color=BLACK)

        # Stack them vertically
        conditions = VGroup(oligo, hyper).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        conditions.next_to(quote_lines, DOWN, buff=0.8).to_edge(LEFT, buff=1.5)

        # Create brace and PCOS label
        brace = Brace(conditions, RIGHT, color=BLACK)
        pcos = TexWrapper('PCOS', font_size=24, color=BLACK)
        pcos.next_to(brace, RIGHT, buff=0.2)

        s.add
        s.add(conditions)

        s.wait()
        s.next_slide()

        s.play(FadeIn(pcos), GrowFromCenter(brace))

        s.wait()
        s.next_slide()

        # Add "Other aetiology" below
        other = TexWrapper('Other aetiology', font_size=24, color=BLACK)
        other.next_to(hyper, DOWN, aligned_edge=LEFT, buff=0.15)

        # Create new extended brace
        new_conditions = VGroup(oligo, hyper, other)
        new_brace = Brace(new_conditions, RIGHT, color=BLACK)

        # Calculate new PCOS position (next to new brace)
        new_pcos_pos = new_brace.get_right() + RIGHT * 0.6

        # Animate adding the third condition, extending the brace, and moving PCOS
        s.play(
            FadeIn(other),
            Transform(brace, new_brace),
            pcos.animate.move_to(new_pcos_pos),
        )

        s.wait()
        s.next_slide()

        # Cross out PCOS
        cross_line = Cross(pcos, color=RED, stroke_width=3).scale(1.05)
        s.play(FadeIn(cross_line))

        s.wait()
        s.next_slide()

        table = TableWrapper(data=[
            # Headers
            [
                r'''National Institutes of Health [$\sone$] criteria statement''',
                r'European Society for Human Reproduction and Embryology/American Society for Reproductive Medicine [$\stwo$] statement',
                r'Androgen Excess Society [$\sthree$] statement'],
            # Text
            [r'Oligo-ovulation [$\atomb$] and clinical and/or biochemical signs of hyperandrogenism [$\atoma$], and exclusion of other aetiologies [$\atomx$]',
             r'Two out of three of: oligo-ovulation and/or anovulation [$\atoma$], clinical and/or biochemical signs of hyperandrogenism [$\atomb$], or polycystic ovaries [$\atomc$], and exclusion of other aetiologies [$\atomx$]',
             r'Hyperandrogenism (hirsutism and/or hyperandrogenaemia) [$\atoma$], [and] ovarian dysfunction (oligoanovulation [$\atoma$] and/or polycystic ovaries [$\atomc$]), and exclusion of other androgen excess related disorders [$\atomy$]']
        ], max_width=7).move_to(ORIGIN).shift(UP*1.5)

        citation = TexWrapper(
            r"\text{Table from H. Teede, A. Deeks, and L. Moran. \textit{Polycystic ovary syndrome: a complex condition with psychological, reproductive and metabolic manifestations that impacts on health across the lifespan}. BMC Medicine, 2010.}",
            font_size=12,
        ).next_to(table, DOWN, buff=0.075)
        

        # Create argumentation graph (from s_aba_motivation)
        RADIUS = 0.25
        STROKE_WIDTH = 1
        HOR_DIST = 1
        PROP_COLOR = ["#E8FFE8", "#B5FFB5"]
        OPPONENT_COLOR = ["#FFFBE8", "#FFF1B5"]
        DEFEAT_COLOR = ["#FFE8E8", "#FFB5B5"]
        SIBLING_DIST_RATIO = 1

        graph_center = ORIGIN

        p_node = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\atomp")).set_z_index(99).move_to(graph_center)
        p_node_1 = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\atomp")).set_z_index(99).next_to(p_node, LEFT, buff=HOR_DIST).shift(UP*2)
        p_node_2 = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\atomp")).set_z_index(99).next_to(p_node, LEFT, buff=HOR_DIST).shift(DOWN*2)

        a_node_1 = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\atoma")).set_z_index(99).next_to(p_node_1, LEFT, buff=HOR_DIST).shift(UP*SIBLING_DIST_RATIO)
        b_node_1 = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\atomb")).set_z_index(99).next_to(p_node_1, LEFT, buff=HOR_DIST)
        x_node_1 = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper(r"\atomx")).set_z_index(99).next_to(p_node_1, LEFT, buff=HOR_DIST).shift(DOWN*SIBLING_DIST_RATIO)

        neg_x_node = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\neg \atomx")).set_z_index(99).next_to(x_node_1, LEFT, buff=HOR_DIST*2.5)
        x_p_node = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\atomx'")).set_z_index(99).next_to(neg_x_node, LEFT, buff=HOR_DIST)
        empty_x_p = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(x_p_node, LEFT, buff=HOR_DIST)

        empty_a_1 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(a_node_1, LEFT, buff=HOR_DIST)
        empty_b_1 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(b_node_1, LEFT, buff=HOR_DIST)

        a_node_2 = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\atoma")).set_z_index(99).next_to(p_node_2, LEFT, buff=HOR_DIST).shift(UP*SIBLING_DIST_RATIO)
        b_node_2 = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\atomb")).set_z_index(99).next_to(p_node_2, LEFT, buff=HOR_DIST)
        y_node_2 = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper(r"\atomy")).set_z_index(99).next_to(p_node_2, LEFT, buff=HOR_DIST).shift(DOWN*SIBLING_DIST_RATIO)

        neg_y_node = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\neg \atomy")).set_z_index(99).next_to(y_node_2, LEFT, buff=HOR_DIST*2.5)
        y_p_node = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper(r"\atomy'")).set_z_index(99).next_to(neg_y_node, LEFT, buff=HOR_DIST)
        empty_y_p = Circle(radius=RADIUS, color=BLACK, stroke_width=0).set_z_index(99).next_to(y_p_node, LEFT, buff=HOR_DIST)

        empty_a_2 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(a_node_2, LEFT, buff=HOR_DIST)
        empty_b_2 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(b_node_2, LEFT, buff=HOR_DIST)

        # Highlight boxes
        p1_arg_box = highlight_box(VGroup(p_node_1, a_node_1, b_node_1, x_node_1), fill_opacity=1, fill_color=DEFEAT_COLOR, buff=0.2, dashed=True).set_z_index(3)
        a1_arg_box = highlight_box(VGroup(a_node_1, empty_a_1), fill_opacity=1, fill_color=DEFEAT_COLOR, buff=0.1, dashed=False).set_z_index(4)
        b1_arg_box = highlight_box(VGroup(b_node_1, empty_b_1), fill_opacity=1, fill_color=DEFEAT_COLOR, buff=0.1, dashed=False).set_z_index(4)
        p1_arg_box_full = highlight_box(VGroup(p1_arg_box, a1_arg_box), fill_opacity=1, fill_color=DEFEAT_COLOR, buff=0.12, dashed=False).set_z_index(0)

        neg_x1_rule_box = highlight_box(VGroup(neg_x_node, x_p_node), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.2, dashed=True).set_z_index(1)
        x_p_rule_box = highlight_box(VGroup(x_p_node, empty_x_p), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(2)
        neg_x1_box_full = highlight_box(VGroup(neg_x1_rule_box, x_p_rule_box), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(0)

        p2_arg_box = highlight_box(VGroup(p_node_2, a_node_2, b_node_2, y_node_2), fill_opacity=1, fill_color=PROP_COLOR, buff=0.2, dashed=True).set_z_index(3)
        a2_arg_box = highlight_box(VGroup(a_node_2, empty_a_2), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=False).set_z_index(4)
        b2_arg_box = highlight_box(VGroup(b_node_2, empty_b_2), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=False).set_z_index(4)
        p2_arg_box_full = highlight_box(VGroup(p2_arg_box, a2_arg_box), fill_opacity=1, fill_color=PROP_COLOR, buff=0.12, dashed=False).set_z_index(0)

        neg_y2_rule_box = highlight_box(VGroup(neg_y_node, y_p_node), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.2, dashed=True).set_z_index(1)

        # Edges
        edge_p1_to_p = fixed_arrow_graph(p_node_1, p_node.get_left()+UP*0.1, color=BLACK)
        edge_a1_to_p1 = fixed_arrow_graph(a_node_1, p_node_1.get_left()+UP*0.1, color=BLACK)
        edge_b1_to_p1 = fixed_arrow_graph(b_node_1, p_node_1.get_left(), color=BLACK)
        edge_x1_to_p1 = fixed_arrow_graph(x_node_1, p_node_1.get_left()+DOWN*0.1, color=BLACK)
        edge_empty_a1 = fixed_arrow_graph(empty_a_1, a_node_1.get_left(), color=BLACK)
        edge_empty_b1 = fixed_arrow_graph(empty_b_1, b_node_1.get_left(), color=BLACK)
        edge_neg_x_attack = fixed_arrow_graph(neg_x_node, x_node_1.get_left(), color=RED)
        edge_xp_to_negx = fixed_arrow_graph(x_p_node, neg_x_node.get_left()+LEFT*0.2, color=BLACK)
        edge_empty_xp = fixed_arrow_graph(empty_x_p, x_p_node.get_left(), color=BLACK)

        edge_p2_to_p = fixed_arrow_graph(p_node_2, p_node.get_left()+DOWN*0.1, color=BLACK)
        edge_a2_to_p2 = fixed_arrow_graph(a_node_2, p_node_2.get_left()+UP*0.1, color=BLACK)
        edge_b2_to_p2 = fixed_arrow_graph(b_node_2, p_node_2.get_left(), color=BLACK)
        edge_y2_to_p2 = fixed_arrow_graph(y_node_2, p_node_2.get_left()+DOWN*0.1, color=BLACK)
        edge_empty_a2 = fixed_arrow_graph(empty_a_2, a_node_2.get_left(), color=BLACK)
        edge_empty_b2 = fixed_arrow_graph(empty_b_2, b_node_2.get_left(), color=BLACK)
        edge_neg_y_attack = fixed_arrow_graph(neg_y_node, y_node_2.get_left(), color=RED)
        edge_yp_to_negy = fixed_arrow_graph(y_p_node, neg_y_node.get_left()+LEFT*0.2, color=BLACK)

        # Group all graph elements
        graph_elements = VGroup(
            p_node, p_node_1, p_node_2, a_node_1, b_node_1, x_node_1,
            a_node_2, b_node_2, y_node_2,
            empty_a_1, empty_b_1, empty_a_2, empty_b_2,
            neg_x_node, neg_y_node, x_p_node, y_p_node, empty_x_p, empty_y_p,
            p1_arg_box, a1_arg_box, b1_arg_box, p1_arg_box_full,
            neg_x1_rule_box, x_p_rule_box, neg_x1_box_full,
            p2_arg_box, a2_arg_box, b2_arg_box, p2_arg_box_full,
            neg_y2_rule_box,
            edge_p1_to_p, edge_a1_to_p1, edge_b1_to_p1, edge_x1_to_p1,
            edge_empty_a1, edge_empty_b1, edge_neg_x_attack, edge_xp_to_negx, edge_empty_xp,
            edge_p2_to_p, edge_a2_to_p2, edge_b2_to_p2, edge_y2_to_p2,
            edge_empty_a2, edge_empty_b2, edge_neg_y_attack, edge_yp_to_negy
        )
        graph_elements.scale(0.45).next_to(table, DOWN, buff=.5, aligned_edge=LEFT).shift(RIGHT)

        s.play(FadeOut(quote_lines), FadeOut(
            VGroup(cross_line, other, oligo, hyper, brace, pcos)),
            FadeIn(VGroup(table, citation)))
        
        s.wait()
        s.next_slide()

        s.play(FadeIn(graph_elements))

        s.wait()
        s.next_slide()

        # ----------
        defaults_font_size = 20
        formula_1_s = MathTexWrapper(r'\standb{\snih}\Bigg[', r'\default{\atoma\land\atomb}{\atomx}{\atomp}', r'\Bigg]', font_size=defaults_font_size).to_edge(RIGHT).shift(LEFT*4+DOWN*.5)
        formula_2_s = MathTexWrapper(r'\standb{\srot}\Bigg[', r'\default{(\atoma\land\atomb)\lor(\atoma\land\atomc)\lor(\atomb\land\atomc)}{\atomx}{\atomp}', r'\Bigg]', font_size=defaults_font_size).next_to(formula_1_s, DOWN, aligned_edge=LEFT)
        formula_3_s = MathTexWrapper(r'\standb{\saes}\Bigg[', r'\default{\atoma\land(\atomb\lor\atomc)}{\atomy}{\atomp}', r'\Bigg]', font_size=defaults_font_size).next_to(formula_2_s, DOWN, aligned_edge=LEFT)
        a_c = MathTexWrapper(r'\atoma\land\atomc', font_size=defaults_font_size).next_to(formula_3_s, DOWN, aligned_edge=LEFT)
        neg_y = MathTexWrapper(r'\neg\atomy', font_size=defaults_font_size).next_to(a_c, DOWN, aligned_edge=LEFT)

        group_1 = VGroup(formula_1_s, formula_2_s, formula_3_s, a_c)

        s.add(formula_1_s, formula_2_s, formula_3_s, a_c)

        brace_5 = Brace(group_1, direction=RIGHT, buff=0.2, color=BLACK)
        brace_5_conclusion = MathTexWrapper(r'\models', r'\big\{', r'\standb{\srot}\atomp,', r'\standb{\saes}\atomp',   r'\big\}', font_size=defaults_font_size)
        brace_6_conclusion = brace_5_conclusion.copy()
        brace_5.put_at_tip(brace_5_conclusion)
        s.wait()
        s.next_slide()
        s.play(GrowFromCenter(brace_5))
        s.wait()
        s.next_slide()
        s.play(FadeIn(brace_5_conclusion))

        group_1.add(neg_y)
        brace_6 = Brace(group_1, direction=RIGHT, buff=0.2, color=BLACK)
        brace_6.put_at_tip(brace_6_conclusion)
        s.wait()
        s.next_slide()
        s.play(
            FadeIn(neg_y),
            Transform(brace_5, brace_6),
            Transform(brace_5_conclusion, brace_6_conclusion)
        )

        saes_cross = Cross(brace_5_conclusion[3], color=RED, stroke_width=3).scale(1.05)
        s.wait()
        s.next_slide()
        s.play(FadeIn(saes_cross))


class SMotivationScene(Slide):
    def construct(self):
        SMotivation(self, show_footer=True,
                    slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
