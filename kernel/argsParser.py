from typing import List

def parse(splitted_list: list) -> List[str]:
    string = " ".join(splitted_list)
    words = []
    in_quotes = False
    current_word = ""
    for char in string:
        if char == " " and not in_quotes:
            if current_word:
                words.append(current_word)
                current_word = ""
        elif char == '"':
            in_quotes = not in_quotes
        else:
            current_word += char
    if current_word:
        words.append(current_word)
    return words
