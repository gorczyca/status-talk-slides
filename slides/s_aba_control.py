from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TextWrapper
from slides.shared.colors import D_BLUE, LAT_ORANGE
from slides.shared.block_diagram import BlockDiagram
from slides.shared.file_icon import FileIcon
from slides.shared.asp_lexer import set_asp_lexer

from slides.shared.slide_count import SLIDES, SLIDES_NO

set_asp_lexer()

SLIDE_NO = 6

WIDTH = 13
BUFF=1.5

# Node colors
NODE_DEFAULT = WHITE
NODE_GREEN = "#4CAF50"  # Material green
NODE_RED = "#F44336"    # Material red



class SAbaControl(BaseSlide):
    TITLE = r'Multi-Shot ASP: Dynamic Solving \& Grounding'

    def create_content(self):
        s = self.slide


        
        # Tree structure:
        #            root
        #          /  |  \
        #         A   B   C
        #            / \  / \
        #           D  E F  G
        #              |   / \
        #              H  I   J

        node_radius = 0.25

        def make_node(pos, color=NODE_DEFAULT):
            return Circle(
                radius=node_radius,
                color=BLACK,
                fill_opacity=1,
                fill_color=color,
                stroke_width=3
            ).move_to(pos)

        def make_edge(n1, n2):
            return Line(n1.get_bottom(), n2.get_top(), color=BLACK, stroke_width=2)

        # Level positions (y-coordinates)
        level_y = [2, 1, 0, -1]

        # Level 0 - root
        root = make_node(UP * level_y[0])

        # Level 1 - three children (example: mark node_a as green)
        node_a = make_node(UP * level_y[1] + LEFT * 2, color=NODE_RED)
        node_b = make_node(UP * level_y[1], color=NODE_DEFAULT)
        node_c = make_node(UP * level_y[1] + RIGHT * 2, color=NODE_DEFAULT)

        # Level 2 - B and C each have 2 children
        node_d = make_node(DOWN * 0 + LEFT * 0.6, color=NODE_DEFAULT)
        node_e = make_node(DOWN * 0 + RIGHT * 0.6, color=NODE_GREEN)
        node_f = make_node(DOWN * 0 + RIGHT * 1.4 + RIGHT * 0.6, color=NODE_RED)
        # node_g = make_node(DOWN * 0 + RIGHT * 2.6 + RIGHT * 0.6, color=NODE_DEFAULT)

        # Level 3 - E has 1 child, F has 2 children
        node_h = make_node(DOWN * 1 + LEFT * 1.2, color=NODE_RED)
        node_i = make_node(DOWN * 1, color=NODE_RED)
        # node_j = make_node(DOWN * 1 + RIGHT * 2.6, color=NODE_DEFAULT)

        # Group nodes by level
        level_0 = VGroup(root)
        level_1 = VGroup(node_a, node_b, node_c)
        level_2 = VGroup(node_d, node_e, node_f)
        # level_2 = VGroup(node_d, node_e, node_f, node_g)
        level_3 = VGroup(node_h, node_i)
        # level_3 = VGroup(node_h, node_i, node_j)
        # levels = [level_0, level_1, level_2, level_3]
        levels = [level_0, level_1, level_2, level_3]

        nodes = VGroup(root, node_a, node_b, node_c, node_d, node_e, node_f, node_h, node_i)

        edges = VGroup(
            make_edge(root, node_a),
            make_edge(root, node_b),
            make_edge(root, node_c),
            make_edge(node_b, node_d),
            make_edge(node_b, node_e),
            make_edge(node_c, node_f),
            make_edge(node_d, node_h),
            make_edge(node_d, node_i),
            # make_edge(node_c, node_g),
            # make_edge(node_e, node_h),
            # make_edge(node_f, node_i),
            # make_edge(node_f, node_j),
        )

        tree = VGroup(edges, nodes).move_to(ORIGIN)

        # Create time labels (t=0, t=1, etc.) positioned to the left
        time_labels = VGroup()
        tree_left = tree.get_left()[0]  # x-coordinate of left edge

        for i, level in enumerate(levels):
            label = MathTex(f"t={i}", color=BLACK, font_size=36)
            # Position label to the left of the tree, aligned with this level's y
            level_center_y = level.get_center()[1]
            label.move_to(np.array([tree_left - 0.8, level_center_y, 0]))
            time_labels.add(label)

        # Create level selection rectangles (initially invisible)
        level_rects = VGroup()
        for i, level in enumerate(levels):
            level_center_y = level.get_center()[1]
            rect = Rectangle(
                width=tree.get_width() + 1.6,  # Include time label area
                height=node_radius * 2 + 0.3,
                color=D_BLUE,
                stroke_width=3,
                fill_opacity=0,  # Empty inside
            )
            rect.move_to(np.array([tree.get_center()[0] - 0.7, level_center_y, 0]))
            rect.set_stroke(opacity=0)  # Start invisible (stroke only)
            level_rects.add(rect)

        # Group everything and shift right
        tree_group = VGroup(tree, time_labels, level_rects)
        tree_group.scale(0.7).shift(RIGHT * 4 + DOWN * 1.2)
        s.add(tree_group)

        # Add ASP code listing above the tree
        CODE_BG = {"fill_color": "#F5F5F5", "stroke_color": "#CCCCCC", "stroke_width": 1}

        asp_code = Code(
            tab_width=2,
            code_string='''
pWin(t) :- termination(t), not possibleMove(t,o,_).
oWin(t) :- not termination(t), not possibleMove(t,p,_).
''',
            language='asp',
            formatter_style='default',
            add_line_numbers=False,
            background_config=CODE_BG,
        ).scale(0.6)
        asp_code.next_to(tree_group, UP, buff=1.2).shift(LEFT*0.75)
        s.add(asp_code)

        # Add block diagram on the left
        diagram = BlockDiagram()
        diagram.to_edge(LEFT, buff=1.5).shift(UP*3)
        s.add(diagram)
        self.diagram = diagram


        # Prepare diagram highlights (all start hidden)
        diagram.create_highlights()
        self.diagram_highlights = diagram.highlights
        self._current_diagram_highlight = None

        # Store references for animation access
        self.tree_group = tree_group
        self.tree = tree
        self.nodes = nodes
        self.levels = levels
        self.time_labels = time_labels
        self.level_rects = level_rects
    

        # Example: Animate highlighting levels one by one
        # Uncomment to enable step-by-step level highlighting
        # for i, rect in enumerate(level_rects):
        #     s.next_slide()
        #     s.play(rect.animate.set_opacity(1), run_time=0.5)

        # Demo: highlight diagram blocks and tree levels

        s.wait()
        s.next_slide()
        self.highlight_level(0)
        self.highlight_diagram("first")
        s.wait()
        s.next_slide()
        self.highlight_diagram("second")
        s.next_slide()
        s.wait()
        self.highlight_diagram("third")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fourth")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fifth")
        s.next_slide()
        s.wait()
        self.highlight_level(1)
        s.wait()
        s.next_slide()

        self.highlight_diagram("second")
        s.next_slide()
        s.wait()
        self.highlight_diagram("third")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fourth")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fifth")
        s.next_slide()
        s.wait()
        self.highlight_level(2)
        s.wait()
        s.next_slide()


        self.highlight_diagram("second")
        s.next_slide()
        s.wait()
        self.highlight_diagram("third")
        s.next_slide()
        s.wait()
        self.highlight_diagram("third_yes")
        s.next_slide()
        s.wait()

        self.highlight_diagram(None)  # Hide all
        self.highlight_level(-1)  # Hide all
        s.next_slide()
        s.wait()

        s.play(node_e.animate.scale(1.3).set_fill(NODE_RED), run_time=0.3)
        s.play(node_e.animate.scale(1/1.3), run_time=0.3)

        s.next_slide()
        s.wait()

        self.highlight_level(2)  # Hide all
        self.highlight_diagram("third")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fourth")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fifth")
        s.next_slide()
        s.wait()
        self.highlight_level(3)
        s.wait()
        s.next_slide()


        self.highlight_diagram("second")
        s.next_slide()
        s.wait()
        self.highlight_diagram("third")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fourth")
        s.next_slide()
        s.wait()
        self.highlight_diagram("fourth_yes")
        s.next_slide()
        s.wait()








    def highlight_level(self, level_idx, opacity=1):
        """Set a level's highlight rectangle visibility, hiding all others."""
        for i, rect in enumerate(self.level_rects):
            if i == level_idx:
                rect.set_stroke(opacity=opacity)
            else:
                rect.set_stroke(opacity=0)

    def highlight_diagram(self, name):
        """Show highlight for a diagram block, hiding the previous one."""
        s = self.slide
        # Hide current highlight if any
        if self._current_diagram_highlight is not None:
            s.remove(self._current_diagram_highlight)
        # Show new highlight if name provided
        if name is not None and name in self.diagram_highlights:
            self._current_diagram_highlight = self.diagram_highlights[name]
            s.add(self._current_diagram_highlight)
        else:
            self._current_diagram_highlight = None



class SAbaControlScene(Slide):
    def construct(self):
        SAbaControl(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
