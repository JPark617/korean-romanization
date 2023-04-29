# CONFIGURATION PARAMETERS

# situational romanization preferences

na_neo_ye = False       # romanize 나의 and 너의 as 'na-ye' and 'neo-ye' respectively (common in songs)
ne_ni = True            # romanize 네 as 'ni' and 네가 as 'ni-ga' (common in spoken Korean)


# purely aesthetic romanization preferences

show_h = 0              # ㅎ linking: 0 = don't show anything (not prescriptive), 1 = show as 'ʰ', 2 = show as 'h'
show_hada_h = True      # if True, always show 'h' for 하다, 한, 했다, etc.
                            # only matters if show_h == 0
sh = True               # if True, romanize ㅅ as 'sh' when preceding ㅣ, ㅑ, etc.
oo = False              # if True, romanize the vowel ㅜ as 'oo' instead of 'u' (and likewise for ㅠ, but not ㅟ)
ee = False              # if True, romanize the vowel ㅣ as 'ee' instead of 'i' (and likewise for ㅟ, but not ㅚ or ㅢ)
no_y = False            # if True, remove the 'y' from the romanization of ㅑ, ㅕ, ㅛ, ㅠ when following ㅈ, ㅉ, ㅊ
                            # NOTE: this configuration option exists because, for example, 자 and 쟈 sound extremely similar
                            # and so some people might not find it critical for their use case to distinguish between the two


# optional non-standard romanization enhancements

always_tense = False    # always show tensing of initial consonants that occur after final consonants
                            # NOTE: initial consonants that occur after sonorants (non-obstruents, e.g., ㄶ, ㄼ)
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


def tense_consonant(phoneme):
    match phoneme:
        case 'g': return 'kk'
        case 'd': return 'tt'
        case 'b': return 'pp'
        case 's': return 'ss'
        case 'j': return 'jj'
        case _: return phoneme


