# CONFIGURATION PARAMETERS

# situational romanization preferences

na_neo_ye = False       # romanize 나의 and 너의 as 'na-ye' and 'neo-ye' respectively (common in songs)
ne_ni = True            # romanize 네 as 'ni' and 네가 as 'ni-ga' (common in spoken Korean)


# purely aesthetic romanization preferences

show_h = 0              # ㅎ-linking: 0 = don't show anything , 1 = show as 'ʰ', 2 = show as 'h'
show_hada_h = True      # if True, always show 'h' for 하다, 한, 했다, etc.
                            # only matters if show_h == 0
sh = True               # if True, romanize ㅅ as 'sh' when preceding ㅣ, ㅑ, etc.
oo = False              # if True, romanize the vowel ㅜ as 'oo' instead of 'u' (and likewise for ㅠ, but not ㅟ)
ee = False              # if True, romanize the vowel ㅣ as 'ee' instead of 'i' (and likewise for ㅟ, but not ㅚ or ㅢ)


# optional non-standard romanization enhancements

always_tense = False    # always show tensing of initial consonants that occur after final consonants
                            # N.B. initial consonants that occur after sonorants (non-obstruents, e.g., ㄶ, ㄼ)
                            # and consequently sound tensed are automatically always denoted as such
                            

# now the fun begins

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


def tense(phoneme):
    if phoneme == 'g': return 'kk'
    if phoneme == 'd': return 'tt'
    if phoneme == 'b': return 'pp'
    if phoneme == 's': return 'ss'
    if phoneme == 'j': return 'jj'
    return phoneme


