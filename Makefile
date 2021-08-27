MAIN = main
BUILD = _build

all: img $(MAIN).pdf

img:
	make -C $@

$(MAIN).pdf:
	latexmk $(MAIN).tex
	mv $(BUILD)/$(MAIN).pdf $(MAIN).pdf

clean:
	$(RM) -r $(BUILD)

distclean: clean
	$(RM) main.pdf

.PHONY: $(MAIN)-report-textidote.html
$(MAIN)-report-textidote.html:
	textidote main.tex > $@

textidote: $(MAIN)-report-textidote.html

.PHONY: $(MAIN).pdf img textidote
