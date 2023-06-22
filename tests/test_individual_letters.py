import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest

from korean_romanization import HangulRomanizer

class TestInitials:
    hangul_romanizer = HangulRomanizer()
    
    def test_one(self):
        output = self.hangul_romanizer.romanize("가 나 다")
        assert output == "ga na da"

class TestVowels:
    hangul_romanizer = HangulRomanizer()
    
    def test_two(self):
        output = self.hangul_romanizer.romanize("가 거 고 구")
        assert output == "ga geo go gu"

class TestFinals:
    hangul_romanizer = HangulRomanizer()
    
    def test_three(self):
        output = self.hangul_romanizer.romanize("악 안 앋")
        assert output == "ak an at"
