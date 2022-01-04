# JarBeGone
"Jar(gon)-be-gone"

Shows word frequencies of text extracted from a TeX file against an nltk word corpus... or more simply, procratination of actual work.

## Requirements
Requires modules: `texsoup` & `nltk`

## Usage
```bash
# JarBeGone version 0.1
#  usage: jarbegone0.1.py [-h] file threshold
#
#  positional arguments:
#    file        The TeX filepath to analyse
#    threshold   Upper threshold to highlight infrequent words (percentage)), default=10
```

## Example output
```bash
python jarbegone0.1.py test.tex 10
```
a
```
Building frequency distribution
Extracting words from TeX document
Cleaning...
Stemming...
Possible Jargon words:
  sacr - 5.426615461679746e-05
  also - 0.0014874492124450382
  known - 0.0003409027661824456
  red - 0.0002810708521177715
  life - 0.0009948795013079534
Done.
```
