REVS := $(shell git rev-list master | tac)
REV_DIRS := $(addprefix revs/,$(REVS))
REV_BITMAPS := $(addsuffix /all.png,$(REV_DIRS))
REV_PDFS := $(addsuffix /main.pdf,$(REV_DIRS))

.IGNORE:
.PRECIOUS: revs/%/main.pdf


all: $(REV_BITMAPS) $(REV_PDFS)

revs/%/main.pdf:
	@mkdir -p revs
	test -d revs/$*/.git || git clone .. revs/$*
	git -C revs/$* checkout $* 2>/dev/null >/dev/null
	echo X | make -C revs/$* >/dev/null 2>/dev/null

revs/%/all.png: revs/%/main.pdf
	@mkdir -p revs/$*/bitmaps
	convert +profile "icc" revs/$*/main.pdf 'revs/$*/bitmaps/%03d.png'
	montage -tile 24x11 -geometry 200x300 revs/$*/bitmaps/*.png $@
