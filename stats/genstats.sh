#!/bin/bash

mkdir -p montages

rm -f data-days data-pages
firstday=0
firstrevts=$( git log --reverse --date=iso --format='%at' | head -n1 )
lastrevts=$( git log --date=iso --format='%at' | head -n1 )
number_of_days=$(( ($lastrevts - $firstrevts) / (60*60*24) ))
echo $number_of_days

for day in $( seq $number_of_days -1 0 ); do
    echo $day
    rev=$( git rev-list -n 1 --before="$day days ago" master )
    rev_pdf="revs/$rev/main.pdf"
    rev_bitmap="revs/$rev/all.png"
    if test -f "$rev_bitmap"; then
        if [ $firstday -eq 0 ]; then
            firstday=$day
        fi
        currentday=$(expr $firstday - $day)

        pages=$(pdfinfo "$rev_pdf" | grep 'Pages:' | rev | cut -d ' ' -f 1 | rev)
        echo -n $currentday, >> data-days
        echo -n $pages, >> data-pages
        currentday=$(printf %03d $currentday)
        cp "$rev_bitmap" montages/$currentday-$rev.png
    fi
done

pushd montages

lastfile=$(ls *.png | head -n 1)
for file in $(ls *.png | tail -n +2); do
    echo "Comparing $lastfile and $file"
    hexdump $lastfile > 0.dump
    hexdump $file > 1.dump
    if [ $(diff 0.dump 1.dump | wc -l) -le 6 ]; then
        rm $file
    else
        lastfile=$file
    fi
    rm 0.dump 1.dump
done

for file in *.png; do
    filenumber=${file%-*.png}
    filenumber=$(printf $((10#$filenumber)))
    convert $file -background '#990000' -fill white -pointsize 100 label:"Day $filenumber" -splice 0x50 +swap -gravity Center -append $file
done

popd

ffmpeg -r 2 -pattern_type glob -i 'montages/*.png' -vf scale=1200:-1 thesis_evolution.mp4
