# Config
SLIDES_DIR := slides
SHELL := /bin/bash
# Strip inline comments and blank lines, then pick scene class (2nd column)
SCENES := $(shell sed 's/#.*//' scenes.list | awk 'NF{print $$2}')

# Default: build and serve full deck
.PHONY: all
all: build serve

.PHONY: build
build:
	@set -e; \
	sed 's/#.*//' scenes.list | awk 'NF{print $$1, $$2}' | \
	while read -r file scene; do \
		echo "Rendering $$scene from $$file"; \
		PYTHONPATH=. manim -qh $$file $$scene; \
	done

.PHONY: serve
serve:
	PYTHONPATH=. manim-slides $(SCENES)

.PHONY: html
html:
	PYTHONPATH=. manim-slides convert $(SCENES) docs/index.html

.PHONY: pdf
pdf:
	PYTHONPATH=. manim-slides convert $(SCENES) docs/slides.pdf

# Generic single slide build + show: underscore_case -> CamelCase
# Single slide build + show
.PHONY: %

%:
	PYTHONPATH=. manim -qh $(SLIDES_DIR)/$@.py $(shell echo $@ | sed -r 's/(^|_)([a-z])/\U\2/g')Scene && manim-slides $(shell echo $@ | sed -r 's/(^|_)([a-z])/\U\2/g')Scene


# manim slides all
# manim-slides convert SemTitleScene gorczyca-semantics.pdf
# manim-slides convert SemTitle SemTitle.html

# MANIM_SLIDES_NO_REVERSE=1 PYTHONPATH=. manim slides/sem_video.py SemVideoScene -ql  


# build single slide
# PYTHONPATH=. manim slides/sem_title.py SemTitleScene


# merge to html
# PYTHONPATH=. manim-slides SemTitleScene SemInitialScene SemMotivationScene SemCurrentPracticesScene SemRiskmanMethodScene SemGraphEncodingScene SemEncRules1Scene SemEncRules2Scene SemEncRules3Scene SemReasoningValidationScene SemMoreShaclScene SemRiskmanStatsScene SemHumanReadabilityScene SemVideoScene SemConclusionScene

# Deploy to GitHub Pages (uploads docs/ folder)
.PHONY: deploy
deploy:
	@echo "Deploying slides to GitHub Pages..."
	touch docs/.nojekyll
	@changes=$$(git status --porcelain docs); \
	if [ -z "$$changes" ]; then \
		echo "No changes in docs/ to deploy; skipping commit."; \
	else \
		git add docs/ && \
		git commit -m "Deploy slides to GitHub Pages" && \
		git push && \
		echo "Deployed! Check your GitHub Pages URL."; \
	fi
