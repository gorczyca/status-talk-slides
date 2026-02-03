# View Live
https://gorczyca.github.io/status-talk-slides/  (F11 for fullscreen)

### Installation

```bash
uv venv .venv   # create environment
source .venv/bin/activate # activate environment 
uv pip install "manim-slides[manim]" #  install manim / manim-slides
uv pip install PySide6 pandas
```

### Workflow
For each new slide `slide_x`, create a new script in the `slides/` directory. Make sure it has the following structure and naming convention:

```python
from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide

class SlideX(BaseSlide):
    TITLE = "Hello"

    def create_content(self):
        eq = MathTex(r"E=mc^2", r"\text{not true}" , color=self.FONT_COLOR)
        self.slide.add(eq)
        
        
class SlideXScene(Slide):  
    def construct(self):
        Slide1(self)
        self.wait()
```
then, to view this standalone slide run:
```bash
make slide_x
```
which should display the standalone slide. Make sure to follow the naming convention, script name in snake case, i.e. `my_first_slide.py`, then the main class name inside `MyFirstSlide` and for running standalone `MyFirstSlideScene` inside of the same script. For reference check [`slides/title.py`](slides/title.py).

### What does `make` do?
If you run `make some_file_name`, the following commands will be executed:
```bash
PYTHONPATH=. manim slides/some_file_name.py SomeFileNameScene  # build the SomeFileNameScene
PYTHONPATH=. manim-slides SomeFuleNameScene                    # show SomeFileNameScene as slide show
```

### Showing whole slidedeck / converting to HTML
Assume the following scenes have been built: `FirstScene`, `SecondScene`, ..., `NthScene` that constitute your entire slide deck. To combine them and run / convert to html / convert to pdf, execute (respectively):

```sh
PYTHONPATH=. manim-slides FirstScene SecondScene ... NthScene           # combine and show

PYTHONPATH=. manim-slides convert FirstScene SecondScene ... NthScene slides.html  # combine and convert to HTML

PYTHONPATH=. manim-slides convert FirstScene SecondScene ... NthScene slides.pdf  # combine and convert to PDF
```

where `slides.html` (`slides.pdf`) can be any filename with `*.html` file extension.