def romanize_word(word):
    if len(word) == 0:
        return ''

    # special case: 네 -> '니'
    if ne_ni:
        if word == '네':
            return 'ni'
        elif word == '네가':
            return 'ni-ga'

    phoneme_list = []
    
    # parsing Hangul and converting to "naive" letter-by-letter romanization
    for syllable in range(len(word)):
        block_ord = ord(word[syllable]) - hangul_blocks

        if block_ord == 7000: # 의
            phoneme_list.append('')
            if syllable == 0:
                phoneme_list.append('q') # placeholder for non-modified ㅢ
            elif syllable == len(word) - 1: # 의 -> '에' (NOTE: technically, this only applies to the grammatical particle 의)
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
        initial = 4*syllable
        final = 4*syllable + 2
        next_initial = initial + 4

        if phoneme_list[final] == 'x' or phoneme_list[next_initial] == 'x':
            continue

        two_syllable = word[syllable : syllable + 2]
        next_syllable = word[syllable + 1]
        next_two_syllable = word[syllable + 1 : syllable + 3]

        # semantic ㅇ linking for compound words where the first half ends in a consonant
        # and the second (semantically meaningful) half begins with 야, 여, 요, 유, 이
        # (e.g., 꽃잎 becomes 꼰닢, 색연필 becomes 생년필)
        # NOTE: it's hard to generalize this because it depends on the semantics of the word
        if phoneme_list[final] != '' and (next_syllable in ('역', '염', '엿', '유', '율', '윷', '잎') \
                                          or next_two_syllable in ('여름', '여비', '여성', '여우', '연필', '열차', '요기', '이불')):
            phoneme_list[next_initial] = 'n'

        # special cases
        match two_syllable:

            # 맛없- becomes 마덦-
            case '맛없':
                phoneme_list[final] = ''
                phoneme_list[next_initial] = 'd'
                continue

            # common compound words and Sino-Korean words that induce tensing
            case '글자' | '발자' | '발전' | '여권' | '절대':
                phoneme_list[next_initial] = tense_consonant(phoneme_list[next_initial])
                continue

            # more semantic ㅇ linking
            case '담요' | '들일' | '막일' | '맨입' | '물약' | '삯일' | '알약':
                phoneme_list[next_initial] = 'n'

        # preparing syllable-final consonants for sound changes
        if len(phoneme_list[final]) == 0:
            final_change = ''
            final_carry = ''
        elif len(phoneme_list[final]) == 1:
            final_change = ''
            final_carry = phoneme_list[final]
        else:
            match phoneme_list[final]:
                case 'kk' | 'ss' | 'ng' | 'ch':
                    final_change = ''
                    final_carry = phoneme_list[final]
                case 'rs':
                    final_change = 'r'
                    final_carry = 'v' # placeholder for ㄽ
                case _:
                    final_change = phoneme_list[final][0]
                    final_carry = phoneme_list[final][1]

        # ㄹ assimilation
        if phoneme_list[next_initial] == 'n':
            # ㄹ + ㄴ -> 'l-l'
            if final_carry == 'r':
                phoneme_list[next_initial] = 'l'
                final_carry = 'l'
        elif phoneme_list[next_initial] == 'r':
            match final_carry:
                # ㄴ + ㄹ -> 'l-l', ㄹ + ㄹ -> 'l-l'
                case 'n' | 'r':
                    phoneme_list[next_initial] = 'l'
                    final_carry = 'l'
                case '':
                    pass
                # when following a consonant, ㄹ induces nasalization like ㄴ
                case _:
                    phoneme_list[next_initial] = 'n'

        # nasalization
        if phoneme_list[next_initial] in ('n', 'm'):
            match final_carry:
                case 'g' | 'kk' | 'k':
                    final_change = 'ng'
                    final_carry = ''
                case 'b' | 'pp' | 'p':
                    final_change = 'm'
                    final_carry = ''
                case 'd' | 's' | 'ss' | 'j' | 'ch' | 't' | 'h':
                    final_change = 'n'
                    final_carry = ''
                case _:
                    if final_change == 'b':
                        final_change = 'm'
                        final_carry = ''

        # palatalization
        # NOTE: this should only occur for 이, 히, 여, 혀 as grammatical particles, but oh well
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
            match phoneme_list[next_initial]:
                case 'g':
                    phoneme_list[next_initial] = 'k'
                    final_carry = ''
                case 'd':
                    phoneme_list[next_initial] = 't'
                    final_carry = ''
                case 's':
                    phoneme_list[next_initial] = 'ss'
                    final_carry = ''
                case 'j':
                    phoneme_list[next_initial] = 'ch'
                    final_carry = ''

        # ㅎ linking
        if phoneme_list[next_initial] == 'h':
            match final_carry:
                case 'g':
                    phoneme_list[next_initial] = 'k'
                    final_carry = ''
                case 'd' | 's' | 'ss' | 'j' | 'ch' | 'v':
                    phoneme_list[next_initial] = 't'
                    final_carry = ''
                case 'b':
                    phoneme_list[next_initial] = 'p'
                    final_carry = ''
                case _:
                    if show_h == 0:
                        # if show_hada_h = True, create an exception for 하다, 한, 했다, etc.
                        # NOTE: this implementation is over-sensitive because it doesn't consider semantics
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
            match phoneme_list[next_initial]:
                case '': # ㄽ + ㅇ -> ㄹ + ㅆ
                    phoneme_list[next_initial] = 'ss'
                    final_carry = ''
                case 'b': # ㄽ + ㅂ -> ㄹ + ㅃ
                    phoneme_list[next_initial] = 'pp'
                    final_carry = ''
                case _:
                    final_carry = ''

        # linking
        if phoneme_list[next_initial] == '':
            match final_carry:
                case 'h': # for syllables ending in ㅎ, ㄶ, and ㅀ
                    phoneme_list[next_initial] = final_change
                    final_change = ''
                    final_carry = ''
                case '' | 'ng':
                    pass
                case _: # general linking case
                    phoneme_list[next_initial] = final_carry
                    final_carry = ''

        # handling standard cases
        phoneme_list[final] = final_change + final_carry

    # second round of sound changes
    for syllable in range(len(word)):
        initial = 4*syllable
        vowel = 4*syllable + 1
        final = 4*syllable + 2
        next_initial = initial + 4
        next_vowel = vowel + 4

        # flags that indicate the location of the syllable in the word
        first_syllable = (syllable == 0)
        last_syllable = (syllable == len(word) - 1)

        # flag that indicates whether or not to tense the following initial consonant
        tense_next = False

        # syllable-final consonants
        match phoneme_list[final]:

            # ㄱ, ㄲ, ㄳ, ㅋ -> 'k'
            case 'g' | 'kk' | 'gs' | 'k':
                phoneme_list[final] = 'k'
                tense_next = always_tense

            # ㄴ, ㄵ, ㄶ -> 'n'
            case 'n' | 'nj' | 'nh':
                tense_next = (phoneme_list[final] == 'nj')
                phoneme_list[final] = 'n'

            # ㄷ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ, ㅎ -> 't'
            case 'd' | 's' | 'ss' | 'j' | 'ch' | 't' | 'h':
                if not last_syllable and phoneme_list[next_initial] in ('s', 'ss'):
                    phoneme_list[final] = ''
                    tense_next = True
                else:
                    phoneme_list[final] = 't'
                    tense_next = always_tense

            # ㄹ -> l
            case 'r':
                phoneme_list[final] = 'l'
                # ㄹ + ㄹ -> 'l-l'
                if not last_syllable and phoneme_list[next_initial] == 'r':
                    phoneme_list[next_initial] = 'l'

            # ㄺ
            case 'rg':
                # ㄺ + ㄱ -> 'l-kk'
                if not last_syllable and phoneme_list[next_initial] == 'g':
                    phoneme_list[final] = 'l'
                    tense_next = True
                # ㄺ -> 'k'
                else:
                    phoneme_list[final] = 'k'

            # ㄻ, ㅁ -> 'm'
            case 'rm' | 'm':
                tense_next = (phoneme_list[final] == 'rm')
                phoneme_list[final] = 'm'

            # ㄼ
            case 'rb':
                # special case: 밟 + consonant
                if phoneme_list[initial] == 'b' and phoneme_list[vowel] == 'a':
                    phoneme_list[final] = 'p'

                # special case: 넓둥- and 넓죽-
                elif not last_syllable and phoneme_list[initial] == 'n' and phoneme_list[vowel] == 'eo':
                    if phoneme_list[next_initial] == 'd' and phoneme_list[next_vowel] == 'oo':
                        phoneme_list[final] = 'p'
                    elif phoneme_list[next_initial] == 'j' and phoneme_list[next_vowel] in ('eo', 'oo'):
                        phoneme_list[final] = 'p'

                # flag that indicates if we entered a special case
                rb_special = (phoneme_list[final] == 'p')

                # default: ㄼ -> ㄹ
                if not rb_special:
                    phoneme_list[final] = 'l'

                # ㄼ always tenses the next consonant (regardless of if it becomes 'ㅍ' or 'ㄹ')
                # but always_tense decides if we include the in our output for the special 'ㅍ' cases
                tense_next = always_tense or not rb_special

            # ㄽ, ㄾ, ㅀ -> 'l'
            case 'rs' | 'rt' | 'rh':
                phoneme_list[final] = 'l'
                tense_next = True

            # ㄿ, ㅂ, ㅄ, ㅍ -> 'p'
            case 'rp' | 'b' | 'bs' | 'p':
                phoneme_list[final] = 'p'
                tense_next = always_tense

        # tensing
        if not last_syllable and tense_next:
            phoneme_list[next_initial] = tense_consonant(phoneme_list[next_initial])

        # patching in non-Korean characters by handling placeholder
        if phoneme_list[initial] == 'x':
            phoneme_list[initial] = ''
            phoneme_list[final] = ''
            
            # punctuation at the end of a clause
            if not first_syllable and phoneme_list[vowel] in ('!', ',', '.', '?'):
                phoneme_list[initial - 1] = ''

            # quotation marks
            if phoneme_list[vowel] in ('\'', '"'):
                if not first_syllable:
                    phoneme_list[initial - 1] = ''
                else:
                    phoneme_list[final + 1] = ''

            # next character is also non-Korean
            if not last_syllable and phoneme_list[next_initial] == 'x':
                phoneme_list[final + 1] = ''
            
            continue

        # different pronuniciations of ㅢ
        if phoneme_list[vowel] == 'ui': # common sound change; occurs for everything except word-initial and grammatical 의
            phoneme_list[vowel] = 'i'
        elif phoneme_list[vowel] == 'q': # deal with placeholder
            phoneme_list[vowel] = 'ui'

        # 시 -> 'shi'/'si', 샤 -> 'sha'/'sya', etc. (based on configuration)
        if sh and phoneme_list[initial] in ('s', 'ss'):
            if phoneme_list[vowel] in ('i', 'wi'):
                phoneme_list[initial] += 'h'
            elif phoneme_list[vowel][0] == 'y':
                phoneme_list[initial] += 'h'
                phoneme_list[vowel] = phoneme_list[vowel][1:]

        # ㅜ -> 'oo'/'u', ㅠ -> 'yoo'/'yu' (based on configuration)
        if not oo and phoneme_list[vowel] in ('oo', 'yoo'):
            phoneme_list[vowel] = phoneme_list[vowel][0:-2] + 'u'

        # ㅣ -> 'ee'/'i' (based on configuration)
        if ee and phoneme_list[vowel] in ('i', 'wi'):
            phoneme_list[vowel] = phoneme_list[vowel][0:-1] + 'ee'

        # 쟈 -> 'ja'/'jya', 쳐 -> 'cheo'/'chyeo', etc. (based on configuration)
        if no_y and phoneme_list[initial] in ('j', 'jj', 'ch') and phoneme_list[vowel][0] == 'y':
            phoneme_list[vowel] = phoneme_list[4*syllable + 1][1:]

    phoneme_list.pop() # trailing hyphen
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
    with open(hangul_in, 'r', encoding='utf8') as reader, \
         open(romanized_out, 'w', encoding='utf8') as writer:
        for line in reader:
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
print(romanize("??? Korean is fun! Tee샤츠"))                # non-Korean
print(romanize("   "))                                      # edge case
"""

# exceptions: currently non-functional

"""
print(split_hangul("안다 안고 감다 감고 신다 신고 참다 참고"))  # semantic tensing
print(split_hangul("의견란 영업용"))
"""


if __name__ == '__main__':
    while True:
        hangul = input("Hangul (Korean) text to romanize: ")
        print(romanize(hangul))
        print()
