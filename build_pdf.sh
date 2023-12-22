# sudo apt-get install pdflatex
# sudo apt-get install texlive-xetex

set -e
python3 prepare_combined_content.py
cd stories
pandoc ../combined_content.md --pdf-engine=xelatex -V mainfont="Liberation Serif" --toc -o ../b1-deutsch-ai-storybook-eng-rus.pdf
