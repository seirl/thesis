MAIN = main
BUILD = _build

all: $(MAIN).pdf

$(MAIN).pdf:
	latexmk $(MAIN).tex
	mv $(BUILD)/$(MAIN).pdf $(MAIN).pdf

clean:
	$(RM) -r $(BUILD)

distclean: clean
	$(RM) main.pdf


.PHONY: main.pdf
