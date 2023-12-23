class HangulRomanizer:
    
    # transliterations of syllable-initial consonants
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

    # transliterations of syllable-final consonants
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

    # transliterations of vowels
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

    @staticmethod
    def tense_consonant(phoneme):
        match phoneme:
            case 'g': return 'kk'
            case 'd': return 'tt'
            case 'b': return 'pp'
            case 's': return 'ss'
            case 'j': return 'jj'
            case _: return phoneme

    
    def __init__(self, na_neo_ye: bool = False, ne_ni: bool = True, \
                 show_h: int = 0, show_hada_h: bool = True, voiced_double: bool = False, sh: bool = True, oo: bool = False, ee: bool = False, \
                 always_tense: bool = False, no_y: bool = False):

        # situational romanization preferences

        self.na_neo_ye = na_neo_ye          # romanize 나의 and 너의 as 'na-ye' and 'neo-ye' respectively (common in songs)
        self.ne_ni = ne_ni                  # romanize 네 as 'ni' and 네가 as 'ni-ga' (common in spoken Korean)

        # purely aesthetic romanization preferences

        self.show_h = show_h                # how to romanize ㅎ linking when aspiration does not occur (e.g., ㄴ + ㅎ)
                                                # 0 = don't show anything (not prescriptive), 1 = show as 'ʰ', 2 = show as 'h'
        self.show_hada_h = show_hada_h      # if True, always show 'h' for 하다 and its conjugations (e.g., 한, 했다)
                                                # only matters if self.show_h == 0
        self.voiced_double = voiced_double  # if True, romanize ㄲ, ㄸ, ㅃ as 'gg', 'dd', 'bb' instead of 'kk', 'tt', 'pp'
        self.sh = sh                        # if True, romanize ㅅ as 'sh' when preceding ㅣ, ㅑ, etc.
        self.oo = oo                        # if True, romanize the vowel ㅜ as 'oo' instead of 'u' (and likewise for ㅠ, but not ㅟ)
        self.ee = ee                        # if True, romanize the vowel ㅣ as 'ee' instead of 'i' (and likewise for ㅟ, but not ㅚ or ㅢ)

        # optional non-standard romanization adjustments

        self.always_tense = always_tense    # always show tensing of initial consonants that occur after final obstruents when applicable
                                                # NOTE: initial consonants that occur after sonorants (non-obstruents, e.g., ㄶ, ㄼ)
                                                # and become tensed for phonological reasons are automatically always denoted as such
        self.no_y = no_y                    # if True, remove the 'y' from the romanization of ㅑ, ㅕ, ㅛ, ㅠ when following ㅈ, ㅉ, ㅊ
                                                # NOTE: this configuration option exists because, for example, 자 and 쟈 sound extremely similar
                                                # and so some people might not find it critical for their use case to distinguish between the two


    def _romanize_word(self, word: str):
        if len(word) == 0:
            return ''

        # special case: 네 -> '니'
        if self.ne_ni:
            if word == '네':
                return 'ni'
            elif word == '네가':
                return 'ni-ga'

        phoneme_list = []
        
        # parsing Hangul and converting to "naive" letter-by-letter romanization
        for syllable in range(len(word)):
            block_ord = ord(word[syllable]) - HangulRomanizer.hangul_blocks

            if block_ord == 7000: # 의
                phoneme_list.append('')
                if syllable == 0:
                    phoneme_list.append('q') # placeholder for non-modified ㅢ
                elif syllable == len(word) - 1: # 의 -> '에' (NOTE: technically, this only applies to the grammatical particle 의)
                    if self.na_neo_ye and syllable == 1 and word[0] in ('나', '너'):
                        phoneme_list.append('ye')
                    else:
                        phoneme_list.append('e')
                else:
                    phoneme_list.append('ui')
                phoneme_list.append('')
            elif 0 <= block_ord < HangulRomanizer.block_count:
                final = HangulRomanizer.final_consonant_phonetics[block_ord % HangulRomanizer.final_consonant_count]
                trunc = block_ord // HangulRomanizer.final_consonant_count
                vowel = HangulRomanizer.vowel_phonetics[trunc % HangulRomanizer.vowel_count]
                initial = HangulRomanizer.initial_consonant_phonetics[trunc // HangulRomanizer.vowel_count]
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
                case '글자' | '될지' | '발자' | '발전' | '여권' | '을지' | '절대' | '할지':
                    phoneme_list[next_initial] = HangulRomanizer.tense_consonant(phoneme_list[next_initial])
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
                        if self.show_h == 0:
                            # if self.show_hada_h = True, create an exception for 하다, 한, 했다, etc.
                            # NOTE: this implementation is over-sensitive because it doesn't consider semantics
                            if not (self.show_hada_h and phoneme_list[next_initial + 1] in ('a', 'ae')):
                                if final_carry not in ('', 'ng'):
                                    phoneme_list[next_initial] = final_carry
                                    final_carry = ''
                                else:
                                    phoneme_list[next_initial] = ''
                        elif self.show_h == 1:
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

            # flag that indicates whether or not to tense the following syllable-initial consonant
            tense_next = False

            # syllable-final consonants
            match phoneme_list[final]:

                # ㄱ, ㄲ, ㄳ, ㅋ -> 'k'
                case 'g' | 'kk' | 'gs' | 'k':
                    phoneme_list[final] = 'k'
                    tense_next = self.always_tense

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
                        tense_next = self.always_tense

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
                    # but self.always_tense decides if we include the in our output for the special 'ㅍ' cases
                    tense_next = self.always_tense or not rb_special

                # ㄽ, ㄾ, ㅀ -> 'l'
                case 'rs' | 'rt' | 'rh':
                    phoneme_list[final] = 'l'
                    tense_next = True

                # ㄿ, ㅂ, ㅄ, ㅍ -> 'p'
                case 'rp' | 'b' | 'bs' | 'p':
                    phoneme_list[final] = 'p'
                    tense_next = self.always_tense

            # tensing
            if not last_syllable and tense_next:
                phoneme_list[next_initial] = HangulRomanizer.tense_consonant(phoneme_list[next_initial])

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

            # tensed consonants: ㄲ -> 'gg'/'kk', ㄸ -> 'dd'/'tt', ㅃ -> 'bb'/'pp'
            if self.voiced_double:
                match phoneme_list[initial]:
                    case 'kk':
                        phoneme_list[initial] = 'gg'
                    case 'tt':
                        phoneme_list[initial] = 'dd'
                    case 'pp':
                        phoneme_list[initial] = 'bb'

            # 시 -> 'shi'/'si', 샤 -> 'sha'/'sya', etc. (based on configuration)
            if self.sh and phoneme_list[initial] in ('s', 'ss'):
                if phoneme_list[vowel] in ('i', 'wi'):
                    phoneme_list[initial] += 'h'
                elif phoneme_list[vowel][0] == 'y':
                    phoneme_list[initial] += 'h'
                    phoneme_list[vowel] = phoneme_list[vowel][1:]

            # ㅜ -> 'oo'/'u', ㅠ -> 'yoo'/'yu' (based on configuration)
            if not self.oo and phoneme_list[vowel] in ('oo', 'yoo'):
                phoneme_list[vowel] = phoneme_list[vowel][0:-2] + 'u'

            # ㅣ -> 'ee'/'i' (based on configuration)
            if self.ee and phoneme_list[vowel] in ('i', 'wi'):
                phoneme_list[vowel] = phoneme_list[vowel][0:-1] + 'ee'

            # 쟈 -> 'ja'/'jya', 쳐 -> 'cheo'/'chyeo', etc. (based on configuration)
            if self.no_y and phoneme_list[initial] in ('j', 'jj', 'ch') and phoneme_list[vowel][0] == 'y':
                phoneme_list[vowel] = phoneme_list[4*syllable + 1][1:]

        phoneme_list.pop() # trailing hyphen
        return(''.join(phoneme_list))


    def romanize(self, hangul_string):
        hangul_string = hangul_string.strip()
        if len(hangul_string) == 0:
            return ''
        
        word_list = []
        hangul_words = hangul_string.split(' ')
        
        for word in hangul_words:
            word_list.append(self._romanize_word(word))
            
        romanized_string = ' '.join(word_list)
        return romanized_string


    def romanize_file(self, hangul_in, romanized_out):
        with open(hangul_in, 'r', encoding='utf8') as reader, \
             open(romanized_out, 'w', encoding='utf8') as writer:
            for line in reader:
                writer.write(self.romanize(line) + '\n')
