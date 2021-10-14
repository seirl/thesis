BUILD=../_build

all: swh-merkle-dag.pdf fuse/arch-container.pdf vault/arch-container.pdf \
	graph-dataset/db-schema.pdf frontmatter/inria.pdf

%.pdf: %.dot
	dot -Tpdf -Gmargin=0 $^ > $@

%.pdf: %.tex
	latexmk -xelatex -outdir=$(BUILD) $^
	mv $(BUILD)/$@ $@

%.pdf: %.puml
	plantuml -Tpdf $<

%.png: %.puml
	plantuml -Tpng $<

%.svg: %.puml
	plantuml -Tsvg $<

%.pdf: %.svg
	inkscape $^ --export-filename=$@
