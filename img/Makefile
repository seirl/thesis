all: swh-cardinality.pdf swh-merkle-dag.pdf

%.pdf: %.dot
	dot -Tpdf -Gmargin=0 $^ > $@

%.pdf: %.svg
	inkscape $^ --export-filename=$@
