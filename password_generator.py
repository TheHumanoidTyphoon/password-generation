import string
import secrets
import random
import requests
import pyperclip
import sys


PROMPTS = {
    "uppercase": "Do you want your password to include uppercase letters? (y/n) ",
    "lowercase": "Do you want your password to include lowercase letters? (y/n) ",
    "letters": "Do you want your password to include numbers? (y/n) ",
    "symbols": "Do you want your password to include symbols? (y/n) ",
}

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 16


def get_choice(prompt):
    """Get user input for a yes/no prompt.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        bool: True if the user entered 'y' or 'Y', False if the user entered 'n' or 'N'.

    Raises:
        KeyboardInterrupt: If the user presses Ctrl+C, the program will exit.

    """
    while True:
        try:
            choice = input(prompt)
            if choice in {"y", "Y"}:
                return True
            elif choice in {"n", "N"}:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()


def get_valid_characters():
    """Get a string of valid characters for the password.

    Returns:
        str: A string of valid characters for the password, based on user input.

    Raises:
        KeyboardInterrupt: If the user presses Ctrl+C, the program will exit.

    """
    valid_chars = ""

    for key, prompt in PROMPTS.items():
        while True:
            try:
                choice = get_choice(prompt)
                if choice:
                    if key == "symbols":
                        valid_chars += string.punctuation
                    else:
                        valid_chars += string.ascii_letters
                    break
                else:
                    break
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit()

    return valid_chars


def calculate_password_strength(password):
    """Calculate the strength of a password and provide feedback.

    Args:
        password (str): The password to evaluate.

    Returns:
        tuple: A tuple containing the strength of the password as an integer (from 0 to 5) and feedback on how to improve the password.

    """
    length = len(password)
    strength = 0
    feedback = ""

    if length < MIN_PASSWORD_LENGTH or length > MAX_PASSWORD_LENGTH:
        feedback += f"The password should be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH} characters long.\n"
    else:
        strength += 1

    if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
        feedback += "The password should contain both uppercase and lowercase letters.\n"
    else:
        strength += 1

    if not any(c.isdigit() for c in password):
        feedback += "The password should contain at least one digit.\n"
    else:
        strength += 1

    if not any(c in string.punctuation for c in password):
        feedback += "The password should contain at least one symbol.\n"
    else:
        strength += 1

    if len(set(password)) != length:
        feedback += "The password should not contain repeated characters.\n"
    else:
        strength += 1

    if strength < 5:
        feedback += "Consider improving your password by increasing its length, complexity, or uniqueness."

    return strength, feedback


def generate_password():
    """Generate and display a password according to the user's specifications.

    Prompts the user for the length of the password and the minimum number of uppercase
    letters, lowercase letters, numbers, and symbols that the password should contain.
    Generates a password that meets the user's specifications and displays its strength
    and feedback. Prompts the user for whether to save the password to a file or copy it
    to the clipboard.
    """
    valid_chars = get_valid_characters()
    if not valid_chars:
        print("Please select at least one option for the password characters.")
        return

    while True:
        try:
            password_length = input(
                f"Enter the desired length of the password (between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}): ")
            if not password_length.isdigit():
                print(
                    f"Please enter a valid password length between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}.")
            elif not MIN_PASSWORD_LENGTH <= int(password_length) <= MAX_PASSWORD_LENGTH:
                print(
                    f"Please enter a valid password length between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}.")
            else:
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()

    min_requirements = {}
    for key, prompt in PROMPTS.items():
        while True:
            try:
                value = input(
                    f"Enter the minimum number of {key} you want in your password: ")
                if not value.isdigit():
                    print(f"{key.capitalize()} minimum must be a positive integer.")
                elif int(value) < 0:
                    print(f"{key.capitalize()} minimum must be a positive integer.")
                elif int(value) > int(password_length):
                    print(
                        f"{key.capitalize()} minimum cannot be greater than the password length.")
                else:
                    break
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit()
        min_requirements[key] = int(value)

    min_total = sum(min_requirements.values())
    if min_total > int(password_length):
        print("The sum of the minimums cannot exceed the password length.")
        return

    password_list = [secrets.choice(string.ascii_uppercase)
                     for _ in range(min_requirements["uppercase"])]
    password_list += [secrets.choice(string.ascii_lowercase)
                      for _ in range(min_requirements["lowercase"])]
    password_list += [secrets.choice(string.digits)
                      for _ in range(min_requirements["letters"])]
    password_list += [secrets.choice(string.punctuation)
                      for _ in range(min_requirements["symbols"])]
    password_list += [secrets.choice(valid_chars)
                      for _ in range(int(password_length) - min_total)]
    shuffled_password = ''.join(random.sample(
        password_list, len(password_list)))

    # Calculate the strength and feedback of the generated password
    strength, feedback = calculate_password_strength(shuffled_password)

    # Display feedback to the user
    print(f"Your password strength is: {strength} out of 5")

    while True:
        save_or_copy = input(
            "Do you want to save it to a file or copy it to the clipboard? (s/c/n) ")
        if save_or_copy.lower() not in ['s', 'c', 'n']:
            print("Please enter a valid option.")
            continue
        break

    # Perform save or copy action
    if save_or_copy.lower() == 's':
        with open('password_history.txt', 'a') as f:
            f.write(shuffled_password + '\n')
        print("Password saved to file.")
    elif save_or_copy.lower() == 'c':
        pyperclip.copy(shuffled_password)
        print("Password copied to clipboard.")
    else:
        print("Password not saved or copied.")


def load_words():
    """
    Retrieves a list of 10,000 English words from a remote server and returns them.

    Returns:
    list: A list of 10,000 English words.

    Raises:
    Exception: If there is a problem with retrieving the list of words.
    """
    response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
    words = response.content.decode().splitlines()
    return words


def generate_passphrase(words):
    """
    Generates a passphrase composed of four randomly chosen words from a list of words.
    Allows the user to save the passphrase to a file or copy it to the clipboard.

    Args:
    words (list): A list of words to choose from.

    Returns:
    None

    Raises:
    ValueError: If the input words list is empty.
    """
    passphrase = "-".join(secrets.choice(words) for _ in range(4))
    print("Passphrase created")
    save_or_copy = input(
        "Do you want to save it to a file or copy it to the clipboard? (s/c/n) ")
    if save_or_copy.lower() == "s":
        filename = input("Enter the filename: ")
        with open(filename, "w") as f:
            f.write(passphrase)
            print("Passphrase saved to", filename)
    elif save_or_copy.lower() == "c":
        pyperclip.copy(passphrase)
        print("Passphrase copied to clipboard")


def main():
    print("What would you like to generate?")
    print("1. Password")
    print("2. Passphrase")
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        num_passwords = int(
            input("How many passwords do you want to generate? "))
        for i in range(num_passwords):
            print(f"Password {i+1}:")
            generate_password()
    elif choice == "2":
        num_passphrases = int(
            input("How many passphrases do you want to generate? "))
        words = load_words()
        for i in range(num_passphrases):
            print(f"Passphrase {i+1}:")
            generate_passphrase(words)
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    """Generate and display a password or passphrase according to the user's specifications."""
    main()



