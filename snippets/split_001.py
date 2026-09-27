def split(string: str, separator: str = " ") -> list:
    """
    Will split the string up into all the values separated by the separator
    (defaults to spaces)
    """
    split_words = []
    last_index = 0
    for index, char in enumerate(string):
        if char == separator:
            split_words.append(string[last_index:index])
            last_index = index + 1
        elif index + 1 == len(string):
            split_words.append(string[last_index : index + 1])
    return split_words

if __name__ == "__main__":
    test_string = "a--b--c"
    test_separator = "--"
    result = split(test_string, test_separator)
    print(result)