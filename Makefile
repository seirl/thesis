all: main.pdf

main.pdf:
	latexmk -xelatex -outdir=_build main.tex
	mv _build/main.pdf main.pdf

clean:
	$(RM) -r _build

distclean: clean
	$(RM) main.pdf


.PHONY: main.pdf
