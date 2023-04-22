"""
Creator: Justin Park
Email: justin.s.park77@gmail.com
Last Updated: October 9, 2022

This script initializes the romanize() function, which takes in a string of Hangul characters
and outputs a proper romanization, obeying most sound change rules including nasalizations,
palatalizations, assimilations, linking, and syllable-final de-voicing/de-aspiration.

As of 2022 Oct 9, this file also contains a romanize_file() function, which takes in two file
locations and and romanizes any Hangul text in the input file line-by line, writing the
resulting text to the output file.

Pronunciation rules have been sourced from the following webpages:
https://en.wikibooks.org/wiki/Korean/Advanced_Pronunciation_Rules
https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=88058

Not all sound change rules have been implemented; in particular, some rules which require an
understanding of the semantics of the text are not fully considered for sake of simplicity.

N.B. This code may exhibit unexpected behavior on text with punctuation.

"""

show_h = 0              # 0 = don't show, 1 = show as "ʰ", 2 = show as "h"
show_hada_h = True      # toggle showing "h" for 하다, 한, 했다, etc.
                            # only matters if show_h == 0
sh = False              # romanize ㅅ as "sh" when preceding ㅣ, ㅑ, etc.
oo = False              # toggle to romanize the vowel ㅜ as "oo" instead of "u" (and likewise for ㅠ, but not ㅟ)
ee = False              # toggle to romanize the vowel ㅣ as either "ee" or "i" (and likewise for ㅟ, but not ㅚ or ㅢ)
always_tense = False    # toggle whether to show tensing of initial consonants that occur after final consonants
                            # initial consonants that occur after sonorants (non-obstruents, e.g. ㄶ, ㄼ)
                            # but should be tensed are automatically denoted as such
na_neo_ye = True        # romanize 나의 and 너의 as "na-ye" and "neo-ye" respectively

initial_consonant_count = 19
initial_consonant_phonetics = [
    'g',
    'kk',
    'n',
    'd',
    'tt',
    'r',
    'm',
    'b',
    'pp',
    's',
    'ss',
    '',
    'j',
    'jj',
    'ch',
    'k',
    't',
    'p',
    'h'
]

final_consonant_count = 28
final_consonant_phonetics = [
    '',
    'g',
    'kk',
    'gs',
    'n',
    'nj',
    'nh',
    'd',
    'r',
    'rg',
    'rm',
    'rb',
    'rs',
    'rt',
    'rp',
    'rh',
    'm',
    'b',
    'bs',
    's',
    'ss',
    'ng',
    'j',
    'ch',
    'k',
    't',
    'p',
    'h'
]

vowel_count = 21
vowel_phonetics = [
    'a',
    'ae',
    'ya',
    'yae',
    'eo',
    'e',
    'yeo',
    'ye',
    'o',
    'wa',
    'wae',
    'we',
    'yo',
    'oo',
    'weo',
    'we',
    'wi',
    'yoo',
    'eu',
    'ui',
    'i'
]

hangul_blocks = 44032
block_count = 11172


