SPECIAL_CHARACTERS = set("!@#$%^&*")


def validate_password(password):
    """Check whether a password meets all of the required rules.

    Rules:
    - at least 8 characters long
    - contains at least one uppercase letter
    - contains at least one lowercase letter
    - contains at least one digit
    - contains at least one special character from: !@#$%^&*

    Returns True if all rules are satisfied, False otherwise.
    """
    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in SPECIAL_CHARACTERS:
            has_special = True

    return has_upper and has_lower and has_digit and has_special