def romanize_word(word):
    if len(word) == 0:
        return ''

    # special case: 네 becomes '니'
    if ne_ni:
        if word == '네':
            return 'ni'
        elif word == '네가':
            return 'ni-ga'

    phoneme_list = []
    
    # parse Hangul and convert to "naive" letter-by-letter romanization
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

    # first round of sound changes
    for syllable in range(len(word) - 1):
        prev_final = 4*syllable + 2
        next_initial = 4*syllable + 4

        if phoneme_list[prev_final] == 'x' or phoneme_list[next_initial] == 'x':
            continue

        two_syllable = word[syllable : syllable + 2]
        next_syllable = word[syllable + 1]
        next_two_syllable = word[syllable + 1 : syllable + 3]

        # special case: 맛없- becomes '마덦-'
        if two_syllable == '맛없':
            phoneme_list[prev_final] = ''
            phoneme_list[next_initial] = 'd'
            continue

        # common compound words and Sino-Korean words that induce tensing
        if two_syllable in ('글자', '발자', '발전', '여권', '절대'):
            phoneme_list[next_initial] = tense(phoneme_list[next_initial])
            continue

        # special case: semantic ㅇ linking for compound words where the first half ends in a consonant
        # and the second (semantically meaningful) half begins with 야, 여, 요, 유, 이
        # (e.g., 꽃잎 becomes '꼰닢', 색연필 becomes '생년필')
        # N.B. it's hard to generalize this because it depends on the semantics of the word
        if two_syllable in ('담요', '들일', '막일', '맨입', '물약', '삯일', '알약') or \
            phoneme_list[prev_final] != '' and (next_syllable in ('역', '염', '엿', '유', '율', '윷', '잎') \
                                                or next_two_syllable in ('여름', '여비', '여성', '여우', '연필', '열차', '요기', '이불')):
            phoneme_list[next_initial] = 'n'

        # preparing syllable-final consonants for sound changes
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
            elif final_carry == 'n':
                phoneme_list[next_initial] = 'l'
                final_carry = 'l'
        elif phoneme_list[next_initial] == 'n':
            if final_carry == 'r':
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

        # handling placeholder for ㄽ
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
            if final_carry == 'h': # for syllables ending in ㅎ, ㄶ, and ㅀ
                phoneme_list[next_initial] = final_change
                final_change = ''
                final_carry = ''
            elif final_carry not in ('', 'ng'): # general linking case
                phoneme_list[next_initial] = final_carry
                final_carry = ''

        # handling standard cases
        phoneme_list[prev_final] = final_change + final_carry

    # second round of sound changes
    for syllable in range(len(word)):
        initial = 4*syllable
        vowel = 4*syllable + 1
        final = 4*syllable + 2
        next_initial = initial + 4
        next_vowel = vowel + 4

        # flag that indicates if this syllable is the end of a word
        not_last_syllable = (next_initial < len(phoneme_list))

        # flag that indicates whether or not to tense the following initial consonant
        tense_next = False

        # syllable-final consonants
        if phoneme_list[final] in ('g', 'kk', 'gs', 'k'):
            phoneme_list[final] = 'k'
            tense_next = always_tense

        elif phoneme_list[final] in ('n', 'nj', 'nh'):
            tense_next = (phoneme_list[final] == 'nj')
            phoneme_list[final] = 'n'

        elif phoneme_list[final] in ('d', 's', 'ss', 'j', 'ch', 't', 'h'):
            if not_last_syllable and phoneme_list[next_initial] in ('s', 'ss'):
                phoneme_list[final] = ''
                tense_next = True
            else:
                phoneme_list[final] = 't'
                tense_next = always_tense

        elif phoneme_list[final] == 'r':
            phoneme_list[final] = 'l'
            if not_last_syllable and phoneme_list[next_initial] == 'r':
                phoneme_list[next_initial] = 'l'

        if phoneme_list[final] == 'rg':
            if phoneme_list[next_initial] == 'g':
                phoneme_list[final] = 'l'
                tense_next = True
            else:
                phoneme_list[final] = 'k'

        elif phoneme_list[final] == 'rb':
            # special case: 밟 + consonant
            if phoneme_list[initial] == 'b' and phoneme_list[vowel] == 'a':
                phoneme_list[final] = 'p'

            # special case: 넓둥- and 넓죽-
            elif not_last_syllable and phoneme_list[initial] == 'n' and phoneme_list[vowel] == 'eo':
                if phoneme_list[next_initial] == 'd' and phoneme_list[next_vowel] == 'oo':
                    phoneme_list[final] = 'p'
                elif phoneme_list[next_initial] == 'j' and phoneme_list[next_vowel] in ('eo', 'oo'):
                    phoneme_list[final] = 'p'

            # flag that indicates if we entered a special case
            rb_special = (phoneme_list[final] == 'p')

            # ㄼ becomes ㄹ by default
            if not rb_special:
                phoneme_list[final] = 'l'

            # ㄼ always tenses the next consonant (regardless of if it becomes 'ㅍ' or 'ㄹ')
            # but always_tense decides if we include the in our output for the special 'ㅍ' cases
            tense_next = always_tense or not rb_special 

        elif phoneme_list[final] in ('rm', 'm'):
            tense_next = (phoneme_list[final] == 'rm')
            phoneme_list[final] = 'm'

        elif phoneme_list[final] in ('rs', 'rt', 'rh'):
            phoneme_list[final] = 'l'
            tense_next = True

        elif phoneme_list[final] in ('b', 'p'):
            phoneme_list[final] = 'p'
            tense_next = always_tense

        elif phoneme_list[final] in ('bs', 'rp'):
            phoneme_list[final] = 'p'
            tense_next = always_tense

        # tensing
        if not_last_syllable and tense_next:
            phoneme_list[next_initial] = tense(phoneme_list[next_initial])

        # patching in non-Korean characters by handling placeholder
        if phoneme_list[initial] == 'x':
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
                if phoneme_list[next_initial] == 'x':
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
            if phoneme_list[vowel] in ('i', 'wi'):
                phoneme_list[initial] += 'h'
            elif phoneme_list[vowel][0] == 'y':
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
print(romanize("악 앆 안 앋 알 암 압 앗 았 앙 앚 앛 앜 앝 앞 앟"))  # syllable-final consonants
print(romanize("앇 앉 않 앍 앎 앏 앐 앑 앒 앓 앖"))               # syllable-final consonant clusters
print(romanize("희망봉에 숨어있는 마법의 학원에 갔어요. 의의의"))   # ㅇ linking, 의
print(romanize("밝은 곳에 앉으라면 얇은 값이 않아"))              # ㅇ linking (double consonants)
print(romanize("맨입 콩엿 담요 물약 솔잎 색연필 서울역 식용유"))   # ㅇ linking (compound words)
print(romanize("한여름 백분율 밤윷 꽃잎 직행열차 홑이불 불여우"))  # ㅇ linking (more compound words)
print(romanize("고양이가 공허한 고향으로 괜히 방문했다"))         # ㅎ linking
print(romanize("없다 없는 없지"))                              # ㅄ
print(romanize("밟다 밟는 훑다 넓다 넓적하다 넓죽하다 넓둥글다"))  # ㄼ, ㄾ
print(romanize("외곬만 외곬으로 외곬발 알아 앓아"))              # ㄽ, ㅀ
print(romanize("앉다 핥다 넋과 밞다"))                         # tensing
print(romanize("밟는 앞문 부엌문 낮말 낱말 학년 꽃나무 죽었니"))  # nasalization
print(romanize("곧이듣다 얹히다 받히다 닫혀"))                  # palatalization
print(romanize("남루하다 대통령 박람회 합력 설날 안락하다"))      # ㄹ assimilation
print(romanize("못생긴 햇살을 먹겠습니다. 맞습니다."))           # ㅅ/ㅆ assimmilation
print(romanize("좋다 입학 넓히다 싫소 옳지 싫다"))              # aspiration
print(romanize("네가 발자국 맛을 보면 여권 글자가 절대 맛없다"))  # special cases
print(romanize("그래요? 와, 진짜 멋지네요! 참..."))             # clause-final punctuation
print(romanize("\"종이접기\"라는 '취미'예술"))                  # quotation marks
print(romanize("Korean is fun!  Tee샤츠"))                   # non-Korean
print(romanize("   "))                                      # edge case
"""

# exceptions: currently non-functional

"""
print(split_hangul("안다 안고 감다 감고 신다 신고 참다 참고"))  # semantic tensing
print(split_hangul("의견란 영업용"))

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
