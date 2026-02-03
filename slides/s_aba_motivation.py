from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.graphs import fixed_arrow_graph, curved_arrow
from slides.shared.common import highlight_box

from slides.shared.slide_count import SLIDES, SLIDES_NO

SLIDE_NO = 1


class SAbaMotivation(BaseSlide):
    TITLE = r'(Structured) Argumentation Games'

    def create_content(self):
        s = self.slide

        # Chat colors (matching graph colors with gradient)
        LEFT_COLOR = ["#E8FFE8", "#B5FFB5"]   # Proponent green (matching PROP_COLOR)
        RIGHT_COLOR = ["#FFFBE8", "#FFF1B5"]  # Opponent yellow (matching OPPONENT_COLOR)

        # Chat area width
        chat_width = 3.8

        # Message bubbles
        def make_bubble(text, width, align_left=True):
            colors = LEFT_COLOR if align_left else RIGHT_COLOR
            bubble = RoundedRectangle(
                width=width, height=0.5,
                corner_radius=0.15,
                stroke_width=1, stroke_color=GREY
            )
            bubble.set_fill(color=colors, opacity=1)
            bubble.set_sheen_direction(DOWN)
            label = TexWrapper(text, font_size=20, color=BLACK)
            label.move_to(bubble)
            group = VGroup(bubble, label)
            group.align_left = align_left
            return group
        
        

        # Create messages
        msg1 = make_bubble("Conclude $P$, if $A$, $B$ and assuming $X$.", 3.8, align_left=True)
        msg2 = make_bubble("$A$ is true.", 1, align_left=True)
        msg3 = make_bubble("$B$ is true.", 1, align_left=True)
        msg4 = make_bubble(r"Conclude $\overline{X}$ if $X'$.", 2, align_left=False)
        msg5 = make_bubble("$X'$ is true.", 1.1, align_left=False)
        msg6 = make_bubble(r"Conclude $P$, if $A$, $B$ and assuming $Y$.", 3.8, align_left=True)
        msg7 = make_bubble(r"Conclude $\overline{Y}$ if $Y'$", 2, align_left=False)
        msg8 = make_bubble("...", .5, align_left=False)
        # msg1 = make_bubble("Hey, how are you?", 2.2, align_left=True)
        # msg1 = make_bubble("Hey, how are you?", 2.2, align_left=True)
        # msg2 = make_bubble("I'm good, thanks!", 2.0, align_left=False)
        # msg3 = make_bubble("What are you up to?", 2.3, align_left=True)
        # msg4 = make_bubble("Working on slides", 2.1, align_left=False)
        # msg5 = make_bubble("Nice!", 1.0, align_left=True)
        # msg6 = make_bubble("Yeah it's fun", 1.8, align_left=False)

        # messages = VGroup(msg1, msg2, msg3, msg4, msg5, msg6)
        messages = VGroup(msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8)
        messages.arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        # Align each message left or right
        chat_left = -chat_width / 2
        chat_right = chat_width / 2

        for msg in messages:
            if msg.align_left:
                msg.move_to([chat_left + msg.width / 2, msg.get_center()[1], 0])
            else:
                msg.move_to([chat_right - msg.width / 2, msg.get_center()[1], 0])

        # Move entire chat to the left
        messages.shift(LEFT * 4 + DOWN*.25)


        # Create a rectangular box around the messages
        chat_box = Rectangle(
            width=messages.get_width() + 0.4,
            height=messages.get_height() + 0.4,
            color=BLACK,
            stroke_width=2,
            fill_opacity=0
        )
        chat_box.move_to(messages)
        s.add(chat_box)

        # Helper function for message animation
        def show_msg(msg):
            direction = LEFT if msg.align_left else RIGHT
            s.play(FadeIn(msg, shift=direction * 0.5), msg.animate.scale(1.05), run_time=0.3)
            s.play(msg.animate.scale(1/1.05), run_time=0.15)
            s.wait(0.1)
            s.next_slide()





        ##############
        # Graph part #
        ##############

        # Draw dispute graph on the right side
        RADIUS = 0.25
        STROKE_WIDTH = 1
        HOR_DIST = 1
        PROP_COLOR = ["#E8FFE8", "#B5FFB5"]
        OPPONENT_COLOR = ["#FFFBE8", "#FFF1B5"]
        DEFEAT_COLOR = ["#FFE8E8", "#FFB5B5"]

        SIBLING_DIST_RATIO = 1

        # Position graph on right side
        graph_center = RIGHT * 3.5 + DOWN * 0.5

        p_node = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("P")).set_z_index(99).move_to(graph_center)

        p_node_1 = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("P")).set_z_index(99).next_to(p_node, LEFT, buff=HOR_DIST).shift(UP*2)

        p_node_2 = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("P")).set_z_index(99).move_to(graph_center).next_to(p_node, LEFT, buff=HOR_DIST).shift(DOWN*2)
        
        a_node_1 = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper("A")).set_z_index(99).next_to(p_node_1, LEFT, buff=HOR_DIST).shift(UP*SIBLING_DIST_RATIO)
        b_node_1 = Circle(radius=RADIUS, color=BLACK,  stroke_opacity=0).add(MathTexWrapper("B")).set_z_index(99).next_to(p_node_1, LEFT, buff=HOR_DIST)
        x_node_1 = Circle(radius=RADIUS, color=BLACK,  stroke_width=STROKE_WIDTH).add(MathTexWrapper("X")).set_z_index(99).next_to(p_node_1, LEFT, buff=HOR_DIST).shift(DOWN*SIBLING_DIST_RATIO)

        neg_x_node = Circle(radius=RADIUS, color=BLACK,  stroke_opacity=0).add(MathTexWrapper(r"\overline{X}")).set_z_index(99).next_to(x_node_1, LEFT, buff=HOR_DIST*2.5)

        x_p_node = Circle(radius=RADIUS, color=BLACK,  stroke_opacity=0).add(MathTexWrapper(r"X'")).set_z_index(99).next_to(neg_x_node, LEFT, buff=HOR_DIST)

        empty_x_p = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(x_p_node, LEFT, buff=HOR_DIST)





        # Checkmark nodes to the left of A and B (first argument)
        empty_a_1 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(a_node_1, LEFT, buff=HOR_DIST)
        empty_b_1 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(b_node_1, LEFT, buff=HOR_DIST)

        a_node_2 = Circle(radius=RADIUS, color=BLACK, stroke_opacity=0).add(MathTexWrapper("A")).set_z_index(99).next_to(p_node_2, LEFT, buff=HOR_DIST).shift(UP*SIBLING_DIST_RATIO)
        b_node_2 = Circle(radius=RADIUS, color=BLACK,  stroke_opacity=0).add(MathTexWrapper("B")).set_z_index(99).next_to(p_node_2, LEFT, buff=HOR_DIST)
        y_node_2 = Circle(radius=RADIUS, color=BLACK,  stroke_width=STROKE_WIDTH).add(MathTexWrapper("Y")).set_z_index(99).next_to(p_node_2, LEFT, buff=HOR_DIST).shift(DOWN*SIBLING_DIST_RATIO)

        neg_y_node = Circle(radius=RADIUS, color=BLACK,  stroke_opacity=0).add(MathTexWrapper(r"\overline{Y}")).set_z_index(99).next_to(y_node_2, LEFT, buff=HOR_DIST*2.5)

        y_p_node = Circle(radius=RADIUS, color=BLACK,  stroke_opacity=0).add(MathTexWrapper(r"Y'")).set_z_index(99).next_to(neg_y_node, LEFT, buff=HOR_DIST)

        empty_y_p = Circle(radius=RADIUS, color=BLACK, stroke_width=0).set_z_index(99).next_to(y_p_node, LEFT, buff=HOR_DIST)

        # Empty nodes to the left of A and B (second argument)
        empty_a_2 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(a_node_2, LEFT, buff=HOR_DIST)
        empty_b_2 = Circle(radius=RADIUS, color=BLACK, stroke_width=0).add(MathTexWrapper(r"\checkmark")).set_z_index(99).next_to(b_node_2, LEFT, buff=HOR_DIST)
        
        # s_node = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("s")).set_z_index(99).move_to(graph_center)

        # d = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("d")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST).shift(UP)
        # p = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("p")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST)
        # a = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("a")).set_z_index(99).next_to(s_node, LEFT, buff=HOR_DIST).shift(DOWN)
        # xc = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\bar{c}")).set_z_index(99).next_to(p, LEFT, buff=HOR_DIST)
        # f = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("f")).set_z_index(99).next_to(xc, LEFT, buff=HOR_DIST)
        # xd = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\bar{d}")).set_z_index(99).next_to(f, LEFT, buff=1.5*HOR_DIST).shift(UP)
        # e = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("e")).set_z_index(99).next_to(xd, LEFT, buff=HOR_DIST)
        # xa = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper(r"\bar{a}")).set_z_index(99).next_to(f, LEFT, buff=1.5*HOR_DIST).shift(DOWN)
        # b = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("b")).set_z_index(99).next_to(xa, LEFT, buff=HOR_DIST).shift(.5*UP)
        # t = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0).add(MathTexWrapper("t")).set_z_index(99).next_to(xa, LEFT, buff=HOR_DIST).shift(.5*DOWN)
        # c = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH).add(MathTexWrapper("c")).set_z_index(99).next_to(t, LEFT, buff=HOR_DIST)
        # xe = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH, fill_color=PROP_COLOR, fill_opacity=1).add(MathTexWrapper(r"\bar{e}")).set_z_index(99).next_to(e, LEFT, buff=HOR_DIST)

        # # Create argument boxes (highlight rectangles)
        # # Proponent argument: s with d, p, a
        # s_arg_box = highlight_box(VGroup(s_node, d, p, a), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=True).set_z_index(3)
        p1_arg_box = highlight_box(VGroup(p_node_1, a_node_1, b_node_1, x_node_1), fill_opacity=1, fill_color=PROP_COLOR, buff=0.2, dashed=True).set_z_index(3)

        a1_arg_box = highlight_box(VGroup(a_node_1, empty_a_1), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=False).set_z_index(4)

        b1_arg_box = highlight_box(VGroup(b_node_1, empty_b_1), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=False).set_z_index(4)

        p1_arg_box_full = highlight_box(VGroup(p1_arg_box, a1_arg_box), fill_opacity=1, fill_color=PROP_COLOR, buff=0.12, dashed=False).set_z_index(0)

        neg_x1_rule_box = highlight_box(VGroup(neg_x_node, x_p_node), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.2, dashed=True).set_z_index(1)

        x_p_rule_box = highlight_box(VGroup(x_p_node, empty_x_p), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(2)

        neg_x1_box_full = highlight_box(VGroup(neg_x1_rule_box, x_p_rule_box), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(0)

        # 

        p2_arg_box = highlight_box(VGroup(p_node_2, a_node_2, b_node_2, y_node_2), fill_opacity=1, fill_color=PROP_COLOR, buff=0.2, dashed=True).set_z_index(3)

        a2_arg_box = highlight_box(VGroup(a_node_2, empty_a_2), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=False).set_z_index(4)

        b2_arg_box = highlight_box(VGroup(b_node_2, empty_b_2), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=False).set_z_index(4)

        p2_arg_box_full = highlight_box(VGroup(p2_arg_box, a2_arg_box), fill_opacity=1, fill_color=PROP_COLOR, buff=0.12, dashed=False).set_z_index(0)

        neg_y2_rule_box = highlight_box(VGroup(neg_y_node, y_p_node), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.2, dashed=True).set_z_index(1)

        y_p_rule_box = highlight_box(VGroup(y_p_node, empty_y_p), fill_opacity=1, fill_color=OPPONENT_COLOR, buff=0.1, dashed=False).set_z_index(2)

        # # Opponent argument: e -> xd (defeated)
        # e_xd_box = highlight_box(VGroup(e, xd), fill_opacity=1, fill_color=DEFEAT_COLOR, buff=0.1, dashed=False).set_z_index(0)

        # # Opponent argument: t, b -> xa (defeated)
        # t_b_xa_box = highlight_box(VGroup(t, b, xa), stroke_width=STROKE_WIDTH, fill_opacity=1, fill_color=DEFEAT_COLOR, dashed=True, buff=0.15).set_z_index(0)

        # # Opponent argument: c -> t (defeated)
        # c_t_box = highlight_box(VGroup(c, t), stroke_width=STROKE_WIDTH, fill_opacity=1, fill_color=DEFEAT_COLOR, dashed=True, buff=0.1).set_z_index(5)

        # # Proponent: xc -> p
        # xc_p_box = highlight_box(VGroup(xc, p), fill_opacity=1, fill_color=PROP_COLOR, buff=0.15, dashed=True).set_z_index(4)

        # # Proponent: f -> xc
        # f_xc_box = highlight_box(VGroup(f, xc), fill_opacity=1, fill_color=PROP_COLOR, buff=0.1, dashed=True).set_z_index(5)

        # # Main proponent argument box
        # main_prop_box = highlight_box(VGroup(f, s_node, d, a), fill_opacity=1, fill_color=PROP_COLOR, buff=0.3, dashed=False).set_z_index(0)

        # Create edges
        edges = VGroup(
            fixed_arrow_graph(p_node_1, p_node.get_left()+UP*0.1, color=BLACK),
            fixed_arrow_graph(p_node_2, p_node.get_left()+DOWN*0.1, color=BLACK),
            fixed_arrow_graph(a_node_1, p_node_1.get_left()+UP*0.1, color=BLACK),
            fixed_arrow_graph(empty_a_1, a_node_1.get_left(), color=BLACK),
            fixed_arrow_graph(b_node_1, p_node_1.get_left(), color=BLACK),
            fixed_arrow_graph(empty_b_1, b_node_1.get_left(), color=BLACK),
            fixed_arrow_graph(x_node_1, p_node_1.get_left()+DOWN*0.1, color=BLACK),
            fixed_arrow_graph(a_node_2, p_node_2.get_left()+UP*0.1, color=BLACK),
            fixed_arrow_graph(empty_a_2, a_node_2.get_left()+UP*0.0, color=BLACK),
            fixed_arrow_graph(empty_b_2, b_node_2.get_left()+UP*0.0, color=BLACK),
            fixed_arrow_graph(b_node_2, p_node_2.get_left(), color=BLACK),
            fixed_arrow_graph(y_node_2, p_node_2.get_left()+DOWN*0.1, color=BLACK),
            fixed_arrow_graph(neg_y_node, y_node_2.get_left()+DOWN*0.0, color=RED),
            fixed_arrow_graph(neg_x_node, x_node_1.get_left()+DOWN*0.0, color=RED),
            fixed_arrow_graph(y_p_node, neg_y_node.get_left()+DOWN*0.0+LEFT*0.2, color=BLACK),
            fixed_arrow_graph(x_p_node, neg_x_node.get_left()+DOWN*0.0+LEFT*0.2, color=BLACK),
            fixed_arrow_graph(empty_x_p, x_p_node.get_left()+DOWN*0.0, color=BLACK),
            # fixed_arrow_graph(a, s_node.get_left()+DOWN*0.1, color=BLACK),
            # fixed_arrow_graph(p, s_node.get_left(), color=BLACK),
            # fixed_arrow_graph(e, xd.get_left(), color=BLACK),
            # fixed_arrow_graph(xd, d.get_left(), color=RED),
            # fixed_arrow_graph(b, xa.get_left()+UP*0.1, color=BLACK),
            # fixed_arrow_graph(t, xa.get_left()+DOWN*0.1, color=BLACK),
            # fixed_arrow_graph(xa, a.get_left(), color=RED),
            # fixed_arrow_graph(c, t.get_left(), color=BLACK),
            # fixed_arrow_graph(xe, e.get_left(), color=RED),
            # fixed_arrow_graph(xc, p.get_left(), color=BLACK),
            # curved_arrow(xc.get_bottom(), c.get_right()+0.1*DOWN+0.2*RIGHT, bend=1, color=RED),
            # fixed_arrow_graph(f, xc.get_left(), color=BLACK),
        )
        


        # Scale factor for positioning
        SCALE = 0.8
        GRAPH_POS = RIGHT * 6.5 + DOWN * 0.25

        # Helper to scale and position a group
        def prep(group):
            return group.scale(SCALE).move_to(GRAPH_POS, aligned_edge=RIGHT)

        # Create edges as needed (will be created inline during animation)
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

        # Group everything for scaling
        all_elements = VGroup(
            p_node, 
            p_node_1, p_node_2, a_node_1, b_node_1, x_node_1,
            a_node_2, b_node_2, y_node_2,
            empty_a_1, empty_b_1, empty_a_2, empty_b_2,
            neg_x_node, neg_y_node, x_p_node, y_p_node, empty_x_p, empty_y_p,
            p1_arg_box, a1_arg_box, b1_arg_box, p1_arg_box_full,
            neg_x1_rule_box, x_p_rule_box, neg_x1_box_full,
            p2_arg_box, a2_arg_box, b2_arg_box, p2_arg_box_full,
            neg_y2_rule_box, y_p_rule_box,
            edge_p1_to_p, edge_a1_to_p1, edge_b1_to_p1, edge_x1_to_p1,
            edge_empty_a1, edge_empty_b1, edge_neg_x_attack, edge_xp_to_negx, edge_empty_xp,
            edge_p2_to_p, edge_a2_to_p2, edge_b2_to_p2, edge_y2_to_p2,
            edge_empty_a2, edge_empty_b2, edge_neg_y_attack, edge_yp_to_negy
        )
        all_elements.scale(SCALE).move_to(GRAPH_POS, aligned_edge=RIGHT)

        # --- Gradual graph drawing ---

                # Show messages explicitly
        show_msg(msg1)


        # Step 1: Show first argument (P <- A, B, X) with rule box
        s.play(Create(VGroup(p_node, p1_arg_box, p_node_1, a_node_1, b_node_1,  x_node_1,
                             edge_a1_to_p1, edge_b1_to_p1, edge_x1_to_p1, edge_p1_to_p)))
        s.next_slide()

        # Step 2: Show A supported by checkmark
        show_msg(msg2)
        s.play(Create(VGroup(a1_arg_box, empty_a_1, edge_empty_a1)))
        s.next_slide()


        show_msg(msg3)
        s.play(Create(VGroup(b1_arg_box, empty_b_1, edge_empty_b1)))
        s.play(DrawBorderThenFill(p1_arg_box_full))
        s.next_slide()



        show_msg(msg4)
        s.play(Create(VGroup(neg_x1_rule_box, neg_x_node, x_p_node, edge_xp_to_negx, edge_neg_x_attack)))
        s.next_slide()

        show_msg(msg5)
        s.play(Create(VGroup(x_p_rule_box, empty_x_p, edge_empty_xp)))
        # Change first argument boxes to defeated (red)
        s.play(
            DrawBorderThenFill(neg_x1_box_full),
            p1_arg_box[0].animate.set_fill(DEFEAT_COLOR, opacity=1),
            p1_arg_box_full[0].animate.set_fill(DEFEAT_COLOR, opacity=1),
            a1_arg_box[0].animate.set_fill(DEFEAT_COLOR, opacity=1),
            b1_arg_box[0].animate.set_fill(DEFEAT_COLOR, opacity=1),
        )
        s.next_slide()

        show_msg(msg6)


        s.play(Create(VGroup(p2_arg_box, p_node_2, a_node_2, b_node_2, y_node_2,
                             edge_a2_to_p2, edge_b2_to_p2, edge_y2_to_p2, a2_arg_box, empty_a_2, edge_empty_a2, b2_arg_box, empty_b_2, edge_empty_b2, p2_arg_box_full, edge_p2_to_p)))

        show_msg(msg7)



        s.play(Create(VGroup(neg_y2_rule_box, neg_y_node, y_p_node, edge_yp_to_negy, edge_neg_y_attack)))
        s.next_slide()
        show_msg(msg8)




class SAbaMotivationScene(Slide):
    def construct(self):
        SAbaMotivation(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
