import string
import random


def generate_password(length=12):
    """Generate a random password for a user."""
    # Define the character sets to use for generating the password
    letters = string.ascii_letters
    digits = string.digits
    special_characters = "!@#$%^&*()"

    # Combine all character sets
    all_characters = letters + digits + special_characters

    # Generate a random password of specified length
    password = "".join(random.choice(all_characters) for _ in range(length))
    return password
