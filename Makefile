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


.PHONY: $(MAIN).pdf img
