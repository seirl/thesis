MAIN = slides
BUILD = _build

all: $(MAIN).pdf

img:
	make -C $@

$(MAIN).pdf:
	latexmk $(MAIN).tex
	mv $(BUILD)/$(MAIN).pdf $(MAIN).pdf

clean:
	$(RM) -r $(BUILD)

distclean: clean
	$(RM) $(MAIN).pdf

.PHONY: $(MAIN).pdf
