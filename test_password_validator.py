import time

import pytest

from password_validator import validate_password


class TestValidPasswords:
    def test_typical_valid_password(self):
        assert validate_password("Abcdefg1!") is True

    def test_valid_password_with_different_special_chars(self):
        assert validate_password("Password9@") is True
        assert validate_password("Password9#") is True
        assert validate_password("Password9$") is True
        assert validate_password("Password9^") is True
        assert validate_password("Password9&") is True
        assert validate_password("Password9*") is True

    def test_valid_password_exactly_eight_characters(self):
        assert validate_password("Abcdef1!") is True

    def test_valid_password_with_multiple_special_characters(self):
        assert validate_password("Ab1!Ab1!") is True

    def test_valid_long_password(self):
        assert validate_password("ThisIsAVeryLongPassword123!") is True


class TestInvalidPasswords:
    def test_empty_string(self):
        assert validate_password("") is False

    def test_missing_uppercase(self):
        assert validate_password("abcdefg1!") is False

    def test_missing_lowercase(self):
        assert validate_password("ABCDEFG1!") is False

    def test_missing_digit(self):
        assert validate_password("Abcdefgh!") is False

    def test_missing_special_character(self):
        assert validate_password("Abcdefg1") is False

    def test_only_lowercase_letters(self):
        assert validate_password("abcdefgh") is False

    def test_only_uppercase_letters(self):
        assert validate_password("ABCDEFGH") is False

    def test_only_digits(self):
        assert validate_password("12345678") is False

    def test_only_special_characters(self):
        assert validate_password("!@#$%^&*") is False


class TestEdgeCases:
    def test_seven_characters_with_all_other_requirements(self):
        assert validate_password("Abcde1!") is False

    def test_special_character_not_in_allowed_set(self):
        # '?' is not part of the allowed special character set.
        assert validate_password("Abcdefg1?") is False

    def test_whitespace_does_not_count_as_special_character(self):
        assert validate_password("Abcdefg1 ") is False

    def test_password_with_spaces_between_valid_characters(self):
        assert validate_password("Abc def1!") is True

    def test_unicode_letters_are_not_ascii_upper_lower_but_still_checked(self):
        # 'É' is uppercase and 'é' is lowercase per str.isupper()/islower(),
        # so this should still satisfy the letter-case requirements.
        assert validate_password("Ééééééé1!") is True

    def test_non_string_like_numeric_characters_still_count_as_digits(self):
        assert validate_password("Abcdefg0!") is True

    def test_exactly_meets_each_requirement_once(self):
        assert validate_password("Aa1!aaaa") is True

    def test_all_whitespace_password(self):
        assert validate_password("        ") is False

    def test_valid_password_with_leading_whitespace(self):
        assert validate_password(" Abcdefg1!") is True

    def test_valid_password_with_trailing_whitespace(self):
        assert validate_password("Abcdefg1! ") is True

    def test_valid_password_with_leading_and_trailing_whitespace(self):
        assert validate_password(" Abcdefg1! ") is True

    def test_emoji_does_not_count_as_special_character(self):
        # The emoji is not upper, lower, digit, or in the allowed special
        # character set, so it's silently ignored, leaving the
        # special-character requirement unmet.
        assert validate_password("Abcdefg1\U0001F512") is False

    def test_family_emoji_does_not_count_as_special_character(self):
        # The family emoji is actually 7 Unicode code points (four person
        # emoji joined by zero-width-joiner characters, U+200D), so len()
        # and the character loop both operate on code points rather than
        # the single visual glyph a person sees -- meaning the password is
        # much longer than 9 characters, and every one of those 7 code
        # points independently fails the upper/lower/digit/special checks,
        # leaving the special-character requirement unmet.
        assert validate_password("Abcdefg1\U0001F468‍\U0001F469‍\U0001F467‍\U0001F466") is False

    def test_valid_very_long_password(self):
        # Distinct from test_valid_long_password (28 chars): confirms
        # there's no accidental upper bound or off-by-one issue at scale.
        password = "Aa1!" + ("x" * 4996)
        assert len(password) == 5000
        assert validate_password(password) is True

    def test_long_password_performance(self):
        # Regression guard against a future refactor accidentally
        # introducing quadratic behavior (e.g., repeated password.count(c)
        # calls or backtracking regex) into what is currently an O(n)
        # single-pass loop.
        password = "Aa1!" + ("x" * 49996)
        assert len(password) == 50000

        start = time.perf_counter()
        result = validate_password(password)
        elapsed = time.perf_counter() - start

        assert result is True
        assert elapsed < 1.0

    def test_none_input_raises_type_error(self):
        # Documents current crash behavior: the function does not guard
        # against non-string input, so None raises TypeError (len(None)).
        with pytest.raises(TypeError):
            validate_password(None)
