# Password Generator
This Python script offers a solution to generate a highly secure and unique password that caters to the user's individual preferences and specifications. By allowing the user to specify the length, character types, and minimum requirements for each type, the script generates a random password that meets all criteria. This ensures that the password generated is both robust and memorable. With this script, users can rest assured that their sensitive data and online accounts are protected.

## Dependencies
This script requires the following dependencies:

- `Python 3.x`
- `requests`
- `pyperclip`

You can install these dependencies using pip:
``` python
pip install requests pyperclip
```

## Usage
To use this script, simply run the following command in your terminal:
``` python
python password_generator.py
```

Once you run the script, you will be prompted to choose which types of characters you want to include in your password (uppercase letters, lowercase letters, numbers, and symbols). Then, you will be prompted to enter the desired length of the password (between 8 and 16 characters) and the minimum number of each character type you want to include.

After you enter these specifications, the script will generate a random password that meets your requirements and display its strength and feedback on how to improve the password. You will also be prompted to save the password to a file or copy it to the clipboard.

## Functions
This script includes the following functions:

- `get_choice(prompt)`: Gets user input for a yes/no prompt and returns True if the user enters `'y'` or `'Y'`, False if the user enters `'n'` or `'N'`.
- `get_valid_characters()`: Gets a string of valid characters for the password based on user input.
- `calculate_password_strength(password)`: Calculates the strength of a password and provides feedback on how to improve it.
- `generate_password()`: Generates and displays a password according to the user's specifications.

## Constants
This script includes the following constants:

- `PROMPTS`: A dictionary containing the prompts for each character type.
- `MIN_PASSWORD_LENGTH`: The minimum length of the password `(8)`.
- `MAX_PASSWORD_LENGTH`: The maximum length of the password `(16)`.

## Contributing 
If you have any suggestions for improving the program or finding bugs, please submit an [issue](https://github.com/TheHumanoidTyphoon/football-match-data-scraper-and-analysis/issues) or pull request on the [GitHub repository](https://github.com/TheHumanoidTyphoon/match-data-scraper).

## License
This script is released under the [MIT]() License.
