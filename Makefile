MAIN = main
BUILD = _build

all: $(MAIN).pdf

$(MAIN).pdf:
	latexmk -xelatex -outdir=$(BUILD) $(MAIN).tex
	mv $(BUILD)/$(MAIN).pdf $(MAIN).pdf

$(MAIN).expanded.tex:
	latexpand $(MAIN).tex > $@

clean:
	$(RM) -r $(BUILD)

distclean: clean
	$(RM) main.pdf


.PHONY: main.pdf
