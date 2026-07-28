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
    def test_too_short(self):
        assert validate_password("Ab1!xyz") is False

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

    def test_only_digits(self):
        assert validate_password("12345678") is False

    def test_only_special_characters(self):
        assert validate_password("!@#$%^&*") is False

    def test_all_requirements_missing_and_too_short(self):
        assert validate_password("abc") is False


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
