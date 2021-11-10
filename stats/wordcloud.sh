#!/bin/bash

( cd .. && pandoc -t plain main.tex -o main.txt )
mv ../main.txt .
wordcloud_cli --no_collocations --width 1200 --height 600 --max_words 100000 --background white --text main.txt --imagefile wordcloud.png
