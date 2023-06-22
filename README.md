# Phonetic Korean Romanization

A self-contained Python module to romanize Hangul text in a way that reflects accurate pronuniciation.


## Context

This romanization scheme is an adaptation of the Revised Romanzation of Korean (RR), the most commonly used and widely accepted Korean romanzation scheme worldwide. However, it is important to note that RR strikes a balance between how the Hangul is written and how the spoken Korean sounds. Naturally, this comes with its benefits and drawbacks. The purpose of this program is to lean completely in one direction, prioritizing accurate transcription of speech and syllable boundaries over accurate transliteration of writing.

Here is an example sentence to help get a better sense of the similarities and differences between these systems:

| System | Text |
| ----------- | ----------- |
| Hangul | 원하시는 선 밝기, 색깔과 굵기에 체크하시면 됩니다. |
| This program (default settings) | weon-ha-shi-neun seon bal-kki, saek-kkal-gwa gul-kki-e che-keu-ha-shi-myeon dwem-ni-da. |
| RR | Wonhasineun seon balkgi, saekkkalgwa gulkkie chekeuhasimyeon doemnida. |
| RR transliteration | Wonhasineun seon balggi, saegkkalgwa gulggie chekeuhasimyeon doebnida. |
| English translation | Just check the line brightness, color and width you want. |

Not all sound change rules have been implemented; in particular, some rules which require an understanding of the semantics of the text are not fully considered for sake of simplicity. This code will probably also produce strange results on certain types of words such as internet slang, text speak, abbreviations, and foreign loanwords.


## Usage

Two important functions are defined as instance methods of the `HangulRomanizer` class in the `korean_romanization.py` file. The first function, `romanize()`, takes in a string of Hangul characters and outputs a phonetic romanization. Here, "phonetic romanization" means that most sound change rules are obeyed, including nasalizations, palatalizations, assimilations, linking, and syllable-final de-voicing/de-aspiration.

The second function, `romanize_file()`, when given an input file location and an output file location, romanizes any Hangul text in the input file line-by line and writes the resulting text to the output file.

Sample usages:
```python3
hangul_romanizer = HangulRomanizer()
hangul_romanizer.romanize("잘 먹겠습니다")    # jal meok-ge-sseum-ni-da 
hangul_romanizer.romanize_file("Jopping_SuperM_Hangul.txt", "Jopping_SuperM_Romanized.txt")
```

The `HangulRomanizer` class can be imported and used in other files, for example:
```python3
from korean_romanization import HangulRomanizer
hangul_romanizer = HangulRomanizer()
hangul_romanizer.romanize("동서남북")    # dong-seo-nam-buk
```


## Compatibility

This script requires Python 3.10 or above.


## Testing

Making local edits and want to test your code? First ensure that you have pytest installed:
```
$ pytest --version
pytest 7.3.2
```

If your command line does not display a version number 7.3.0 or higher, install/update pytest:
```
$ pip install -U pytest
```

To run the full suite of unit tests on this module, simply navigate to the main directory in your command line and run `pytest` (default output) or `pytest -q` ("quiet" reporting mode):
```
$ pytest -q
...                                                                      [100%]
1 passed in 0.17s
```

The test files are located in the `tests/` directory.
Check out the [pytest documentation](https://docs.pytest.org/en/7.3.x/) for information on how to run select test functions or write your own test cases.


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
