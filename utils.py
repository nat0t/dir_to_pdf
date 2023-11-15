def delete_escape_chr(text: str) -> str:
    """Remove escape characters from text."""
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return text.translate(translator)