def romanize_word(word):
    if len(word) == 0:
        return ''

    phoneme_list = []
    
    # parse Hangul and convert "naive" sound-by-sound romanization
    for syllable in range(len(word)):            
        block_ord = ord(word[syllable]) - hangul_blocks

        if block_ord == 7000: # 의
            phoneme_list.append('')
            if syllable == 0:
                phoneme_list.append('q') # placeholder for non-modified ㅢ
            elif syllable == len(word) - 1: # 의 -> '에'  –  should be only for grammatical particle, but not sure how to code that
                if na_neo_ye and syllable == 1 and word[0] in ('나', '너'):
                    phoneme_list.append('ye')
                else:
                    phoneme_list.append('e')
            else:
                phoneme_list.append('ui')
            phoneme_list.append('')
        elif 0 <= block_ord < block_count:
            final = final_consonant_phonetics[block_ord % final_consonant_count]
            trunc = block_ord // final_consonant_count
            vowel = vowel_phonetics[trunc % vowel_count]
            initial = initial_consonant_phonetics[trunc // vowel_count]
            phoneme_list.append(initial)
            phoneme_list.append(vowel)
            phoneme_list.append(final)
        else:
            phoneme_list.append('x') # placeholder for non-Korean characters
            phoneme_list.append(word[syllable])
            phoneme_list.append('x')
            
        phoneme_list.append('-')

    # sound changes
    for syllable in range(len(word) - 1):
        prev_final = 4*syllable + 2
        next_initial = 4*syllable + 4

        if phoneme_list[prev_final] == 'x' or phoneme_list[next_initial] == 'x':
            continue

        # special case: 꽃잎 becomes '꼰닢'
        if word[syllable:syllable+2] == '꽃잎':
            phoneme_list[prev_final] = phoneme_list[next_initial] = 'n'
            continue

        # special case: 맛없- becomes '맏 없'
        if word[syllable:syllable+2] == '맛없':
            phoneme_list[prev_final] = 't'
            continue

        # special cases: 설날, 줄넘기, 칼날 become 설랄, etc.
        # N.B. I couldn't find a good rule for when ㄹㄴ assimilates in general
        if word[syllable:syllable+2] in ('설날', '줄넘', '칼날'):
            phoneme_list[next_initial] = 'l'
            continue

        # split double consonants in syllable-final position
        if len(phoneme_list[prev_final]) == 0:
            final_change = ''
            final_carry = ''
        elif len(phoneme_list[prev_final]) == 1:
            final_change = ''
            final_carry = phoneme_list[prev_final]
        elif phoneme_list[prev_final] in ('kk', 'ss', 'ng', 'ch'):
            final_change = ''
            final_carry = phoneme_list[prev_final]
        elif phoneme_list[prev_final] == 'rs':
            final_change = 'r'
            final_carry = 'v' # placeholder for ㄽ
        else:
            final_change = phoneme_list[prev_final][0]
            final_carry = phoneme_list[prev_final][1]

        # nasalization
        if phoneme_list[next_initial] in ('n', 'm'):
            if final_carry in ('g', 'kk', 'k'):
                final_change = 'ng'
                final_carry = ''
            elif final_change == 'b' or final_carry in ('b', 'pp', 'p'):
                final_change = 'm'
                final_carry = ''
            elif final_carry in ('d', 's', 'ss', 'j', 'ch', 't', 'h'):
                final_change = 'n'
                final_carry = ''

        # ㄹ assimilation
        if phoneme_list[next_initial] == 'r':
            if final_carry in ('g', 'ng'):
                phoneme_list[next_initial] = 'n'
                final_carry = 'ng'
            elif final_carry in ('m', 'b'):
                phoneme_list[next_initial] = 'n'
                final_carry = 'm'
            elif final_carry == 'n': # TODO hard-code exceptions?
                phoneme_list[next_initial] = 'l'
                final_carry = 'l'

        # palatalization
        # N.B. this should only occur for 이, 히, 여, 혀 as grammatical particles, but oh well
        if phoneme_list[next_initial + 1] in ('i', 'yeo'):
            if phoneme_list[next_initial] == '':
                if final_carry == 'd':
                    phoneme_list[next_initial] = 'j'
                    final_carry = ''
                elif final_carry == 't':
                    phoneme_list[next_initial] = 'ch'
                    final_carry = ''
            elif phoneme_list[next_initial] == 'h':
                if final_carry in ('d', 's', 'ss', 'j', 'ch', 't', 'h'):
                    phoneme_list[next_initial] = 'ch'
                    final_carry = ''

        # aspiration
        if final_carry == 'h':
            if phoneme_list[next_initial] == 'g':
                phoneme_list[next_initial] = 'k'
                final_carry = ''
            if phoneme_list[next_initial] == 'd':
                phoneme_list[next_initial] = 't'
                final_carry = ''
            if phoneme_list[next_initial] == 's':
                phoneme_list[next_initial] = 'ss'
                final_carry = ''
            if phoneme_list[next_initial] == 'j':
                phoneme_list[next_initial] = 'ch'
                final_carry = ''

        # more aspiration
        if phoneme_list[next_initial] == 'h':
            if final_carry == 'g':
                phoneme_list[next_initial] = 'k'
                final_carry = ''
            elif final_carry in ('d', 's', 'ss', 'j', 'ch', 'v'):
                phoneme_list[next_initial] = 't'
                final_carry = ''
            elif final_carry == 'b':
                phoneme_list[next_initial] = 'p'
                final_carry = ''
            else:
                if show_h == 0:
                    # ㅎ-linking (not prescriptive)
                    # if show_hada_h = True, create an exception for 하다, 한, 했다, etc.
                    # N.B. this exception is over-sensitive because it doesn't consider semantics
                    if not (show_hada_h and phoneme_list[next_initial + 1] in ('a', 'ae')):
                        if final_carry not in ('', 'ng'):
                            phoneme_list[next_initial] = final_carry
                            final_carry = ''
                        else:
                            phoneme_list[next_initial] = ''
                elif show_h == 1:
                    phoneme_list[next_initial] = 'ʰ'

        # deal with placeholder for ㄽ
        if final_carry == 'v':
            if phoneme_list[next_initial] == '': # ㄽ + ㅇ = ㄹ + ㅆ
                phoneme_list[next_initial] = 'ss'
                final_carry = ''
            elif phoneme_list[next_initial] == 'b': # ㄽ + ㅂ = ㄹ + ㅃ
                phoneme_list[next_initial] = 'pp'
                final_carry = ''
            else:
                final_carry = ''

        # linking
        if phoneme_list[next_initial] == '':
            if final_carry == 'h':
                phoneme_list[next_initial] = final_change
                final_change = ''
                final_carry = ''
            elif final_carry not in ('', 'ng'):
                phoneme_list[next_initial] = final_carry
                final_carry = ''

        # deal with standard cases
        phoneme_list[prev_final] = final_change + final_carry

    # more sound changes
    for syllable in range(len(word)):
        initial = 4*syllable
        vowel = 4*syllable + 1
        final = 4*syllable + 2

        # syllable-final consonants
        tense = False
        if phoneme_list[final] in ('g', 'gs', 'rg', 'k', 'kk'):
            phoneme_list[final] = 'k'
            if always_tense:
                tense = True
        elif phoneme_list[final] in ('n', 'nj', 'nh'):
            if phoneme_list[final] == 'nj':
                tense = True
            phoneme_list[final] = 'n'
        elif phoneme_list[final] in ('d', 's', 'ss', 'j', 'ch', 't', 'h'):
            phoneme_list[final] = 't'
            if always_tense:
                tense = True
        elif phoneme_list[final] == 'r':
            phoneme_list[final] = 'l'
            try:
               if phoneme_list[initial + 4] == 'r':
                   phoneme_list[initial + 4] = 'l'
            except IndexError:
                pass
        elif phoneme_list[final] in ('rs', 'rt', 'rh'):
            phoneme_list[final] = 'l'
            tense = True
        elif phoneme_list[final] == 'rb': # hard-coding special cases for ㄼ
            if phoneme_list[initial] == 'b' and phoneme_list[vowel] == 'a':
                phoneme_list[final] = 'p'
            else:
                try:
                    if phoneme_list[initial] == 'n' and phoneme_list[vowel] == 'eo':
                        if phoneme_list[initial + 4] == 'd' and phoneme_list[vowel + 4] == 'oo':
                            phoneme_list[final] = 'p'
                        elif phoneme_list[initial + 4] == 'j' and phoneme_list[vowel + 4] in ('eo', 'oo'):
                            phoneme_list[final] = 'p'
                        else:
                            raise IndexError # lmao
                except IndexError:
                    phoneme_list[final] = 'l'
                    tense = True
            if always_tense:
                tense = True
        elif phoneme_list[final] in ('rm', 'm'):
            if phoneme_list[final] == 'rm':
                tense = True
            phoneme_list[final] = 'm'
        elif phoneme_list[final] in ('b', 'pp', 'p'):
            phoneme_list[final] = 'p'
            if always_tense:
                tense = True
        elif phoneme_list[final] in ('bs', 'rb', 'rp'):
            phoneme_list[final] = 'p'
            if always_tense:
                tense = True

        # tensing - some of these rules should depend on whether the final-consonant obstruent is the end of a word stem, but oh well
        if tense and initial + 4 < len(phoneme_list):
            if phoneme_list[initial + 4] == 'g':
                phoneme_list[initial + 4] = 'kk'
            elif phoneme_list[initial + 4] == 'd':
                phoneme_list[initial + 4] = 'tt'
            elif phoneme_list[initial + 4] == 'b':
                phoneme_list[initial + 4] = 'pp'
            elif phoneme_list[initial + 4] == 's':
                phoneme_list[initial + 4] = 'ss'
            elif phoneme_list[initial + 4] == 'j':
                phoneme_list[initial + 4] = 'jj'
                
        if phoneme_list[initial] == 'x': # patch in non-Korean characters by handling placeholder
            phoneme_list[initial] = ''
            phoneme_list[final] = ''
            try:
                # punctuation at the end of a clause
                if phoneme_list[vowel] in ('!', ',', '.', '?'):
                    phoneme_list[initial - 1] = ''

                # quotation marks
                if phoneme_list[vowel] in ('\'', '"'):
                    if initial == 0:
                        phoneme_list[final + 1] = ''
                    else:
                        phoneme_list[initial - 1] = ''

                # next character is also non-Korean
                if phoneme_list[initial + 4] == 'x':
                    phoneme_list[final + 1] = ''
            except IndexError:
                pass
            continue

        if len(phoneme_list[vowel]) == 0:
            continue
            
        if phoneme_list[vowel] == 'ui': # common sound change; occurs for everything except word-initial and grammatical 의
            phoneme_list[vowel] = 'i'
        elif phoneme_list[vowel] == 'q': # deal with placeholder
            phoneme_list[vowel] = 'ui'
            
        if sh and phoneme_list[initial] in ('s', 'ss'): # add 'h' to certain ㅅ, ㅆ sounds for more intuitive pronunciation
            if phoneme_list[vowel] == 'i':
                phoneme_list[initial] += 'h'
            if phoneme_list[vowel][0] == 'y':
                phoneme_list[initial] += 'h'
                phoneme_list[vowel] = phoneme_list[vowel][1:]

        if phoneme_list[initial] in ('j', 'jj', 'ch'): # remove 'y' from ㅈ, ㅉ, ㅊ sounds
            if phoneme_list[vowel][0] == 'y':
                phoneme_list[vowel] = phoneme_list[4*syllable + 1][1:]

        if not oo:
            if phoneme_list[vowel] in ('oo', 'yoo'):
                phoneme_list[vowel] = phoneme_list[vowel][0:-2] + 'u'

        if ee:
            if phoneme_list[vowel] in ('i', 'wi'):
                phoneme_list[vowel] = phoneme_list[vowel][0:-1] + 'ee'

    # return combined result
    phoneme_list.pop()
    return(''.join(phoneme_list))


def romanize(hangul_string):
    hangul_string = hangul_string.strip()
    if len(hangul_string) == 0:
        return ''
    
    word_list = []
    hangul_words = hangul_string.split(' ')
    
    for word in hangul_words:
        word_list.append(romanize_word(word))
        
    romanized_string = ' '.join(word_list)
    return romanized_string


def romanize_file(hangul_in, romanized_out):
    # read Hangul text from file
    with open(hangul_in, 'r', encoding='utf8') as reader:
        original_text = reader.readlines()

    # write romanization to file
    with open(romanized_out, 'w', encoding='utf8') as writer:
        for line in original_text:
            writer.write(romanize(line) + '\n')


# TEST CASES

"""
print(romanize("희망봉에 있는 마법의 학원에 갔어요. 의의의"))      # linking, 의
print(romanize("없다 없는 없지"))                              # ㅄ
print(romanize("밟다 밟는 훑다 넓다 넓적하다 넓죽하다 넓둥글다"))  # ㄼ, ㄾ
print(romanize("외곬만 외곬으로 외곬발 알아 앓아"))              # ㄽ, ㅀ
print(romanize("앉다 핥다 넋과 밞다"))                         # tensing
print(romanize("고양이가 공허한 고향으로 괜히 방문했다"))         # ㅎ linking
print(romanize("Korean is fun!  Tee샤츠"))                   # non-Korean
print(romanize("밝 밞 밝은 곳으로 갑쇼"))                      # general
print(romanize("밟는 앞문 부엌문 낮말 낱말 학년 꽃나무 죽었니"))  # nasalization
print(romanize("곧이듣다 얹히다 받히다 닫혀"))                  # palatalization
print(romanize("남루하다 대통령 박람회 합력 설날 안락하다"))      # ㄹ assimilation
print(romanize("좋다 입학 넓히다 싫소 옳지 싫다"))              # aspiration
print(romanize("꽃잎은 맛없어요"))                            # special cases
print(romanize("그래요? 와, 진짜 멋지네요! 참..."))            # clause-final punctuation
print(romanize("\"종이접기\"라는 '취미'예술"))                  # quotation marks
print(romanize("   "))                                      # edge case
"""

# exceptions: currently non-functional

"""
print(split_hangul("안다 의견란 여권"))
"""

# considerations

"""
쉬 -> swi? shi? shwi? sui? shui?
"""


if __name__ == '__main__':
    while True:
        hangul = input("Hangul (Korean) text to romanize: ")
        print(romanize(hangul))
        print()
