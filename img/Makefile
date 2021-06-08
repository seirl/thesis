BUILD=../_build

all: swh-cardinality.pdf swh-merkle-dag.pdf roadmap.pdf

%.pdf: %.dot
	dot -Tpdf -Gmargin=0 $^ > $@

%.pdf: %.svg
	inkscape $^ --export-filename=$@

%.pdf: %.tex
	latexmk -xelatex -outdir=$(BUILD) $^
	mv $(BUILD)/$@ $@
