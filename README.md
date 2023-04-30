# Phonetic Korean Romanization

A script to romanize Hangul text in a way that reflects accurate pronuniciation.


## Context

This romanization scheme is an adaptation of the Revised Romanzation of Korean (RR), the most commonly used and widely accepted Korean romanzation scheme worldwide. However, it is important to note that RR strikes a balance between how the Hangul is written and how the spoken Korean sounds. Naturally, this comes with its benefits and drawbacks. The purpose of this script is to lean completely in one direction, prioritizing accurate transcription of speech and syllable boundaries over accurate transliteration of writing.

Here is an example sentence to help get a better sense of the similarities and differences between these systems:

| System | Text |
| ----------- | ----------- |
| Hangul | 원하시는 선 색깔과 굵기에 체크하시면 됩니다. |
| This script (with default settings) | weon-ha-shi-neun seon saek-kkal-gwa gul-kki-e che-keu-ha-shi-myeon dwem-ni-da. |
| RR | Wonhasineun seon saekkkalgwa gulkkie chekeuhasimyeon doemnida. |
| RR transliteration | Wonhasineun seon saegkkalgwa gulggie chekeuhasimyeon doebnida. |
| English translation | Just check the line color and width you want. |

Not all sound change rules have been implemented; in particular, some rules which require an understanding of the semantics of the text are not fully considered for sake of simplicity. This code will probably also produce strange results on certain types of words such as internet slang, text speak, abbreviations, and foreign loanwords.


## Usage

Two important functions are defined in the `korean_romanization.py` script. The first function, `romanize()`, takes in a string of Hangul characters and outputs a phonetic romanization. Here, "phonetic romanization" means that most sound change rules are obeyed, including nasalizations, palatalizations, assimilations, linking, and syllable-final de-voicing/de-aspiration.

The second function, `romanize_file()`, when given an input file location and an output file location, romanizes any Hangul text in the input file line-by line and writes the resulting text to the output file.

Sample usages:
```python3
romanize("잘 먹겠습니다")     # jal meok-ge-sseum-ni-da 
romanize_file("Jopping_SuperM_Hangul.txt", "Jopping_SuperM_Romanized.txt")
```

These functions can be imported and used in other scripts, for example:
```python3
from korean_romanization import romanize as hangul_to_latin
hangul_to_latin("동서남북")  # dong-seo-nam-buk
```

Directly running the `korean_romanization.py` script will also start an interactive session which allows the user to quickly romanize individual lines of Hangul. (Ensure that the terminal in which you are running the session is configured to use UTF-8 to encode strings. Notably, [this is not the default for Git Bash on Windows](https://stackoverflow.com/questions/45660817/python-print-unicode-string-via-git-bash-gets-unicodeencodeerror).


## Compatibility

This script requires Python 3.10 or above.


## Resources

Learn how to pronounce the romanized text with [this handy guide](https://docs.google.com/document/d/1XNkx1R6ImgwYNysgWlGWjXfG1Xzb6qSvdctRAhZvpis/edit?usp=sharing)!

Pronuniciation rules have been sourced from the following webpages:
- [Korean phonology – Wikipedia](https://en.wikipedia.org/wiki/Korean_phonology)
- [Advanced Korean Pronuniciation Rules – Wikibooks](https://en.wikibooks.org/wiki/Korean/Advanced_Pronunciation_Rules)
- [표준 발음법 – 조의성](http://www.tufs.ac.jp/ts/personal/choes/korean/nanboku/Barum.html)

Other relevant resources:
- [Korean language – Wikipedia](https://en.wikipedia.org/wiki/Korean_language)
- [Hangul – Wikipedia](https://en.wikipedia.org/wiki/Hangul)
- [Revised Romanization of Korean – Wikipedia](https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean)
